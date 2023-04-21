from enum import Enum


class ChainsSelectors(str, Enum):
    CHAINS = "//tr[@class='zA zE']"  # get unread chains
    CHAIN_ID = ".//span[@class='bqe']"
    CHAIN_DATE = ".//td[@class='xW xY ']//span"
