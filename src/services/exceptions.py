class TokenExpiredOrNotValid(Exception):
    message: str = "Token expired or not valid"


class AuthenticationError(Exception):
    message: str = "The password or username is not valid"


class AccessDeniedError(Exception):
    message: str = "Access Denied"
