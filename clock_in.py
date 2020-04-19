import requests
from lxml import html
from datetime import datetime

import config

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
            'language' : 'CHINESE',
            'username' : config.CONFIG['account'],
            'password' : config.CONFIG['password']
            }

    session = requests.session()

    # IDK how to explain this section
    r = session.get('https://portal.ncu.edu.tw/login', headers=headers)

    # Get CSRF token from portal login page
    tree = html.fromstring(r.text)
    payload['_csrf'] = tree.forms[0].fields['_csrf']

    r = session.post('https://portal.ncu.edu.tw/login', data=payload)
    r = session.get('https://cis.ncu.edu.tw/HumanSys/login')    #This whill redirect to https://portal.ncu.edu.tw/leaving where portal will ask you weather you want to leave portal or not
    
    # Get CSRF token from portal redirect form
    tree = html.fromstring(r.text)
    token = tree.forms[0].fields['_csrf']

    r = session.post('https://portal.ncu.edu.tw/leaving', data={ "_csrf" : token })
    
    r = session.get('https://cis.ncu.edu.tw/HumanSys/student/stdSignIn/create?ParttimeUsuallyId='+config.CONFIG['PartTimeId'])

    SignIn = {
            'functionName': 'doSign',
            'idNo': '',
            'ParttimeUsuallyId': config.CONFIG['PartTimeId'],
            'AttendWork': ''
            }

    # Get token
    tree = html.fromstring(r.text)
    token = tree.xpath('//input[@name="_token"]/@value')
    SignIn.update({'_token': token[0]})

    # SignIn
    r = session.post('https://cis.ncu.edu.tw/HumanSys/student/stdSignIn_detail', data=SignIn)


if __name__ == '__main__':
    main()
