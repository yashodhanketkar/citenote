class CitenoteException(BaseException):
    """Common base class for all non-exit citenote exceptions."""

    def __init__(self, error, message) -> None:
        super().__init__()
        self.error = error
        self.message = message


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


class UsernameInSession(CitenoteException):
    """Username not present in session"""

    def __init__(self):
        super().__init__("UsernameInSession", "Username is present in session")


if __name__ == "__main__":
    try:
        raise UsernameInSession

    except UsernameInSession as err:
        print(err.message, err.error)
        print(err)

    except Exception as err:
        print(err)
