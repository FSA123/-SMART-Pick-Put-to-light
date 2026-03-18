import sqlite3

def initialize_database():
    # Conectare la baza de date (va crea fișierul 'smart_warehouse.db')
    conn = sqlite3.connect('smart_warehouse.db')
    cursor = conn.cursor()

    # Crearea tabelei cu constrângeri de integritate
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            bin_id INTEGER PRIMARY KEY,
            yolo_class_id INTEGER UNIQUE,
            component_name TEXT NOT NULL,
            current_stock INTEGER DEFAULT 0,
            threshold INTEGER DEFAULT 10
        )
    ''')

    # Popularea inițială (Exemplu pentru primele 3 LED-uri)
    # Mapăm: Class 0 -> Bin 0, Class 1 -> Bin 1, etc.
    initial_data = [
        (0, 0, 'Resistor 1k', 100, 20),
        (1, 1, 'Capacitor 10uF', 50, 10),
        (2, 2, 'LED Red 5mm', 200, 30)
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO inventory (bin_id, yolo_class_id, component_name, current_stock, threshold)
        VALUES (?, ?, ?, ?, ?)
    ''', initial_data)

    conn.commit()
    conn.close()
    print("Baza de date a fost inițializată cu succes.")

if __name__ == "__main__":
    initialize_database()