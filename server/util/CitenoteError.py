from .helper.helper_main import bcolors


class CitenoteException(BaseException):
    """Common base class for all non-exit citenote exceptions."""

    def __init__(self, error, message) -> None:
        super().__init__()
        self.error = error
        self.message = message

    def __repr__(self) -> str:
        return f"CitenoteException(error: {self.error}, message: {self.message})"

    def __str__(self) -> str:
        return repr(self)

    def print_error(self):
        """Prints out warning message with help of bcolors class"""
        bcolors.print_warning(
            self.message,
            self.error + "()",
        )


class SameValueError(CitenoteException):
    """Similar value is provided"""

    def __init__(self):
        super().__init__("SameValueError", "Similar value is provided")


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


class PaperFoundError(CitenoteException):
    """Paper already exist."""

    def __init__(self) -> None:
        super().__init__("PaperFoundError", "Paper already exist in database.")


class PaperNotFoundError(CitenoteException):
    """Paper already exist."""

    def __init__(self) -> None:
        super().__init__("PaperNotFoundError", "Paper does not exist in database.")


class ManuscriptFoundError(CitenoteException):
    """Manuscript already exist."""

    def __init__(self):
        super().__init__("ManuscriptFoundError", "Manuscript already exists in database.")


class ManuscriptNotFoundError(CitenoteException):
    """Manuscript does not exist."""

    def __init__(self):
        super().__init__("ManuscriptNotFoundError", "Manuscript not found in database.")


if __name__ == "__main__":
    raise SystemExit
