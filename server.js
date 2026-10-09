// PCB Kalvi server: serves the app and the "My Workshop" API (board stock + photos).
// Data lives outside git in DATA_DIR (default ./data): workshop.json + uploads/.
"use strict";
const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const crypto = require("crypto");

const PORT = Number(process.env.PORT || 3070);
const DATA = process.env.DATA_DIR || path.join(__dirname, "data");
const UPLOADS = path.join(DATA, "uploads");
const DB_FILE = path.join(DATA, "workshop.json");
const PIN = String(process.env.WORKSHOP_PIN || "");
const MAX_PHOTOS = 6;

fs.mkdirSync(UPLOADS, { recursive: true });
if (!PIN) console.warn("[pcb-kalvi] WORKSHOP_PIN is not set: adding/editing is disabled until you set it.");

/* ---------- tiny JSON store ---------- */
function readDB() {
  try { const d = JSON.parse(fs.readFileSync(DB_FILE, "utf8")); return Array.isArray(d.items) ? d : { items: [] }; }
  catch (e) { return { items: [] }; }
}
function writeDB(db) {
  const tmp = DB_FILE + ".tmp";
  fs.writeFileSync(tmp, JSON.stringify(db, null, 2));
  fs.renameSync(tmp, DB_FILE);
}

/* ---------- PIN check with simple lockout ---------- */
const fails = new Map(); // ip -> {n, until}
function ipOf(req) { return (req.headers["x-forwarded-for"] || req.socket.remoteAddress || "").split(",")[0].trim(); }
function pinOK(given) {
  if (!PIN || !given) return false;
  const a = crypto.createHash("sha256").update(String(given)).digest();
  const b = crypto.createHash("sha256").update(PIN).digest();
  return crypto.timingSafeEqual(a, b);
}
function requirePin(req, res, next) {
  const ip = ipOf(req), f = fails.get(ip);
  if (f && f.until > Date.now()) return res.status(429).json({ error: "Too many wrong PINs. Try again in 15 minutes." });
  if (!PIN) return res.status(503).json({ error: "Workshop PIN is not set on the server." });
  if (!pinOK(req.headers["x-workshop-pin"])) {
    const n = (f && f.until > Date.now() - 15 * 60e3 ? f.n : 0) + 1;
    fails.set(ip, { n, until: n >= 5 ? Date.now() + 15 * 60e3 : 0 });
    return res.status(401).json({ error: "Wrong PIN." });
  }
  fails.delete(ip);
  next();
}

/* ---------- uploads ---------- */
const OK_TYPES = { "image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp" };
const upload = multer({
  storage: multer.diskStorage({
    destination: UPLOADS,
    filename: (req, file, cb) => cb(null, crypto.randomBytes(12).toString("hex") + OK_TYPES[file.mimetype])
  }),
  limits: { fileSize: 8 * 1024 * 1024, files: MAX_PHOTOS },
  fileFilter: (req, file, cb) => cb(null, !!OK_TYPES[file.mimetype])
});
function removePhoto(name) {
  if (!/^[a-f0-9]{24}\.(jpg|png|webp)$/.test(name)) return;
  fs.unlink(path.join(UPLOADS, name), () => {});
}

/* ---------- validation ---------- */
const STATUSES = ["stock", "use", "used", "faulty"];
const str = (v, max) => String(v == null ? "" : v).trim().slice(0, max);
function cleanItem(body) {
  const qty = Math.max(0, Math.min(9999, Math.round(Number(body.qty) || 0)));
  const price = body.price === "" || body.price == null ? null : Math.max(0, Math.min(1e6, Number(body.price) || 0));
  return {
    board: str(body.board, 40).replace(/[^a-z0-9]/gi, "") || "other",
    name: str(body.name, 80),
    qty,
    status: STATUSES.includes(body.status) ? body.status : "stock",
    location: str(body.location, 80),
    bought: /^\d{4}-\d{2}-\d{2}$/.test(String(body.bought || "")) ? body.bought : "",
    price,
    project: str(body.project, 120),
    notes: str(body.notes, 1500)
  };
}

/* ---------- app ---------- */
const app = express();
app.disable("x-powered-by");
app.set("trust proxy", "loopback");
app.use((req, res, next) => {
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("Referrer-Policy", "same-origin");
  next();
});

app.get(["/", "/index.html"], (req, res) => res.sendFile(path.join(__dirname, "index.html")));
app.use("/uploads", express.static(UPLOADS, { maxAge: "30d", index: false, dotfiles: "deny" }));

app.get("/api/workshop", (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  res.json({ items: readDB().items, pinSet: !!PIN });
});

app.post("/api/workshop/unlock", express.json({ limit: "2kb" }), (req, res, next) => {
  req.headers["x-workshop-pin"] = req.body && req.body.pin;
  next();
}, requirePin, (req, res) => res.json({ ok: true }));

app.post("/api/workshop", requirePin, upload.array("photos", MAX_PHOTOS), (req, res) => {
  const db = readDB();
  const item = Object.assign({ id: crypto.randomBytes(8).toString("hex"), added: new Date().toISOString() }, cleanItem(req.body));
  item.photos = (req.files || []).map(f => f.filename);
  db.items.unshift(item);
  writeDB(db);
  res.json({ item });
});

app.put("/api/workshop/:id", requirePin, upload.array("photos", MAX_PHOTOS), (req, res) => {
  const db = readDB();
  const it = db.items.find(x => x.id === req.params.id);
  if (!it) { (req.files || []).forEach(f => removePhoto(f.filename)); return res.status(404).json({ error: "Item not found." }); }
  let keep = [];
  try { keep = JSON.parse(req.body.keep || "[]"); } catch (e) { keep = []; }
  keep = (it.photos || []).filter(p => keep.includes(p));
  (it.photos || []).filter(p => !keep.includes(p)).forEach(removePhoto);
  const added = (req.files || []).map(f => f.filename);
  const photos = keep.concat(added);
  photos.slice(MAX_PHOTOS).forEach(removePhoto);
  Object.assign(it, cleanItem(req.body), { photos: photos.slice(0, MAX_PHOTOS), updated: new Date().toISOString() });
  writeDB(db);
  res.json({ item: it });
});

app.delete("/api/workshop/:id", requirePin, (req, res) => {
  const db = readDB();
  const i = db.items.findIndex(x => x.id === req.params.id);
  if (i < 0) return res.status(404).json({ error: "Item not found." });
  (db.items[i].photos || []).forEach(removePhoto);
  db.items.splice(i, 1);
  writeDB(db);
  res.json({ ok: true });
});

app.use((err, req, res, next) => {
  if (err && err.code === "LIMIT_FILE_SIZE") return res.status(413).json({ error: "Photo is larger than 8 MB." });
  if (err && err.code === "LIMIT_FILE_COUNT") return res.status(413).json({ error: `Maximum ${MAX_PHOTOS} photos per board.` });
  console.error(err);
  res.status(500).json({ error: "Server error." });
});
app.use((req, res) => res.status(404).send("Not found"));

app.listen(PORT, "127.0.0.1", () => console.log(`[pcb-kalvi] listening on 127.0.0.1:${PORT}, data in ${DATA}`));
