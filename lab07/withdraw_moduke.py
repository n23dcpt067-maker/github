import mysql.connector
import hashlib


def verify_pin(card_no, pin):
    conn = mysql.connector.connect(
        user="root",
        password="123456",
        database="atm_demo"
    )
    cur = conn.cursor()
    cur.execute("SELECT pin_hash FROM cards WHERE card_no=%s", (card_no,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return False
 
    return row[0] == hashlib.sha256(pin.encode()).hexdigest()



def withdraw(card_no, amount):
    conn = mysql.connector.connect(
        user="root",
        password="123456",
        database="atm_demo"
    )
    cur = conn.cursor()

    try:
        conn.start_transaction()

    
        cur.execute("""
            SELECT a.account_id, a.balance 
            FROM accounts a
            JOIN cards c ON a.account_id = c.account_id
            WHERE c.card_no = %s
            FOR UPDATE
        """, (card_no,))
        row = cur.fetchone()

        if not row:
            raise Exception("Không tìm thấy tài khoản!")

        account_id, balance = row

        if balance < amount:
            raise Exception("Không đủ tiền trong tài khoản!")


        cur.execute(
            "UPDATE accounts SET balance = balance - %s WHERE account_id = %s",
            (amount, account_id)
        )


        cur.execute("""
            INSERT INTO transactions(account_id, card_no, atm_id, tx_type, amount, balance_after)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (account_id, card_no, 1, 'RÚT TIỀN', amount, balance - amount))


        conn.commit()
        print("💸 Rút tiền thành công!")
        print(f"Số dư còn lại: {balance - amount}")

    except Exception as e:
        conn.rollback()
        print("❌ Lỗi:", e)

    finally:
        conn.close()