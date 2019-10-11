def switch_test_item( item):
    switcher = {
        "CPU": 0,
        "Memory": 1,
        "BIOSVER": 2,
        "FAN": 3,
        "BIOSSETUP": 4,
    }
    return switcher.get(item, "nothing")













switch = switch_test_item( "Memory")
print(switch)