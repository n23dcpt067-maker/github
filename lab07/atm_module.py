import mysql.connector
import hashlib

def verify_pin(card_no, pin):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",      
        database="atm_demo"
    )
    cur = conn.cursor()
    cur.execute("SELECT pin_hash FROM cards WHERE card_no=%s", (card_no,))
    row = cur.fetchone()
    conn.close()

    if row:
        pin_hash = hashlib.sha256(pin.encode()).hexdigest()
        return row[0] == pin_hash
    return False

def withdraw(card_no, amount):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",     
        database="atm_demo"
    )
    cur = conn.cursor()
    try:
        conn.start_transaction()

       
        cur.execute("""
            SELECT accounts.account_id, balance 
            FROM accounts 
            JOIN cards USING(account_id) 
            WHERE card_no=%s FOR UPDATE
        """, (card_no,))
        row = cur.fetchone()

        if not row:
            raise Exception("❌ Không tìm thấy tài khoản")

        account_id, balance = row

        if balance < amount:
            raise Exception("❌ Số dư không đủ")

        cur.execute(
            "UPDATE accounts SET balance = balance - %s WHERE account_id = %s",
            (amount, account_id)
        )

        cur.execute("""
            INSERT INTO transactions(account_id, card_no, atm_id, tx_type, amount, balance_after)
            VALUES (%s, %s, 1, 'RÚT TIỀN', %s, %s)
        """, (account_id, card_no, amount, balance - amount))

        conn.commit()
        print("✅ Rút tiền thành công, số dư còn lại:", balance - amount)

    except Exception as e:
        conn.rollback()
        print("❌ Lỗi:", e)
    finally:
        conn.close()