import cv2
from ultralytics import YOLO
import serial
import time

# --- CONFIG ---
SERIAL_PORT = 'COM3' 
model = YOLO('best.pt')

# Define our order exactly as you requested
CLASSES_ORDER = [
    "Resistor", "Capacitor", "Button", "Inductor", 
    "Transistor", "Transformer", "Diode", "Potentiometer"
]

try:
    esp32 = serial.Serial(SERIAL_PORT, 115200, timeout=0.1)
    time.sleep(2)
except:
    print("Check your ESP32 connection!")
    exit()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret: break

    results = model(frame, conf=0.5, verbose=False)
    
    # Start with a "clean slate" (all LEDs off)
    bitmask = 0
    
    # Look at every object the AI found
    for box in results[0].boxes:
        class_id = int(box.cls)
        class_name = model.names[class_id] # e.g., "Resistor"
        
        if class_name in CLASSES_ORDER:
            # Find which LED this component belongs to
            index = CLASSES_ORDER.index(class_name)
            # Flip that specific bit to 1
            bitmask |= (1 << index)

    # Send the final 8-bit number to ESP32
    # We send it as a raw byte for speed
    esp32.write(bytes([bitmask]))

    # Display UI
    annotated_frame = results[0].plot()
    cv2.imshow("Electronic Component Detector", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()