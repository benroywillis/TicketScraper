from selenium import webdriver
import time

DRIVER_PATH = "/bin/google-chrome"
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get("https://google.com")
time.sleep(1)
driver.quit()
