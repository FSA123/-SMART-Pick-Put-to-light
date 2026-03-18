# Smart Pick/Put-to-Light (SPPL) - Vision-Controlled Logistics
### Integrated Cyber-Physical System (CPS) for Electronic Component Management

## 1. Abstract
Acest proiect reprezintă o soluție de automatizare industrială de tip **Industry 4.0**, menită să optimizeze fluxurile logistice în depozitele de componente electronice. Sistemul fuzionează detecția de obiecte în timp real (**YOLO26**) cu feedback-ul hardware determinist (**ESP32 & Shift Registers**) și gestiunea datelor prin **SQLite**, eliminând eroarea umană și reducând latența operațională.

## 2. Arhitectura Sistemului
Sistemul funcționează într-o buclă închisă (**Closed-Loop Control**):
1.  **Percepție:** Camera preia fluxul video; modelul YOLO26 identifică componenta (Resistor, Capacitor, etc.).
2.  **Procesare:** Scriptul Python interoghează baza de date SQLite pentru a mapa clasa AI pe locația fizică (Bin ID).
3.  **Execuție:** Comanda este trimisă prin Serial (UART) către ESP32, care activează LED-ul corespunzător via Shift Register (74HC595).
4.  **Validare:** Senzorul ToF (VL53L0X) detectează acțiunea fizică și trimite confirmarea către Host pentru actualizarea automată a inventarului.



## 3. Stack Tehnologic
### Software
- **AI/CV:** Python 3.11, Ultralytics YOLO26 (Transformer-based architecture).
- **Database:** SQLite3 (RDBMS).
- **UI/Dashboard:** Streamlit (Web-based Industrial UI).
- **Communication:** PySerial (115200 baud).

### Hardware
- **MCU:** ESP32-WROOM-32.
- **Logic Expansion:** 74HC595 (8-bit Shift Register).
- **Sensors:** VL53L0X (Time-of-Flight Laser Sensor).
- **Optics:** 4K USB Camera / ESP32-CAM.
- **Mechanical:** 3D Printed PETG Diffusers for LED status indication.

## 4. Configurare Hardware (Pinout ESP32)
| Componentă | Pin ESP32 | Funcție |
| :--- | :--- | :--- |
| **74HC595 DS** | GPIO 23 | Serial Data Input |
| **74HC595 SHCP** | GPIO 18 | Shift Register Clock |
| **74HC595 STCP** | GPIO 5 | Latch Storage Clock |
| **I2C SDA** | GPIO 21 | ToF Data |
| **I2C SCL** | GPIO 22 | ToF Clock |
| **XSHUT (ToF)** | GPIO 14 | Sensor Shutdown/Enable |



## 5. Instalare și Utilizare

### Prerechizite
```bash
pip install -r requirements.txt
