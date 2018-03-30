import requests
from lxml import html
from datetime import datetime

# SET THIS
#============================================================================================
USER = ''                               # Portal's account
USER_PW = ''                            # Portal's password
PartTimeId = ''                         # Ger from the url of the page of you clock in/out.
AttendWork = '睡覺Zz(´-ω-`*)'           # Job content

DayofWeek_Clock_Out = [0, 1, 2, 3, 4]   # 0 is Monday and 6 is Sunday
#============================================================================================

def main():
    Weekday = datetime.today().weekday()
    if Weekday not in DayofWeek_Clock_Out:
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

    SignOut = {
            'functionName': 'doSign',
            'idNo': '',
            'ParttimeUsuallyId': PartTimeId,
            'AttendWork': AttendWork
            }

    # Get token and idNo
    tree = html.fromstring(r.text)
    token = tree.xpath('/html/body/div[4]/div/input/@value')
    SignOut.update({'_token': token[0]})
    idNo = tree.xpath('//*[@id="idNo"]/@value')
    SignOut.update({'idNo': idNo[0]})

    # SignOut
    r = session.post('https://cis.ncu.edu.tw/HumanSys/student/stdSignIn_detail', data=SignOut)


if __name__ == '__main__':
    main()
