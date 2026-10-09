# PCB Kalvi · பிசிபி கல்வி

Interactive PCB learning app. Every board is drawn as a digital diagram you can rotate, tilt and flip, and every numbered part is explained in English and Tamil.

## What's inside
- 51 boards: Arduino (Uno, Nano, Mega, Pro Mini, Digispark), ESP (8266, ESP‑01, D1 Mini, ESP32, C3, S3, CAM), Raspberry Pi (4, 5, Zero 2 W, Pico), STM32 Blue Pill, relay and motor drivers, power modules, radios (HC‑05, nRF24, LoRa, GPS, GSM, RFID, Ethernet), displays (OLED, 16×2 LCD, TM1637, MAX7219), sensors and utility modules
- Tap any point for: what it is, what it does, its role on that board, and how to identify and test it
- Uses, key specs and a beginner tip for each board
- Search box for boards and parts
- Parts library (84 components) and PCB basics
- Language switch: English, Tamil, or both, plus read-aloud
- My Workshop: step-by-step wiring guides (pins, jumper wire type, diagram, code) and your own boards with photos, stock count, location, price and project (PIN-protected editing)

## Run
```
npm install
WORKSHOP_PIN=your-pin PORT=3070 node server.js
```
- `index.html` is the whole front end; `server.js` serves it and the My Workshop API.
- Workshop data and photos are saved in `data/` (not in git). Back it up if you move servers.
- Photos are resized in the browser to max 1600 px before upload.
