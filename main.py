#!/user/bin/env
import json
from os.path import exists

import serial

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


def decode_signal(inp):
    split = [inp[i:i+2] for i in range(0, len(inp), 2)]
    if len(inp) > 0 and len(split) == 54:
        print(split)
        d = {}
        if split[1] == "33":
            d = {
                "33": {
                    "type": "BASKETBALL_with_individual_fouls",
                    "ball_possession": "HOME" if split[3] == "31" else "GUEST" if split[3] == "32" else None,
                    "timer_left": str(int(split[4])*10 + int(split[5])).zfill(2),
                    "timer_right": str(int(split[6])*10 + int(split[7])).zfill(2),
                    "points_home": str(int(split[8])*100 + int(split[9])*10 + int(split[10])).zfill(3),
                    "points_guest": str(int(split[11])*100 + int(split[12])*10 + int(split[13])).zfill(3),
                    "period": str(split[14]),
                    "team_fouls_home": str(split[15]),
                    "team_fouls_guest": str(split[16]),
                    "num_timeouts_home": str(split[17]),
                    "num_timeouts_guest": str(split[18]),
                    "horn": "ON" if split[19] == "31" else "OFF",
                    "timer_start_stop": "START" if split[20] == "30" else "STOP",
                    "timeout_timer": str(int(split[21])*100 + int(split[46])*10 + int(split[47])).zfill(3),
                    "timer_24_pure": str(int(split[48][1])*10 + int(split[49][1])).zfill(2),
                    "timer_24_dot": "ON" if split[49][0] == "4" else "OFF" if split[49][0] == "3" else None,
                    "timer_24_formatted": str((int(split[48][1])*10 + int(split[49][1]))/10).zfill(2) if split[49][0] == "4" else str(int(split[48][1])*10 + int(split[49][1])).zfill(2) if split[49][0] == "3" else None,
                    "horn_24": "ON" if split[50] == "31" else "OFF",
                    "timer_24_start_stop": "START" if split[51] == "30" else "STOP",
                    "display_24": "OFF" if split[52] == "24" else "ON",
                    "individual_fouls_player": {
                        "home": {
                            "1": str(int(split[22])),
                            "2": str(int(split[23])),
                            "3": str(int(split[24])),
                            "4": str(int(split[25])),
                            "5": str(int(split[26])),
                            "6": str(int(split[27])),
                            "7": str(int(split[28])),
                            "8": str(int(split[29])),
                            "9": str(int(split[30])),
                            "10": str(int(split[31])),
                            "11": str(int(split[32])),
                            "12": str(int(split[33])),
                        },
                        "guest": {
                            "1": str(int(split[34])),
                            "2": str(int(split[35])),
                            "3": str(int(split[36])),
                            "4": str(int(split[37])),
                            "5": str(int(split[38])),
                            "6": str(int(split[39])),
                            "7": str(int(split[40])),
                            "8": str(int(split[41])),
                            "9": str(int(split[42])),
                            "10": str(int(split[43])),
                            "11": str(int(split[44])),
                            "12": str(int(split[45])), }
                    }
                }}
        if exists("score_connect_data.json"):
            fread = open("score_connect_data.json", "r")
            file = json.load(fread)
            fread.close()
        else:
            file = {}
        fwrite = open("score_connect_data.json", "w")
        new = json.dumps(file | {"data": d, "input": inp}, indent=2)
        fwrite.write(new)
        fwrite.close()
        print(new)


while 1:
    msg = ser.readline().decode('utf-8').rstrip()
    decode_signal(msg)
