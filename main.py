import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from private_info import *
import smtplib
from email.message import EmailMessage

CHECK_INTERVAL = 1140 #19 minutes

driver = webdriver.Chrome()

def login():
    driver.get("https://my.fiu.edu/")
    time.sleep(5)
    driver.find_element(By.LINK_TEXT, "Login to MyFIU").click()
    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.NAME, "submit").click()
    driver.find_element(By.ID, "rememberLabel").click()
    driver.find_element(By.ID, "push").click()

    print("Waiting for DUO 2FA... Complete manually.")
    time.sleep(30)

def check_class():
    print("Checking for class")
    driver.get(SHOPPING_CART_PAGE)
    time.sleep(5)
    driver.find_element(By.XPATH, "//span[@title='Enrollment']/../../..").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//span[@title='Shopping Cart']/../../..").click()
    time.sleep(5)
    class_element = driver.find_element(By.XPATH, "//span[starts-with(text(),'COP 4610')]/ancestor::tr")
    status = class_element.find_element(By.XPATH, "//td[2]").text

    return not "Closed" in status

def send_notification():
    msg = EmailMessage()
    msg.set_content(f"Your class has an open seat! Enroll now")
    msg['Subject'] = f'Class {CLASS_CODE} is open'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

def main():
    login()
    while True:
        try:
            if check_class():
                print("Seat found!")
                send_notification()
                break
            else:
                print(f"{CLASS_CODE} is still full. Checking again in {CHECK_INTERVAL//60} minutes")
        except Exception as e:
            print("Error during check: ", e)
        time.sleep(CHECK_INTERVAL)

    driver.quit()

if __name__ == "__main__":
    main()