import requests
from lxml import html
from datetime import datetime
import random
import config
import time
def main():
    Weekday = datetime.today().weekday()
    if Weekday not in config.CONFIG['DayofWeek_Clock']:
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
            'j_username': config.CONFIG['account'],
            'j_password': config.CONFIG['password']
            }

    session = requests.session()

    # IDK how to explain this section
    r = session.get('https://portal.ncu.edu.tw/login', headers=headers)
    r = session.post('https://portal.ncu.edu.tw/j_spring_security_check', data=payload)
    r = session.get('https://cis.ncu.edu.tw/HumanSys/login?netid-user='+config.CONFIG['account'])
    r = session.get('https://cis.ncu.edu.tw/HumanSys/student/stdSignIn/create?ParttimeUsuallyId='+config.CONFIG['PartTimeId'])

    SignOut = {
            'functionName': 'doSign',
            'idNo': '',
            'ParttimeUsuallyId': config.CONFIG['PartTimeId'],
            'AttendWork': config.CONFIG['AttendWork'][random.randint(0,len(config.CONFIG['AttendWork'])-1)]
            }
    # Get token and idNo
    tree = html.fromstring(r.text)
    token = tree.xpath('//input[@name="_token"]/@value')
    SignOut.update({'_token': token[0]})
    idNo = tree.xpath('//*[@id="idNo"]/@value')
    SignOut.update({'idNo': idNo[0]})

    # SignOut
    r = session.post('https://cis.ncu.edu.tw/HumanSys/student/stdSignIn_detail', data=SignOut)


if __name__ == '__main__':
    #隨機延遲執行0~5分鐘
    delay_time=random.randint(0,config.CONFIG['Random_delay_range'])*60
    time.sleep(delay_time)
    main()