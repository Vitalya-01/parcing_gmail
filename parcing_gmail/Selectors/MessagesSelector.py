from enum import Enum


class MessagesSelectors(str, Enum):
    MESSAGE = "//div[@class='G3 G2' or @class='G3 G2 afm']"
    MESSAGE_ID = ".//div[@class='adn ads']"
    MESSAGE_TEXT = ".//div[@class='ii gt' or class='ii gt adO']"
