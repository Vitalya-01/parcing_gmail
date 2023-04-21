from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from Selectors.ChainsSelector import ChainsSelectors
from Selectors.NextPageSelector import NextPageSelectors
from Selectors.MessagesSelector import MessagesSelectors
from Selectors.OptionalSelector import OptionalSelectors
from dataBase.models.MailChains import MailChains
from dataBase.models.MailInterlocutors import MailInterlocutors
from dataBase.models.MailMessages import MailMessages
import time
import random
import dateparser


class Scraper:
    @classmethod
    def scrape(cls, driver, client_id, client_email_login):
        # Get letters
        chains = driver.find_elements(By.XPATH, ChainsSelectors.CHAINS)
        print(len(chains))

        # Get ids and texts from messages
        for chain in chains[-3:]:  # Change "chains[:2]" on "chains"
            chain_id = Scraper.get_chain_id(chain)
            print(chain_id)
            chain.click()
            # driver.implicitly_wait(1)
            time.sleep(random.randrange(1, 3))
            try:
                photo_many = chain.find_element(By.XPATH, OptionalSelectors.PHOTO_MANY)
                photo_many.click()
            except NoSuchElementException:
                pass
            driver.implicitly_wait(2)

            messages = driver.find_elements(By.XPATH, MessagesSelectors.MESSAGE)
            photo_click = driver.find_elements(By.XPATH, OptionalSelectors.PHOTO)
            driver.implicitly_wait(2)

            for photo in photo_click[:-1]:
                photo.click()
            time.sleep(random.randrange(1, 3))

            # Get interlocutor
            interlocutor = Scraper.get_chain_interlocutor(
                photo_click, client_email_login
            )
            print(*interlocutor)

            # Check interlocutor in db or create
            interlocutor_messages = MailInterlocutors.get_or_create_interlocutor(
                *interlocutor
            )

            # Get or create chain messages
            chain_messages = MailChains.get_or_create_chain(
                client_id, chain_id, interlocutor_messages.id
            )

            # Get data from messages
            for message in messages:
                # Get id one message
                message_id = Scraper.get_message_id(message)

                # Check that message not in chain messages
                if MailMessages.is_not_exist(message_id, chain_messages.id):
                    text = Scraper.get_text_email_message(message)
                    is_interlocutor = Scraper.check_is_interlocutor(
                        message, client_email_login
                    )

                    MailMessages.add_to_db(
                        chain_id=chain_messages.id,
                        message_id=message_id,
                        text=text,
                        is_interlocutor=is_interlocutor,
                    )
            driver.back()
            driver.implicitly_wait(4)

    @classmethod
    def get_chain_interlocutor(cls, photos, client_email):
        ntrlctr_first_name = ""
        ntrlctr_last_name = ""
        ntrlctr_email = ""
        ntrlctr_avatar_link = ""
        for photo in photos:
            interlocutor = photo.find_element(By.XPATH, OptionalSelectors.IMAGE)
            ntrlctr_email = interlocutor.get_attribute("data-hovercard-id")
            if ntrlctr_email != client_email:
                ntrlctr_name = interlocutor.get_attribute("data-name").split()
                ntrlctr_last_name = ""
                ntrlctr_avatar_link = interlocutor.get_attribute("src")
                if len(ntrlctr_name) == 0:
                    start = ntrlctr_email.find("@") + 1
                    end = ntrlctr_email.rfind(".")
                    ntrlctr_first_name = ntrlctr_email[start:end]
                else:
                    ntrlctr_first_name = ntrlctr_name[0]
                if len(ntrlctr_name) > 1:
                    ntrlctr_last_name = ntrlctr_name[1]
                break
        return ntrlctr_first_name, ntrlctr_last_name, ntrlctr_email, ntrlctr_avatar_link

    @classmethod
    def get_message_interlocutor(cls, message):
        photo = message.find_element(By.XPATH, OptionalSelectors.PHOTO)
        interlocutor = photo.find_element(By.XPATH, OptionalSelectors.IMAGE)

        ntrlctr_name = interlocutor.get_attribute("data-name").split()
        ntrlctr_last_name = ""
        ntrlctr_email = interlocutor.get_attribute("data-hovercard-id")
        ntrlctr_avatar_link = interlocutor.get_attribute("src")
        if len(ntrlctr_name) == 0:
            start = ntrlctr_email.find("@") + 1
            end = ntrlctr_email.rfind(".")
            ntrlctr_first_name = ntrlctr_email[start:end]
        else:
            ntrlctr_first_name = ntrlctr_name[0]
        if len(ntrlctr_name) > 1:
            ntrlctr_last_name = ntrlctr_name[1]

        return ntrlctr_first_name, ntrlctr_last_name, ntrlctr_email, ntrlctr_avatar_link

    @classmethod
    def get_chain_id(cls, chain):
        chain_id = chain.find_element(By.XPATH, ChainsSelectors.CHAIN_ID)
        return chain_id.get_attribute("data-thread-id")[10:]

    @classmethod
    def get_message_id(cls, message):
        div = message.find_element(By.XPATH, MessagesSelectors.MESSAGE_ID)
        return div.get_attribute("data-legacy-message-id")

    @classmethod
    def get_text_email_message(cls, message):
        text = message.find_element(By.XPATH, MessagesSelectors.MESSAGE_TEXT).text
        return text

    @classmethod
    def get_chain_date(cls, chain):
        data = (
            chain.find_element(By.XPATH, ChainsSelectors.CHAIN_DATE)
            .get_attribute("title")
            .split()
        )
        day = data[1]
        month = data[2][:-1]
        year = data[3]
        datetime = data[-1]

        data = " ".join((day, month, year, datetime))
        return dateparser.parse(data)

    @classmethod
    def next_page(cls, driver):
        next_button = driver.find_element(By.XPATH, NextPageSelectors.NEXT_PAGE)
        next_button_class = next_button.get_attribute("class")

        if next_button_class in (
            NextPageSelectors.NEXT_PAGE_REST,
            NextPageSelectors.NEXT_PAGE_CLICK,
        ):
            next_button.click()
            time.sleep(random.randrange(1, 3))
            return True
        if next_button_class == NextPageSelectors.NEXT_PAGE_SLEEP:
            return False

    @classmethod
    def check_is_interlocutor(cls, message, client_email):
        interlocutor = Scraper.get_message_interlocutor(message)
        return interlocutor[2] != client_email
