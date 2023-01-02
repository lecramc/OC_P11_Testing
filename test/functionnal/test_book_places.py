

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service



service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get('http://127.0.0.1:5000/')
time.sleep(2)
driver.find_element(By.NAME, 'email').send_keys("john@simplylift.co")
driver.find_element(By.TAG_NAME,'button').click()
time.sleep(2)
driver.find_element(By.PARTIAL_LINK_TEXT,'Book').click()
time.sleep(2)
driver.find_element(By.NAME,'places').send_keys('4')
time.sleep(2)
driver.find_element(By.TAG_NAME,'button').click()
time.sleep(2)
message = driver.find_element(By.CLASS_NAME, 'message')
assert "Great-booking complete!" in message.text
driver.find_element(By.PARTIAL_LINK_TEXT,'Logout').click()
time.sleep(2)
driver.quit()