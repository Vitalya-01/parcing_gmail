import undetected_chromedriver as uc
from peewee import *
from dataBase.db import get_db_instance
from dataBase.manipulation import create_tables, add_client
from links.Links import Links
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from urllib3.exceptions import MaxRetryError
from Selectors.SignUpSelector import SignUpSelectors
from scraper import Scraper

wait_time = 6


def enter_login(driver, login):
    driver.implicitly_wait(wait_time)
    login_box = driver.find_element(By.XPATH, SignUpSelectors.LOGIN_BOX)
    login_box.send_keys(login)
    driver.implicitly_wait(wait_time)
    driver.find_element(By.XPATH, SignUpSelectors.LOGIN_NEXT).click()
    driver.implicitly_wait(wait_time)


def enter_password(driver, pass_box, password):
    driver.implicitly_wait(wait_time)
    pass_box.send_keys(password)
    driver.implicitly_wait(wait_time)
    driver.find_element(By.XPATH, SignUpSelectors.PASSWORD_NEXT).click()
    driver.implicitly_wait(wait_time)


def enter_gmail(client):
    client_id = client.id
    client_first_name = client.first_name
    client_last_name = client.last_name
    client_email_login = client.email_login
    client_email_password = client.email_password

    print(
        client_id,
        client_first_name,
        client_last_name,
        client_email_login,
        client_email_password,
    )
    db = get_db_instance()
    path = "../parcing_gmail/drivers/chrome/chromedriver112.exe"
    # Mail login
    try:
        driver = uc.Chrome(driver_executable_path=path)
        driver.get(Links.STACKOVERFLOW)
        driver.implicitly_wait(wait_time)
        driver.find_element(By.XPATH, SignUpSelectors.SIGN_UP).click()
        enter_login(driver, client_email_login)

        # Confirmation to enter
        try:
            while 1:
                confirmation = driver.find_element(By.XPATH, SignUpSelectors.CONFIRMATION_BOX)
                driver.execute_script("arguments[0].click();", confirmation)
                print('Confirmation complete!')
                driver.implicitly_wait(wait_time)

                enter_login(driver, client_email_login)
        except NoSuchElementException:
            pass

        driver.implicitly_wait(wait_time)
        # Check login
        try:
            password_box = driver.find_element(By.XPATH, SignUpSelectors.PASSWORD_BOX)
        except NoSuchElementException:
            print("Login not suitable")
            raise NoSuchElementException
        enter_password(driver, password_box, client_email_password)
        # Check password
        try:
            driver.find_element(By.XPATH, SignUpSelectors.PASSWORD_ERROR)
            print("Password not suitable")
            raise Exception
        except NoSuchElementException:
            pass
        driver.get(Links.GMAIL)
        driver.implicitly_wait(wait_time)
        print("Login Successful...!!")
    except MaxRetryError as error:
        pass
    finally:
        Scraper.scrape(driver, client_id, client_email_login)
        # while Scraper.next_page(driver):
        #     Scraper.scrape(driver, client_id, client_email_login)
        driver.close()
        driver.quit()
    db.close()


def main():
    # Enter necessary information
    # fisrt_name = input("Enter first name:")
    # last_name = input("Enter last name:")
    # email = input("Enter email:")
    # password = input("Enter password:")

    test = {'first_name': 'vit',
            'last_name': 'buh',
            'email': 'vitalikbuhtiarov@gmail.com',
            'password': 'H3cZ81rQ'}

    # Create db and tables
    create_tables()
    client = add_client(test['first_name'], test['last_name'], test['email'], test['password'])
    enter_gmail(client)

if __name__ == '__main__':
    main()
