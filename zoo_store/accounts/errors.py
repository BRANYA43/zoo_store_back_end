class EmptyEmailError(Exception):
    def __init__(self, message='Given email cannot be empty'):
        super().__init__(message)
