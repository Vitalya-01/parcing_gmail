from enum import Enum


class OptionalSelectors(str, Enum):
    PHOTO = "//div[@class='aju']"
    PHOTO_MANY = "//div[@class='aCi']"
    IMAGE = "//div[@class='aCi']//img"
