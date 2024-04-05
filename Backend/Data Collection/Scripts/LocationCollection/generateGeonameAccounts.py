from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

def create_account(driver, current_count, username, email_start, email_end, password):
    
    url = 'https://www.geonames.org/login'
    driver.get(url)
    time.sleep(2)

    username_inputs = driver.find_elements(by=By.NAME, value='username')
    email_input = driver.find_element(by=By.NAME, value='email')
    confirm_email_input = driver.find_element(by=By.NAME, value='confirmemail')
    password_inputs = driver.find_elements(by=By.NAME, value='password')
    confirm_password_input = driver.find_element(by=By.NAME, value='pass2')
    submit_button = driver.find_element(by=By.XPATH, value="//input[@type='submit' and @value='create account']")

    username_inputs[1].send_keys(f'{username}{current_count}')
    email_input.send_keys(f'{email_start}+{current_count}{email_end}')
    confirm_email_input.send_keys(f'{email_start}+{current_count}{email_end}')
    password_inputs[1].send_keys(password)
    confirm_password_input.send_keys(password)
    submit_button.click()
    time.sleep(5)
    return f"{username}{current_count}"

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))
    chrome_driver_path = os.path.join(parent_parent_dir, 'Driver', 'chromedriver.exe')

    driver = webdriver.Chrome(executable_path=chrome_driver_path)

    username = input("Enter a username: ")
    email = input("Enter an email address: ")
    password = input("Enter a password: ")
    count = int(input("Enter the number of accounts to create: "))
    skipCount = int(input("Enter the number of account numbers to skip: "))
    
    email_start = email.split('@')[0]
    email_end = '@' + email.split('@')[1]
    if skipCount != 0:
        skipCount += 1
    username_list = [] 

    for i in range(skipCount,count):
        account_username = create_account(driver, i, username, email_start, email_end, password)
        username_list.append(account_username)
    
    print("\033[92m" + str(username_list) + "\033[0m")
    print("\033[92mVerification emails have been sent to the email addresses provided. Please verify the accounts.\033[0m")
    driver.quit()

if __name__ == "__main__":
    main()
