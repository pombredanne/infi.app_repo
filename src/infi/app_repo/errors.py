from infi.rpc.errors import RPCUserException


class AppRepoBaseException(RPCUserException):
    pass


class FileAlreadyExists(AppRepoBaseException):
    pass


class FileRejected(AppRepoBaseException):
    pass


class FilenameParsingFailed(FileRejected):
    pass


class FileProcessingFailed(FileRejected):
    pass


class FileNeglectedByIndexers(FileRejected):
    pass


class NoCredentialsException(Exception):
    pass
