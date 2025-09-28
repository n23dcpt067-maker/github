# selenium_test_login.py
import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# chỉnh đường dẫn HTML theo bạn
HTML_PATH = "file:///D:/lab/lab08/dangnhap.html"

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    # nếu muốn nhìn browser khi chạy, comment dòng headless
    # options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    driver.get(HTML_PATH)
    yield driver
    driver.quit()

def wait_msg_text(driver, timeout=3):
    el = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "msg")))
    return el.text.strip()

def test_login_success(driver):
    driver.refresh()
    WebDriverWait(driver,3).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys("123456")
    driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()
    time.sleep(0.5)
    msg = wait_msg_text(driver)
    assert "Đăng nhập thành công" in msg

def test_login_wrong(driver):
    driver.refresh()
    WebDriverWait(driver,3).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys("wrongpass")
    driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()
    time.sleep(0.5)
    msg = wait_msg_text(driver)
    assert "Sai Username hoặc Password" in msg

def test_login_empty_username(driver):
    driver.refresh()
    WebDriverWait(driver,3).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys("123456")
    driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()
    time.sleep(0.3)
    msg = wait_msg_text(driver)
    assert "Vui lòng nhập Username" in msg

def test_login_empty_password(driver):
    driver.refresh()
    WebDriverWait(driver,3).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()
    time.sleep(0.3)
    msg = wait_msg_text(driver)
    assert "Vui lòng nhập Password" in msg