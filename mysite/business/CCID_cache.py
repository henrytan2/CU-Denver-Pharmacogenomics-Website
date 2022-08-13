CCID = ''
positions = ''
sequence_length = ''
pdb = ''

def set_PDB(value):
    PDB = value
    success = True
    if PDB == '':
        success = False
    return success


def set_CCID(value):
    CCID = value
    success = True
    if CCID == '':
        success = False
    return success

def get_CCID():
    print('cached CCID in CCID_cache is', CCID)
    return CCID


def set_positions(value):
    positions = value
    success = True
    if positions == '':
        success = False
    return success

def get_positions():
    print('cached positions in CCID_cache are', positions)
    return positions


def set_length(value):
    sequence_length = value
    success = True
    if sequence_length == '':
        success = False
    return success

def get_length():
    print('cached sequence_length in CCID_cache is', sequence_length)
    return sequence_length
