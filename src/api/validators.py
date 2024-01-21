from functions import read_from_db_lol


def command_exists(command):
    read_from_db_lol()
    if command in read_from_db_lol().keys():
        return True
    return False


def db_exists():
    return isinstance(read_from_db_lol(), dict)