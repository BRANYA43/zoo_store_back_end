class EmptyEmailError(Exception):
    def __init__(self, message='The given email must be set'):
        self.message = message
