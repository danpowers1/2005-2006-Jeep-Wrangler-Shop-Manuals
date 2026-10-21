# Manual index

Map of every manual in this repository: what's in it and on which PDF page.

## How to use

1. Find the topic: `grep -i "crankshaft oil seal" index/pages.tsv` (columns: file, PDF page, printed page, running header, section path, figure captions, page_pdf).
2. Or browse a manual's outline and figure list in `index/<manual>.md`.
3. Show the page: `tools/page.sh <page_pdf>` fetches just that page (~30 KB) and renders a PNG. Every page is stored on its own as `pages/<manual>/pNNNN.pdf` + `.txt` (NNNN = PDF page), so you never need to download a whole manual. See README.md for the fast clone.

Use the 2006 manuals by default; check the 2005 manuals to cross-check.
The service manuals cover both the 2.4L and the 4.0L engine; check the running header (e.g. `ENGINE 4.0L`) before using a spec.

## Manuals

| Manual | File | PDF pages | Bookmarks | Figures | Index |
|---|---|---:|---:|---:|---|
| 2006 TJ/LJ Factory Service Manual | `2006 TJ Service Manual .pdf` | 1746 | 3535 | 2236 | [index/2006-service-manual.md](index/2006-service-manual.md) |
| 2006 TJ Powertrain Diagnostic Procedures | `2006-TJ-Powertrain.pdf` | 488 | 357 | 0 | [index/2006-powertrain-diagnostics.md](index/2006-powertrain-diagnostics.md) |
| 2006 TJ Body Diagnostic Procedures | `2006-TJ-Body.pdf` | 216 | 224 | 0 | [index/2006-body-diagnostics.md](index/2006-body-diagnostics.md) |
| 2006 TJ Chassis Diagnostic Procedures (ABS, axle lock) | `2006-TJ-Chassis.pdf` | 72 | 106 | 0 | [index/2006-chassis-diagnostics.md](index/2006-chassis-diagnostics.md) |
| 2006 TJ Parts List | `2006 TJ Parts List.pdf` | 409 | 340 | 0 | [index/2006-parts-list.md](index/2006-parts-list.md) |
| 2005 TJ/LJ Factory Service Manual | `2005 TJ Service Manual.pdf` | 1678 | 3444 | 2214 | [index/2005-service-manual.md](index/2005-service-manual.md) |
| 2005 TJ Powertrain Diagnostic Procedures | `2005 Jeep Wrangler TJ Powertrain Manual.PDF` | 502 | 370 | 0 | [index/2005-powertrain-diagnostics.md](index/2005-powertrain-diagnostics.md) |
| 2005 TJ Body Diagnostic Procedures | `2005 Jeep Wrangler TJ Body Manual.PDF` | 214 | 221 | 0 | [index/2005-body-diagnostics.md](index/2005-body-diagnostics.md) |
| 2005 TJ Chassis Diagnostic Procedures (ABS, axle lock) | `2005 Jeep Wrangler TJ Chassis Manual.PDF` | 72 | 107 | 0 | [index/2005-chassis-diagnostics.md](index/2005-chassis-diagnostics.md) |
| 2005 TJ Parts List | `2005 TJ Parts List.pdf` | 337 | 288 | 0 | [index/2005-parts-list.md](index/2005-parts-list.md) |
| 42RLE Automatic Transmission (FSM excerpt) | `42RLE-AUTOMATIC-TRANSMISSION.pdf` | 128 | 0 | 298 | [index/42rle-automatic-transmission.md](index/42rle-automatic-transmission.md) |
| NSG370 6-Speed Manual Transmission (FSM excerpt) | `NSG370-MANUAL-TRANSMISSION.pdf` | 36 | 0 | 99 | [index/nsg370-manual-transmission.md](index/nsg370-manual-transmission.md) |

The 2005 service manual is also stored as two halves (`2005_TJ_FSM_Part1_p1-799...` and `2005_TJ_FSM_Part2_p800-1678...`). Part 2 page = full-manual page − 799.

## 2006 service manual: groups

| Group | PDF pages |
|---|---|
| GROUP TAB LOCATOR | 1–2 |
| in-INTRODUCTION | 3–14 |
| 0-LUBRICATION & MAINTENANCE | 15–36 |
| 2-SUSPENSION | 37–56 |
| 3-DIFFERENTIAL & DRIVELINE | 57–230 |
| 4-VEHICLE QUICK REFERENCE | 231–252 |
| 5-BRAKES | 253–300 |
| 6-CLUTCH | 301–312 |
| 7-COOLING | 313–358 |
| 8a-AUDIO / VIDEO | 359–370 |
| 8b-CHIME / BUZZER | 371–376 |
| 8e-ELECTRONIC CONTROL MODULES | 377–394 |
| 8f-ENGINE SYSTEMS | 395–436 |
| 8g-HEATED SYSTEMS | 437–444 |
| 8h-HORN | 445–448 |
| 8i-IGNITION CONTROL | 449–468 |
| 8j-INSTRUMENT CLUSTER | 469–512 |
| 8l-LAMPS | 513–550 |
| 8n-POWER SYSTEMS | 551–554 |
| 8o-RESTRAINTS | 555–594 |
| 8p-SPEED CONTROL | 595–602 |
| 8q-VEHICLE THEFT SECURITY | 603–608 |
| 8r-WIPERS / WASHERS | 609–654 |
| 8w-WIRING | 655–960 |
| 9-ENGINE | 961–1096 |
| 11-EXHAUST SYSTEM | 1097–1106 |
| 13-FRAME & BUMPERS | 1107–1118 |
| 14-FUEL SYSTEM | 1119–1162 |
| 19-STEERING | 1163–1190 |
| 21-TRANSMISSION AND TRANSFER CASE | 1191–1436 |
| 22-TIRES / WHEELS | 1437–1452 |
| 23-BODY | 1453–1636 |
| 24-HEATING & AIR CONDITIONING | 1637–1720 |
| 25-EMISSIONS CONTROL | 1721–1740 |
| INDEX | 1741–1746 |

## 2005 service manual: groups

| Group | PDF pages |
|---|---|
| GROUP TAB LOCATOR | 1–2 |
| in-INTRODUCTION | 3–12 |
| 0-LUBRICATION & MAINTENANCE | 13–38 |
| 2-SUSPENSION | 39–58 |
| 3-DIFFERENTIAL & DRIVELINE | 59–218 |
| 5-BRAKES | 219–262 |
| 6-CLUTCH | 263–274 |
| 7-COOLING | 275–318 |
| 8a-AUDIO/VIDEO | 319–328 |
| 8b-CHIME/BUZZER | 329–334 |
| 8e-ELECTRONIC CONTROL MODULES | 335–352 |
| 8f-ENGINE SYSTEMS | 353–394 |
| 8g-HEATED SYSTEMS | 395–402 |
| 8h-HORN | 403–406 |
| 8i-IGNITION CONTROL | 407–426 |
| 8j-INSTRUMENT CLUSTER | 427–470 |
| 8l-LAMPS | 471–506 |
| 8n-POWER SYSTEMS | 507–510 |
| 8o-RESTRAINTS | 511–548 |
| 8p-SPEED CONTROL | 549–556 |
| 8q-VEHICLE THEFT SECURITY | 557–562 |
| 8r-WIPERS/WASHERS | 563–604 |
| 8w-WIRING | 605–920 |
| 9-ENGINE | 921–1052 |
| 11-EXHAUST SYSTEM | 1053–1064 |
| 13-FRAME & BUMPERS | 1065–1076 |
| 14-FUEL SYSTEM | 1077–1118 |
| 19-STEERING | 1119–1144 |
| 21-TRANSMISSION AND TRANSFER CASE | 1145–1378 |
| 22-TIRES/WHEELS | 1379–1392 |
| 23-BODY | 1393–1568 |
| 24-HEATING & AIR CONDITIONING | 1569–1652 |
| 25-EMISSIONS CONTROL | 1653–1672 |
| INDEX | 1673–1678 |
