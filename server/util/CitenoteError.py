class UsernameError(Exception):
    def __init__(self):
        self.message = "Invalid Credentials: Wrong username"
        super().__init__("UsernameError")


class PasswordError(Exception):
    def __init__(self):
        self.message = "Invalid Credentials: Wrong password"
        super().__init__("PasswordError")


class RoleError(Exception):
    def __init__(self):
        self.message = "Invalid user role"
        super().__init__("RoleError")
