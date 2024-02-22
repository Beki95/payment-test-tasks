class NoBalanceError(Exception):
    message: str = "Lack of funds on the balance sheet"


class InsufficientFundsError(Exception):
    message: str = "Insufficient funds on the balance sheet"
