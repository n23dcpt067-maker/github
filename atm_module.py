# atm_module.py

users = {
    "123456789": {"pin": "1234", "balance": 1000},
    "987654321": {"pin": "4321", "balance": 2000},
}

def verify_pin(account, pin):
    """Kiểm tra PIN"""
    if account in users and users[account]["pin"] == pin:
        return True
    return False

def withdraw(account, amount):
    """Rút tiền"""
    if account not in users:
        return False, "Tài khoản không tồn tại"

    if amount > users[account]["balance"]:
        return False, "Không đủ số dư"

    users[account]["balance"] -= amount
    return True, f"Rút tiền thành công, số dư còn lại {users[account]['balance']}"