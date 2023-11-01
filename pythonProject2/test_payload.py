# Dữ liệu từ host/camera
host_data = {
    "switch": 0,
    "cmd": "get",
    "event": "status",
}

# Dữ liệu từ client/camera
client_data = {
    "switch": 0,
    "blink": [3, 3, 3, 3],
    "status": [0, 1, 1, 0],
    "color": [0, 1, 2, 1]
}

# Xử lý dữ liệu
if host_data["cmd"] == "get":
    if host_data["event"] == "blink":
        switch_number = host_data["switch"]
        blink_number = client_data["blink"]
        print(f"{switch_number} : {blink_number}")
    elif host_data["event"] == "status":
        switch_number = host_data["switch"]
        status = client_data["status"]
        print(f"{switch_number}: {status}")
    elif host_data["event"] == "color":
        switch_number = host_data["switch"]
        color = client_data["color"][switch_number]
        print(f"Color of switch {switch_number}: {color}")
else:
    print("Invalid command")
