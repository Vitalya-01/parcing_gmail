import undetected_chromedriver
import multiprocessing.pool
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from peewee import *
from urllib3.exceptions import MaxRetryError
from Selectors.SignUpSelector import SignUpSelectors
from links.Links import Links
from Scraper import Scraper
from dataBase.models.Clients import Clients

# from multiprocessing import cpu_count


class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)


class NoDaemonProcessPool(multiprocessing.pool.Pool):
    def Process(self, *args, **kwds):
        proc = super(NoDaemonProcessPool, self).Process(*args, **kwds)
        proc.__class__ = NoDaemonProcess

        return proc


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

    db = PostgresqlDatabase(
        database="postgres",
        user="root",
        password="root",
        port="5432",
        host="localhost",
        options="",
    )
    db.connect()
    path = "/home/yalg/PycharmProjects/parsing_letters_gmail/chromedriver"
    # Mail login
    try:
        driver = undetected_chromedriver.Chrome(driver_executable_path=path)

        driver.get(Links.STACKOVERFLOW)
        driver.implicitly_wait(4)
        driver.find_element(By.XPATH, SignUpSelectors.SIGN_UP).click()
        driver.implicitly_wait(4)
        login_box = driver.find_element(By.XPATH, SignUpSelectors.LOGIN_BOX)
        login_box.send_keys(client_email_login)
        driver.implicitly_wait(4)
        driver.find_element(By.XPATH, SignUpSelectors.LOGIN_NEXT).click()
        driver.implicitly_wait(4)
        # Check login
        try:
            password_box = driver.find_element(By.XPATH, SignUpSelectors.PASSWORD_BOX)
        except NoSuchElementException:
            print("Login not suitable")
            raise Exception
        driver.implicitly_wait(4)
        password_box.send_keys(client_email_password)
        driver.implicitly_wait(4)
        driver.find_element(By.XPATH, SignUpSelectors.PASSWORD_NEXT).click()
        driver.implicitly_wait(4)
        # Check password
        try:
            driver.find_element(By.XPATH, SignUpSelectors.PASSWORD_ERROR)
            print("Password not suitable")
            raise Exception
        except NoSuchElementException:
            pass
        driver.get(Links.GMAIL)
        driver.implicitly_wait(4)
        print("Login Successful...!!")
    except MaxRetryError as error:
        print(error)
    finally:
        Scraper.scrape(driver, client_id, client_email_login)
        while Scraper.next_page(driver):
            Scraper.scrape(driver, client_id, client_email_login)
        driver.close()
        driver.quit()
    db.close()


def main():
    process_count = int(input("enter count processes:"))
    # process_count = cpu_count()
    print(f"Count processes {process_count}")
    # try:
    db = PostgresqlDatabase(
        database="postgres",
        user="root",
        password="root",
        port="5432",
        host="localhost",
        options="",
    )
    db.connect()
    # Get all clients
    clients = Clients.select()
    pool = NoDaemonProcessPool(process_count)
    pool.map(enter_gmail, clients)

    pool.close()
    pool.join()
    db.close()


if __name__ == "__main__":
    main()
