'''
account:
    account on Portal
password:
    password on Portal
PartTimeId:
    Get from the url of the page you clock in/out.
AttendWork:
    Job content. You can set multiple options,the system will randomly choose.
DayofWeek_Clock_In:
    0 is Monday and 6 is Sunday
Random_delay_range:
    The unit is minutes. This is the time the program will be delayed.
    Make you auto clock-in and clock-out more like human.
'''
AttendWork=[
"工作",
"看論文",
"學習"
]
CONFIG = {
    'account': '',
    'password': '',
    'PartTimeId': '',
    'AttendWork':AttendWork,
    'DayofWeek_Clock': [0, 1, 2, 3, 4],
    'Random_delay_range': 5
}
