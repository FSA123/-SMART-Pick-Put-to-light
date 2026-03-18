import cv2
from ultralytics import YOLO
import serial
from db_manager import WarehouseDB

# 1. Inițializare
db = WarehouseDB()
model = YOLO('best.pt')
active_bin = None  # Variabilă de stare pentru a ști ce bin așteptăm să fie confirmat

try:
    ser = serial.Serial('COM3', 115200, timeout=0.05) # Timeout mic pentru a nu bloca video
except:
    ser = None

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # --- SECȚIUNEA 1: DETECȚIE ȘI COMANDĂ ---
    results = model.predict(frame, conf=0.7, verbose=False)
    
    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])
            target_bin = db.get_bin_by_class(class_id)

            if target_bin is not None and active_bin != target_bin:
                if ser:
                    ser.write(f"{target_bin}\n".encode())
                    active_bin = target_bin # Memorăm bin-ul activat
                print(f"Sistem: Activare Bin {target_bin} pentru Clasa {class_id}")

    # --- SECȚIUNEA 2: ASCULTARE FEEDBACK (AICI PUI CODUL) ---
    # Verificăm buffer-ul serial la fiecare frame
    if ser and ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line == "CONFIRMED":
                if active_bin is not None:
                    db.update_stock(active_bin, -1) # Actualizăm Baza de Date
                    print(f"LOG: Tranzacție reușită la Bin {active_bin}. Stoc actualizat.")
                    active_bin = None # Resetăm starea după confirmare
        except Exception as e:
            print(f"Eroare Serial: {e}")

    # --- SECȚIUNEA 3: UI ---
    cv2.imshow("Smart Pick-to-Light System", results[0].plot())
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
