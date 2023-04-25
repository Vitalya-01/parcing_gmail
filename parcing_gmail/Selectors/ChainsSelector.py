from enum import Enum


class ChainsSelectors(str, Enum):
    CHAINS_UNREAD = "//tr[@class='zA zE']"  # get unread chains
    CHAINS_ALL = "//tr[contains(@class, 'zA')]"  # get all chains
    CHAIN_ID = ".//div[@class='y6']//span//span"
    CHAIN_DATE = ".//td[@class='xW xY ']//span"