class ValidationError(Exception):

    def __init__(self, message: str = None, status_code: int = 400, result=None):
        self.__message = message
        self.__result = result
        self.__status_code = status_code
        super().__init__(self.__message)

    @property
    def result(self):
        return self.__result

    @property
    def message(self):
        return self.__message

    @property
    def status_code(self):
        return self.__status_code

