from enum import Enum


class OptionalSelectors(str, Enum):
    PHOTO = "//div[@class='aju']"
    PHOTO_MANY = "//span[@class='adx']"
    IMAGE = "//span[@class='adx']//img"
