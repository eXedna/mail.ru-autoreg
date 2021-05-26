#!/usr/bin/python3

from tools import Mail, phone, addAccount
from time import sleep

global apiKey
apiKey = input('введите apiKey с sms-activate.ru: ')

def start():
    mail = Mail()
    Phone = phone(apiKey)
    print('start() > Get phone nomber...')
    data = Phone.getMailRuNomber()
    phoneId = data.split(':')[1]
    phoneNomber = data.split(':')[2]
    print(f'start() > Phone recieved: {phoneNomber}')
    mail.tokenParse(phoneNomber)
    mail.sendConfirmCode()
    Phone.setStat(phoneId, phoneNomber)
    data = Phone.getStat(phoneId)
    while 'STATUS_OK' not in data:
        data = Phone.getStat(phoneId)
        sleep(2)
    
    code = data.split(':')[1]
    d = mail.final(code)
    if len(d) != 1:
        login = d['login'] + '@mail.ru'
        password = d['password'] 
        addAccount(login, password)

for i in range(int(input('Введите кол-во аккаунтов, которые надо зарегестрировать: '))):
    start()


