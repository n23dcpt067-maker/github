# test_withdraw.py
import pytest
import atm_module

def test_verify_pin_correct():
    assert atm_module.verify_pin("123456789", "1234") is True

def test_verify_pin_incorrect():
    assert atm_module.verify_pin("123456789", "0000") is False

def test_withdraw_success():
    # reset số dư để test
    atm_module.users["123456789"]["balance"] = 1000
    success, msg = atm_module.withdraw("123456789", 500)
    assert success is True
    assert "Rút tiền thành công" in msg
    assert "số dư còn lại 500" in msg

def test_withdraw_insufficient_balance():
    # reset số dư để test
    atm_module.users["123456789"]["balance"] = 300
    success, msg = atm_module.withdraw("123456789", 1000)
    assert success is False
    assert "Không đủ số dư" in msg