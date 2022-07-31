CCID = ''

def get_CCID():
    print('cached CCID is', CCID)
    return CCID

def set_CCID(value):
    CCID = value
    success = True
    if CCID == '':
        success = False
    return success