# HACKCLUB‑Hackpad

A compact macropad project including PCB, schematic, and a fitted case inspired by Serial Experiments Lain.

**Overview**

This repository contains the design files, a simple KMK firmware, and placeholder screenshots for a small 8-key macropad with rotary encoder, underglow LEDs, and a 0.91" OLED.

**Screenshots**

![Overall design](docs/images/overall.png)

![Schematic](pcb/schematic.png)

![PCB layout](pcb/PCB.png)

![Case / exploded view](cad/case.png)

**Bill of Materials (BOM)**
- Seeed XIAO RP2040 — x1
- Through-hole 1N4148 diodes — x8
- MX-style mechanical switches — x8
- EC11 rotary encoder — x1
- Blank DSA keycaps — x8
- SK6812 MINI-E LEDs — x8
- 0.91 inch OLED display — x1
- M3 x 16 mm screws & M3 heat-set inserts — x4

**Repository layout**
- `cad/` — CAD files and case models
- `pcb/` — KiCad schematic and PCB files
- `firmware/` — KMK firmware and `keymap.py`
- `docs/images/` — project screenshots used by this README


