"""Generate the PCB Kalvi practice project: a 5V power-indicator LED board (J1, R1, D1) in KiCad 6+ format."""
import uuid, json, zipfile, os, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
_n = [0]
def U():
    _n[0] += 1
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "pcbkalvi/" + str(_n[0])))
E = '(effects (font (size 1.27 1.27)))'
EH = '(effects (font (size 1.27 1.27)) hide)'
ST = '(stroke (width 0) (type default) (color 0 0 0 0))'

def prop(name, val, i, at, hide=False, rot=0):
    return f'(property "{name}" "{val}" (id {i}) (at {at[0]} {at[1]} {rot}) {EH if hide else E})'

# ---------- schematic library symbols ----------
LIB = f'''
  (lib_symbols
    (symbol "Device:R" (pin_numbers hide) (pin_names (offset 0)) (in_bom yes) (on_board yes)
      {prop("Reference","R",0,(2.032,0),rot=90)}
      {prop("Value","R",1,(0,0),rot=90)}
      {prop("Footprint","",2,(-1.778,0),True,90)}
      {prop("Datasheet","~",3,(0,0),True)}
      (symbol "R_0_1"
        (rectangle (start -1.016 -2.54) (end 1.016 2.54) {ST} (fill (type none)))
      )
      (symbol "R_1_1"
        (pin passive line (at 0 3.81 270) (length 1.27) (name "~" {E}) (number "1" {E}))
        (pin passive line (at 0 -3.81 90) (length 1.27) (name "~" {E}) (number "2" {E}))
      )
    )
    (symbol "Device:LED" (pin_numbers hide) (pin_names (offset 1.016) hide) (in_bom yes) (on_board yes)
      {prop("Reference","D",0,(0,2.54))}
      {prop("Value","LED",1,(0,-2.54))}
      {prop("Footprint","",2,(0,0),True)}
      {prop("Datasheet","~",3,(0,0),True)}
      (symbol "LED_0_1"
        (polyline (pts (xy -1.27 -1.27) (xy -1.27 1.27)) (stroke (width 0.254) (type default) (color 0 0 0 0)) (fill (type none)))
        (polyline (pts (xy -1.27 0) (xy 1.27 0)) {ST} (fill (type none)))
        (polyline (pts (xy 1.27 -1.27) (xy 1.27 1.27) (xy -1.27 0) (xy 1.27 -1.27)) (stroke (width 0.254) (type default) (color 0 0 0 0)) (fill (type none)))
        (polyline (pts (xy -3.048 -0.762) (xy -4.572 -2.286) (xy -3.81 -2.286) (xy -4.572 -2.286) (xy -4.572 -1.524)) {ST} (fill (type none)))
        (polyline (pts (xy -1.778 -0.762) (xy -3.302 -2.286) (xy -2.54 -2.286) (xy -3.302 -2.286) (xy -3.302 -1.524)) {ST} (fill (type none)))
      )
      (symbol "LED_1_1"
        (pin passive line (at -3.81 0 0) (length 2.54) (name "K" {E}) (number "1" {E}))
        (pin passive line (at 3.81 0 180) (length 2.54) (name "A" {E}) (number "2" {E}))
      )
    )
    (symbol "Connector:Conn_01x02_Pin" (pin_names (offset 1.016) hide) (in_bom yes) (on_board yes)
      {prop("Reference","J",0,(0,2.54))}
      {prop("Value","Conn_01x02_Pin",1,(0,-5.08))}
      {prop("Footprint","",2,(0,0),True)}
      {prop("Datasheet","~",3,(0,0),True)}
      (symbol "Conn_01x02_Pin_1_1"
        (polyline (pts (xy 1.27 -2.54) (xy 0.8636 -2.54)) (stroke (width 0.1524) (type default) (color 0 0 0 0)) (fill (type none)))
        (polyline (pts (xy 1.27 0) (xy 0.8636 0)) (stroke (width 0.1524) (type default) (color 0 0 0 0)) (fill (type none)))
        (rectangle (start 0.8636 -2.413) (end 0 -2.667) (stroke (width 0.1524) (type default) (color 0 0 0 0)) (fill (type outline)))
        (rectangle (start 0.8636 0.127) (end 0 -0.127) (stroke (width 0.1524) (type default) (color 0 0 0 0)) (fill (type outline)))
        (pin passive line (at 5.08 0 180) (length 3.81) (name "Pin_1" {E}) (number "1" {E}))
        (pin passive line (at 5.08 -2.54 180) (length 3.81) (name "Pin_2" {E}) (number "2" {E}))
      )
    )
    (symbol "power:+5V" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
      {prop("Reference","#PWR",0,(0,-3.81),True)}
      {prop("Value","+5V",1,(0,3.556))}
      {prop("Footprint","",2,(0,0),True)}
      {prop("Datasheet","",3,(0,0),True)}
      (symbol "+5V_0_1"
        (polyline (pts (xy -0.762 1.27) (xy 0 2.54)) {ST} (fill (type none)))
        (polyline (pts (xy 0 0) (xy 0 2.54)) {ST} (fill (type none)))
        (polyline (pts (xy 0 2.54) (xy 0.762 1.27)) {ST} (fill (type none)))
      )
      (symbol "+5V_1_1"
        (pin power_in line (at 0 0 90) (length 0) hide (name "+5V" {E}) (number "1" {E}))
      )
    )
    (symbol "power:GND" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
      {prop("Reference","#PWR",0,(0,-6.35),True)}
      {prop("Value","GND",1,(0,-3.81))}
      {prop("Footprint","",2,(0,0),True)}
      {prop("Datasheet","",3,(0,0),True)}
      (symbol "GND_0_1"
        (polyline (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27)) {ST} (fill (type none)))
      )
      (symbol "GND_1_1"
        (pin power_in line (at 0 0 270) (length 0) hide (name "GND" {E}) (number "1" {E}))
      )
    )
  )'''

insts, paths = [], []
DX, DY = 50.8, 20.32  # move the drawing toward the middle of the A5 sheet
O = lambda pt: (round(pt[0] + DX, 2), round(pt[1] + DY, 2))
def sym(lib, ref, val, fp, at, refat, valat, npins, rot=0, hide_ref=False):
    u = U()
    at, refat, valat = O(at), O(refat), O(valat)
    pins = "".join(f'\n    (pin "{i+1}" (uuid {U()}))' for i in range(npins))
    insts.append(f'''  (symbol (lib_id "{lib}") (at {at[0]} {at[1]} {rot}) (unit 1)
    (in_bom yes) (on_board yes)
    (uuid {u})
    {prop("Reference", ref, 0, refat, hide_ref)}
    {prop("Value", val, 1, valat)}
    {prop("Footprint", fp, 2, at, True)}
    {prop("Datasheet", "~", 3, at, True)}{pins}
  )''')
    paths.append(f'    (path "/{u}" (reference "{ref}") (unit 1) (value "{val}") (footprint "{fp}"))')

sym("Connector:Conn_01x02_Pin", "J1", "5V IN", "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", (38.1, 50.8), (38.1, 46.99), (38.1, 57.15), 2)
sym("Device:R", "R1", "330", "Resistor_SMD:R_0805_2012Metric", (63.5, 55.88), (66.04, 54.61), (66.04, 57.15), 2)
sym("Device:LED", "D1", "RED", "LED_SMD:LED_0805_2012Metric", (55.88, 60.96), (55.88, 66.04), (55.88, 68.58), 2)
sym("power:+5V", "#PWR01", "+5V", "", (63.5, 50.8), (63.5, 54.61), (63.5, 47.244), 1, hide_ref=True)
sym("power:GND", "#PWR02", "GND", "", (48.26, 63.5), (48.26, 69.85), (48.26, 67.31), 1, hide_ref=True)

def wire(a, b):
    a, b = O(a), O(b)
    return f'  (wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]}))\n    {ST}\n    (uuid {U()})\n  )'
W = [((43.18, 50.8), (63.5, 50.8)), ((63.5, 50.8), (63.5, 52.07)),
     ((63.5, 59.69), (63.5, 60.96)), ((63.5, 60.96), (59.69, 60.96)),
     ((52.07, 60.96), (48.26, 60.96)), ((48.26, 60.96), (48.26, 53.34)), ((48.26, 53.34), (43.18, 53.34)),
     ((48.26, 60.96), (48.26, 63.5))]
wires = "\n".join(wire(a, b) for a, b in W)
junc = f'  (junction (at {48.26 + DX} {round(60.96 + DY, 2)}) (diameter 0) (color 0 0 0 0)\n    (uuid {U()})\n  )'
def text(t, x, y, size=1.27):
    x, y = O((x, y))
    return f'  (text "{t}" (at {x} {y} 0)\n    (effects (font (size {size} {size})) (justify left bottom))\n    (uuid {U()})\n  )'
texts = "\n".join([
    text("PCB Kalvi practice project: 5V power LED", 30.48, 30.48, 2.54),
    text("Current = (5V - 2V LED) / 330 ohm = about 9 mA", 30.48, 35.56),
    text("LED: long leg / A = anode (+), K = cathode (-) to GND", 30.48, 38.1),
])
SCH = f'''(kicad_sch (version 20211123) (generator eeschema)

  (uuid {U()})

  (paper "A5")

  (title_block
    (title "LED Kalvi - power indicator")
    (date "2026-10-11")
    (rev "v1")
    (company "PCB Kalvi")
    (comment 1 "Practice project for the Learn KiCad course")
  )
{LIB}

{junc}

{wires}

{texts}

{chr(10).join(insts)}

  (sheet_instances
    (path "/" (page "1"))
  )

  (symbol_instances
{chr(10).join(paths)}
  )
)
'''

# ---------- PCB ----------
NETS = {0: "", 1: "+5V", 2: "GND", 3: "Net-(D1-A)"}
def tstamp(): return f'(tstamp {U()})'
def fptext(kind, val, at, layer, hide=False):
    return f'    (fp_text {kind} "{val}" (at {at[0]} {at[1]}) (layer "{layer}"){" hide" if hide else ""}\n      (effects (font (size 1 1) (thickness 0.15)))\n      {tstamp()}\n    )'
def line(a, b, layer, w=0.12):
    return f'    (fp_line (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (layer "{layer}") (width {w}) {tstamp()})'
def rect(a, b, layer, w=0.05):
    return "\n".join(line(p, q, layer, w) for p, q in [((a[0], a[1]), (b[0], a[1])), ((b[0], a[1]), (b[0], b[1])), ((b[0], b[1]), (a[0], b[1])), ((a[0], b[1]), (a[0], a[1]))])
def net(n): return f'(net {n} "{NETS[n]}")'

def smd2(lib, ref, val, at, rot, pads, body, silk, extra=""):
    ang = f" {rot}" if rot else ""
    p = "\n".join(f'    (pad "{num}" smd roundrect (at {x} 0{ang}) (size {w} {h}) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) {net(n)} {tstamp()})' for num, x, w, h, n in pads)
    return f'''  (footprint "{lib}" (layer "F.Cu")
    {tstamp()}
    (at {at[0]} {at[1]}{ang})
    (attr smd)
{fptext("reference", ref, (0, -1.65), "F.SilkS")}
{fptext("value", val, (0, 1.65), "F.Fab")}
{rect((-body[0], -body[1]), (body[0], body[1]), "F.Fab", 0.1)}
{rect((-1.68, -0.95), (1.68, 0.95), "F.CrtYd", 0.05)}
{silk}
{extra}
{p}
  )'''

R1 = smd2("Resistor_SMD:R_0805_2012Metric", "R1", "330", (115, 105), 0,
          [("1", -0.9125, 1.025, 1.4, 1), ("2", 0.9125, 1.025, 1.4, 3)], (1, 0.625),
          line((-0.227064, -0.735), (0.227064, -0.735), "F.SilkS") + "\n" + line((-0.227064, 0.735), (0.227064, 0.735), "F.SilkS"))
D1 = smd2("LED_SMD:LED_0805_2012Metric", "D1", "RED", (121, 105), 180,
          [("1", -0.9375, 0.975, 1.4, 2), ("2", 0.9375, 0.975, 1.4, 3)], (1, 0.6),
          line((1, -0.96), (-1.685, -0.96), "F.SilkS") + "\n" + line((-1.685, -0.96), (-1.685, 0.96), "F.SilkS") + "\n" + line((-1.685, 0.96), (1, 0.96), "F.SilkS"),
          line((-0.3, -0.6), (-0.3, 0.6), "F.Fab", 0.1))

J1 = f'''  (footprint "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" (layer "F.Cu")
    {tstamp()}
    (at 104.5 106.23)
    (attr through_hole)
{fptext("reference", "J1", (0, -2.33), "F.SilkS")}
{fptext("value", "5V IN", (0, 4.87), "F.Fab")}
{line((-1.33, 3.87), (1.33, 3.87), "F.SilkS")}
{line((-1.33, 1.27), (-1.33, 3.87), "F.SilkS")}
{line((1.33, 1.27), (1.33, 3.87), "F.SilkS")}
{line((-1.33, 1.27), (1.33, 1.27), "F.SilkS")}
{line((-1.33, 0), (-1.33, -1.33), "F.SilkS")}
{line((-1.33, -1.33), (0, -1.33), "F.SilkS")}
{rect((-1.8, -1.8), (1.8, 4.35), "F.CrtYd")}
{rect((-1.27, -1.27), (1.27, 3.81), "F.Fab", 0.1)}
    (pad "1" thru_hole rect (at 0 0) (size 1.7 1.7) (drill 1) (layers *.Cu *.Mask) {net(1)} {tstamp()})
    (pad "2" thru_hole oval (at 0 2.54) (size 1.7 1.7) (drill 1) (layers *.Cu *.Mask) {net(2)} {tstamp()})
  )'''

def hole(ref, at):
    return f'''  (footprint "MountingHole:MountingHole_3.2mm_M3_Pad" (layer "F.Cu")
    {tstamp()}
    (at {at[0]} {at[1]})
    (attr exclude_from_pos_files exclude_from_bom)
{fptext("reference", ref, (0, -4.2), "F.SilkS", True)}
{fptext("value", "MountingHole", (0, 4.2), "F.Fab", True)}
    (fp_circle (center 0 0) (end 3.45 0) (layer "F.CrtYd") (width 0.05) (fill none) {tstamp()})
    (pad "1" thru_hole circle (at 0 0) (size 6.4 6.4) (drill 3.2) (layers *.Cu *.Mask) {tstamp()})
  )'''

def seg(a, b, w, n):
    return f'  (segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width {w}) (layer "F.Cu") {net(n)} {tstamp()})'
SEG = [((104.5, 106.23), (108, 106.23), 0.5, 1), ((108, 106.23), (109.23, 105), 0.5, 1), ((109.23, 105), (114.0875, 105), 0.5, 1),
       ((115.9125, 105), (120.0625, 105), 0.3, 3),
       ((121.9375, 105), (123.5, 105), 0.5, 2), ((123.5, 105), (125, 106.5), 0.5, 2), ((125, 106.5), (125, 108), 0.5, 2),
       ((125, 108), (124.23, 108.77), 0.5, 2), ((124.23, 108.77), (104.5, 108.77), 0.5, 2)]

def gr_line(a, b, layer="Edge.Cuts", w=0.1):
    return f'  (gr_line (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (layer "{layer}") (width {w}) {tstamp()})'
def gr_text(t, at, layer="F.SilkS", size=1):
    mir = " (justify mirror)" if layer.startswith("B.") else ""
    return f'  (gr_text "{t}" (at {at[0]} {at[1]}) (layer "{layer}") {tstamp()}\n    (effects (font (size {size} {size}) (thickness 0.15)){mir})\n  )'
edge = [((100, 100), (130, 100)), ((130, 100), (130, 120)), ((130, 120), (100, 120)), ((100, 120), (100, 100))]

LAYERS = '''  (layers
    (0 "F.Cu" signal)
    (31 "B.Cu" signal)
    (34 "B.Paste" user)
    (35 "F.Paste" user)
    (36 "B.SilkS" user "B.Silkscreen")
    (37 "F.SilkS" user "F.Silkscreen")
    (38 "B.Mask" user)
    (39 "F.Mask" user)
    (40 "Dwgs.User" user "User.Drawings")
    (41 "Cmts.User" user "User.Comments")
    (44 "Edge.Cuts" user)
    (45 "Margin" user)
    (46 "B.CrtYd" user "B.Courtyard")
    (47 "F.CrtYd" user "F.Courtyard")
    (48 "B.Fab" user)
    (49 "F.Fab" user)
  )'''
PCB = f'''(kicad_pcb (version 20211014) (generator pcbnew)

  (general
    (thickness 1.6)
  )

  (paper "A4")
  (title_block
    (title "LED Kalvi - power indicator")
    (date "2026-10-11")
    (rev "v1")
    (company "PCB Kalvi")
  )

{LAYERS}

  (setup
    (pad_to_mask_clearance 0)
  )

{chr(10).join(f'  (net {k} "{v}")' for k, v in NETS.items())}

{J1}
{R1}
{D1}
{hole("H1", (126, 116))}
{hole("H2", (104, 116))}

{chr(10).join(gr_line(a, b, "Edge.Cuts", 0.1) for a, b in edge)}
{gr_text("LED KALVI v1", (115, 112), "F.SilkS", 1.2)}
{gr_text("+5V", (101.55, 106.23), "F.SilkS", 0.7)}
{gr_text("GND", (101.55, 108.77), "F.SilkS", 0.7)}
{gr_text("pcb.azr-operations.com", (115, 118.2), "B.SilkS", 0.8)}

{chr(10).join(seg(a, b, w, n) for a, b, w, n in SEG)}
)
'''
PRO = {"meta": {"filename": "led-kalvi.kicad_pro", "version": 1}, "board": {}, "schematic": {}, "sheets": [], "text_variables": {}}
files = {"led-kalvi.kicad_sch": SCH, "led-kalvi.kicad_pcb": PCB, "led-kalvi.kicad_pro": json.dumps(PRO, indent=2) + "\n"}
for n, c in files.items():
    open(os.path.join(OUT, n), "w").write(c)
with zipfile.ZipFile(os.path.join(OUT, "led-kalvi.zip"), "w", zipfile.ZIP_DEFLATED) as z:
    for n, c in files.items():
        z.writestr("led-kalvi/" + n, c)
    z.writestr("led-kalvi/README.txt", "PCB Kalvi practice project: 5V power LED (J1 header, R1 330 ohm 0805, D1 red LED 0805).\nOpen led-kalvi.kicad_pro in KiCad 7 or newer. KiCad will offer to update the files to its current format: say yes.\nBoard: 30 x 20 mm, 2 layers, two M3 mounting holes.\n")
print("ok", {n: len(c) for n, c in files.items()})
