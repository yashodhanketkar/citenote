class CitenoteException(BaseException):
    """Common base class for all non-exit citenote exceptions."""

    def __init__(self, error, message):
        self.message = message
        super().__init__(error)


class UsernameError(CitenoteException):
    """Incorrect username"""

    def __init__(self):
        super().__init__("UsernameError", "Invalid Credentials: Wrong username")


class PasswordError(CitenoteException):
    """Incorrect password"""

    def __init__(self):
        super().__init__("PasswordError", "Invalid Credentials: Wrong password")


class RoleError(CitenoteException):
    """Invalid user role"""

    def __init__(self):
        super().__init__("RoleError", "Invalid user role")


class UsernameNotInSession(CitenoteException):
    """Username not present in session"""

    def __init__(self):
        super().__init__("UsernameNotInSession", "Username not present in session")
