import sys
import os

SWITCH_ID = 0
SWITCH_TYPE = "BLE"
QUANTITY_SWITCH = 4
COLOR = ["z", "z", "z", "z"]
STATUS = [0, 0, 0, 0]
SWITCH_1 = []
SWITCH_2 = []
SWITCH_3 = []
SWITCH_4 = []


def reset():
    global COLOR, STATUS, SWITCH_4, SWITCH_3, SWITCH_2, SWITCH_1, QUANTITY_SWITCH

    COLOR = ['z' for x in range(0, QUANTITY_SWITCH, 1)]
    STATUS = [0 for x in range(0, QUANTITY_SWITCH, 1)]
    SWITCH_1 = []
    SWITCH_2 = []
    SWITCH_3 = []
    SWITCH_4 = []


def set_quantity_switch(quantity):
    global QUANTITY_SWITCH
    QUANTITY_SWITCH = quantity


def set_type_switch(type):
    global SWITCH_TYPE
    SWITCH_TYPE = type


def get_quantity_switch():
    global QUANTITY_SWITCH
    return QUANTITY_SWITCH


def get_type_switch():
    global SWITCH_TYPE
    return SWITCH_TYPE

# ok
def add_status(order, status=0):
    _status_list = []
    if order == 0:
        global SWITCH_1
        _status_list = SWITCH_1
    elif order == 1:
        global SWITCH_2
        _status_list = SWITCH_2
    elif order == 2:
        global SWITCH_3
        _status_list = SWITCH_3
    else:
        global SWITCH_4
        _status_list = SWITCH_4

    if len(_status_list) == 0:
        _status_list.append(status)
    elif _status_list[-1] != status:
        _status_list.append(status)

    global STATUS
    STATUS[order] = status
    print("status", _status_list)

    return _status_list

# ok
def add_color(order, color):
    global COLOR
    if color == 0:
        COLOR[order] = "red"
    elif color == 1:
        COLOR[order] = "green"
    elif color == 2:
        COLOR[order] = "blue"
    else:
        COLOR[order] = "z"
    print("color", COLOR[order])


def get_color():
    global COLOR
    return COLOR


def get_status():
    global STATUS
    return STATUS


def get_blink():
    global SWITCH_1, SWITCH_2, SWITCH_3, SWITCH_4, QUANTITY_SWITCH
    if QUANTITY_SWITCH == 4:
        return [_calculator_blink(SWITCH_1), _calculator_blink(SWITCH_2), _calculator_blink(SWITCH_3), _calculator_blink(SWITCH_4)]
    elif QUANTITY_SWITCH == 3:
        return [_calculator_blink(SWITCH_1), _calculator_blink(SWITCH_2), _calculator_blink(SWITCH_3)]
    elif QUANTITY_SWITCH == 2:
        return [_calculator_blink(SWITCH_1), _calculator_blink(SWITCH_2)]
    elif QUANTITY_SWITCH == 1:
        return [_calculator_blink(SWITCH_1)]
    return []


def clean_blink():
    global SWITCH_1, SWITCH_2, SWITCH_3, SWITCH_4, QUANTITY_SWITCH
    if QUANTITY_SWITCH == 4:
        SWITCH_1 = list()
        SWITCH_2 = list()
        SWITCH_3 = list()
        SWITCH_4 = list()
    elif QUANTITY_SWITCH == 3:
        SWITCH_1 = list()
        SWITCH_2 = list()
        SWITCH_3 = list()
    elif QUANTITY_SWITCH == 2:
        SWITCH_1 = list()
        SWITCH_2 = list()
    elif QUANTITY_SWITCH == 1:
        SWITCH_1 = list()


def _calculator_blink(buffer):

    blink = 0
    for i in range(0, len(buffer), 1):
        if i == len(buffer) - 1:
            break
        if buffer[i] == 1 and buffer[i+1] == 2:
            blink += 1
    return blink


def get_switch_id():
    global SWITCH_ID
    return SWITCH_ID


def get1():
    global SWITCH_1, SWITCH_2, SWITCH_3, SWITCH_4
    SWITCH_1 = list()
    SWITCH_2 = list()
    SWITCH_3 = list()
    SWITCH_4 = list()

