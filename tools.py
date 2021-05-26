#!/usr/bin/python3


import faker
import requests
import json
from time import sleep



class Mail:
    def __init__(self) -> None:
        self.session = requests.session()
        self.session.headers = {
            "User-Agent" : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'
        }

    def tokenParse(self, phone : str):
        self.email = faker.Faker().md5()[:6]
        self.password = faker.Faker().md5()[:8]
        self.phone = phone

        
        data = {
            'extended' : 'true',
            'more_password_strength' : '1',
            'context' : 'signup',
            'browser' : '{"screen":{"availWidth":"1440","availHeight":"900","width":"1440","height":"900","colorDepth":"24","pixelDepth":"24","top":"75","left":"1920","availTop":"75","availLeft":"1920","mozOrientation":"landscape-primary","onmozorientationchange":"inaccessible"},"navigator":{"doNotTrack":"1","maxTouchPoints":"0","oscpu":"Linux x86_64","vendor":"","vendorSub":"","productSub":"20100101","cookieEnabled":"true","buildID":"20181001000000","webdriver":"false","hardwareConcurrency":"4","appCodeName":"Mozilla","appName":"Netscape","appVersion":"5.0 (X11)","platform":"Linux x86_64","userAgent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0","product":"Gecko","language":"ru","onLine":"true"},"flash":{"version":"inaccessible"}}',
            'from' : 'navi',
            'sent_me_ads' : 'true',
            'sent_me_ads_common' : 'true',
            'name' : '{"first":"Alex","last":"Super"}',
            'birthday' : '{"day":3,"month":5,"year":2000}',
            'sex' : 'male', 
            'login' : self.email,
            'domain' : 'mail.ru',
            'password' : self.password,
            'phones' : '[{"phone":"' + phone + '","mobile":true}]',
            'htmlencoded' : 'false',
            'utm' : '{"source":"","medium":"","campaign":"","term":"","content":""}',
            'referrer' : 'https://mail.ru/'
        }
        request = self.session.post( 'https://account.mail.ru/api/v1/user/signup', data = data )
        data = json.loads(request.text)
        self.token = data["body"]["token"]
        print(f'Token parsed: {self.token}')
    def sendConfirmCode(self):
        data = {
            "reg_token" : '{"id":"' + self.token + '","transport":"phone","index":0,"target":"user/signup","format":"only_code"}',
            "email" : f'{self.email}@mail.ru',
            "callui" : "false",
            "from" : "navi",
            "lang" : "ru_RU",
            "htmlencoded" : "false",
            "utm" : '{"source":"","medium":"","campaign":"","term":"","content":""}',
            'referrer' : 'https://mail.ru/'
        }
        request = self.session.post( 'https://account.mail.ru/api/v1/tokens/send', data = data )
        print('Confirm code send...')
    def final(self, code : str): 
        data = {
            'email' : f'{self.email}@mail.ru',
            'redirect_uri' : 'https://mail.ru',
            'adblock' : 'true',
            'from' : 'navi',
            'reg_token' : '{"id":"' + self.token + '","value":"' + code + '"}',
            'htmlencoded' : 'false',
            'utm' : '{"source":"","medium":"","campaign":"","term":"","content":""}',
            'referrer' : 'https://mail.ru/'
        }

        request = self.session.post( 'https://account.mail.ru/api/v1/user/signup/confirm', data = data )
        print('Send final request...')
        if json.loads(request.text)['status'] != 200:
            print(f'Account not create: {self.email}@mail.ru')
        else:
            print(f'{"-"*15}\nAccount create!\n{"-"*15}\nLogin: {self.email}@mail.ru\nPwd: {self.password}')
            return {
                'login' : self.email,
                'password' : self.password
            }
        
class phone:
    def __init__(self, apiKey):
        self.apiKey = apiKey
    
    def getAllInfo(self):
        return json.loads(requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={self.apiKey}&action=getNumbersStatus&country=0').text)

    def getBalance(self):
        return requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={self.apiKey}&action=getBalance').text

    def getMailRuNomber(self):
        service = "ma"
        return requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={self.apiKey}&action=getNumber&service={service}').text

    def setStat(self, id : str, phone : str):
        return requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={self.apiKey}&action=setStatus&status=1&id={id}&forward={phone}')
        
    def getStat(self, id : str) -> str:
        return requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={self.apiKey}&action=getStatus&id={id}').text

def addAccount(login : str, password: str, fileName = 'accounts.txt') -> None:
    with open(fileName, 'a') as file:
        file.write(f'{login}:{password}\n')

