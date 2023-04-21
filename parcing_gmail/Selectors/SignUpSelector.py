from enum import Enum


class SignUpSelectors(str, Enum):
    SIGN_UP = '//*[@id="openid-buttons"]/button[1]'
    LOGIN_BOX = '//*[@id ="identifierId"]'
    LOGIN_NEXT = '//*[@id ="identifierNext"]'
    PASSWORD_BOX = '//*[@id ="password"]/div[1]/div / div[1]/input'
    PASSWORD_NEXT = '//*[@id ="passwordNext"]'
    PASSWORD_ERROR = "//div[@class='EjBTad']"
