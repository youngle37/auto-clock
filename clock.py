import requests
import argparse
import json
from lxml import html
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("action",choices=['signin', 'signout'])
parser.add_argument("-j", "--jobname", default="default_job", help="欲打卡工作名稱，定義在 config.json  (default: %(default)s)")
parser.add_argument("--config", default="config.json", help="default: %(default)s")
args = parser.parse_args()

def main():
    with open(args.config) as config_file:
        config = json.load(config_file)

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Host': 'portal.ncu.edu.tw',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    session = requests.session()
    login(session, headers, config['account'], config['password'])

    if args.action == "signin":
        signin(session, config["jobs"][args.jobname]["partTimeId"])
        pass
    elif args.action == "signout": 
        signout(session, config["jobs"][args.jobname]["partTimeId"], config["jobs"][args.jobname]["attendWork"])
        pass


    


def login(session, headers, account, password):
    payload = {
        'language' : 'CHINESE',
        'username' : account,
        'password' : password
    }

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
    return

def signin(session, partTimeId):
    SignIn = {
        'functionName': 'doSign',
        'idNo': '',
        'ParttimeUsuallyId': partTimeId,
        'AttendWork': ''
    }

    r = session.get('https://cis.ncu.edu.tw/HumanSys/student/stdSignIn/create?ParttimeUsuallyId='+partTimeId)

    # Get token
    tree = html.fromstring(r.text)
    token = tree.xpath('//input[@name="_token"]/@value')
    SignIn.update({'_token': token[0]})

    # SignIn
    r = session.post('https://cis.ncu.edu.tw/HumanSys/student/stdSignIn_detail', data=SignIn)
    return

def signout(session, partTimeId, attendWork):
    r = session.get('https://cis.ncu.edu.tw/HumanSys/student/stdSignIn/create?ParttimeUsuallyId='+partTimeId)

    SignOut = {
        'functionName': 'doSign',
        'idNo': '',
        'ParttimeUsuallyId': partTimeId,
        'AttendWork': attendWork
    }

    # Get token and idNo
    tree = html.fromstring(r.text)
    token = tree.xpath('//input[@name="_token"]/@value')
    SignOut.update({'_token': token[0]})
    idNo = tree.xpath('//*[@id="idNo"]/@value')
    SignOut.update({'idNo': idNo[0]})

    # SignOut
    r = session.post('https://cis.ncu.edu.tw/HumanSys/student/stdSignIn_detail', data=SignOut)
    return

if __name__ == '__main__':
    main()
