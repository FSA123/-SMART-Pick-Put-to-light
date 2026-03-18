import streamlit as st
import sqlite3
import pandas as pd
import time

# Configurare pagină
st.set_page_config(page_title="Smart Warehouse Dashboard", layout="wide")

st.title("📊 Sistem Smart Pick-to-Light: Gestiune Inventar")
st.markdown("---")

def get_data():
    """Interogare bază de date SQLite."""
    conn = sqlite3.connect('smart_warehouse.db')
    query = "SELECT bin_id, component_name, yolo_class_id, current_stock, threshold FROM inventory"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Layout cu coloane pentru metrici globale
col1, col2, col3 = st.columns(3)

# Placeholder pentru tabel (pentru auto-refresh)
placeholder = st.empty()

while True:
    df = get_data()

    with placeholder.container():
        # Calcule metrici
        total_items = df['current_stock'].sum()
        low_stock_items = df[df['current_stock'] <= df['threshold']].shape[0]

        col1.metric("Total Componente", total_items)
        col2.metric("Piese sub Prag Critic", low_stock_items, delta_color="inverse")
        col3.metric("Status Sistem", "ONLINE", delta="Active")

        st.subheader("📋 Starea Raftului (8 Bins)")
        
        # Formatare vizuală: evidențiere rânduri cu stoc scăzut
        def highlight_low_stock(s):
            return ['background-color: #ff4b4b' if s.current_stock <= s.threshold else '' for _ in s]

        st.dataframe(df.style.apply(highlight_low_stock, axis=1), use_container_width=True)

        # Afișare alerte specifice
        if low_stock_items > 0:
            st.warning(f"⚠️ Atenție: Aveți {low_stock_items} tipuri de piese care necesită realimentare!")

    # Refresh la fiecare 2 secunde pentru a vedea actualizările în timp real
    time.sleep(2)
    st.rerun()