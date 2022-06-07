import re

class Utils:

    EMAIL_PATTERN = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"

    @staticmethod
    def check_if_email(email):
        if re.fullmatch(Utils.EMAIL_PATTERN, email):
            return True
        else:
            return False
