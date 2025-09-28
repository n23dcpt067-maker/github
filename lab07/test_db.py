import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="atm_demo"
    )
    print("✅ Kết nối MySQL thành công!")
    conn.close()
except Exception as e:
    print("❌ Lỗi kết nối:", e)