import requests
from lxml import html
from datetime import datetime

# SET THIS
#==============================================================================================
USER = ''                               # Portal's account
USER_PW = ''                            # Portal's password
PartTimeId = ''                         # Get from the url of the page of you clock in/out.

DayofWeek_Clock_In = [0, 1, 2, 3, 4]    # 0 is Monday and 6 is Sunday
#==============================================================================================

def main():
    Weekday = datetime.today().weekday()
    if Weekday not in DayofWeek_Clock_In:
        exit()

    headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Host': 'portal.ncu.edu.tw',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
            }

    payload = {
            'j_username': USER,
            'j_password': USER_PW
            }

    session = requests.session()

    r = session.get('https://portal.ncu.edu.tw/login', headers=headers)
    r = session.post('https://portal.ncu.edu.tw/j_spring_security_check', data=payload)
    r = session.get('https://cis.ncu.edu.tw/HumanSys/login?netid-user='+USER)
    r = session.get('https://cis.ncu.edu.tw/HumanSys/student/stdSignIn/create?ParttimeUsuallyId='+PartTimeId)

    SignIn = {
            'functionName': 'doSign',
            'idNo': '',
            'ParttimeUsuallyId': PartTimeId,
            'AttendWork': ''
            }

    # Get token
    tree = html.fromstring(r.text)
    token = tree.xpath('/html/body/div[4]/div/input/@value')
    SignIn.update({'_token': token[0]})

    # SignIn
    r = session.post('https://cis.ncu.edu.tw/HumanSys/student/stdSignIn_detail', data=SignIn)


if __name__ == '__main__':
    main()
