
class BookUnavailableError(Exception):
    pass

class BookNotFoundError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class UserBorrowLimitExceeded(Exception):
    pass

class LoanNonExistent(Exception):
    pass

class BookAlreadyReturned(Exception):
    pass

class UnauthorizedReturnError(Exception):
    pass

class MaxLoansReachedError(Exception):
    pass

