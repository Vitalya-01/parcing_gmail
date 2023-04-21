from enum import Enum


class Links(str, Enum):
    STACKOVERFLOW = (
        "https://stackoverflow.com/users/"
        "signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent"
    )
    GMAIL = "https://www.gmail.com/"
