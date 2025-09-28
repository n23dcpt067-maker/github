from atm_module import verify_pin, withdraw


card_no = "1234567890"   
pin = "1234"             
amount = 500000          
if verify_pin(card_no, pin):
    print("✅ PIN đúng, tiến hành rút tiền...")
    withdraw(card_no, amount)
else:
    print("❌ Sai PIN, không thể rút tiền")