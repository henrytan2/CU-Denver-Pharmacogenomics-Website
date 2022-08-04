CCID = ''
positions = ''

def get_CCID():
    print('cached CCID is', CCID)
    return CCID

def set_CCID(value):
    CCID = value
    success = True
    if CCID == '':
        success = False
    return success

def get_positions():
    print('cached positions are', positions)
    return positions

def set_positions(value):
    positions = value
    success = True
    if positions == '':
        success = False
    return success