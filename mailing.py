import vk_api
import vk_captchasolver as vc
from os import system
from sys import exit
from random import choice
from vk_api import exceptions
from time import sleep

i = 0


def authvk(strt, accounts):
    global vk
    global i
    while (True):
        try:
            print(f'[#{strt+1} accounts.txt]Попытка входа в аккаунт...')
            vk_session = vk_api.VkApi(
                login=accounts[strt].split(':')[0],
                password=accounts[strt].split(':')[1],
                app_id=2685278,
                scope=4096
            )
            vk_session.auth()
            vk = vk_session.get_api()

            if (vk != None):
                print(f'[#{strt+1} accounts.txt]Успешно вошли.')
                return vk

        except IndexError:
            print('  [!accounts.txt]Уберите лишние пробелы или добавьте аккаунты.')
            exit()

        except vk_api.exceptions.AuthError:
            print('  [!accounts.txt]Токен невалид!')
            i += 1
            strt += 1


def checkFiles(accounts, mess):
    if (accounts[0] == ""):
        print('  [!accounts.txt]Укажите аккаунты!')
        exit()

    if (mess[0] == ""):
        print('  [!messages.txt]Укажите сообщения!')
        exit()


def captcha_handler(captcha):
    key = vc.solve(sid=captcha.sid, s=1)
    print('  [?]Решили капчу')
    return captcha.try_again(key)


def getUsers(vk):
    friendsIds = []

    for i in range(2):
        friendsList = vk.friends.get(
            fields='can_write_private_message',
            count=5000,
            offset=i
        )['items']
        for friend in friendsList:
            if (friend['can_write_private_message'] == 1 and not friend.get('deactivated')):
                friendsIds.append(friend['id'])
    return friendsIds


def main(i, mess, accounts):
    vk = authvk(i, accounts)
    userlist = getUsers(vk)
    for id in userlist:
        try:
            vk.messages.send(
                user_id=id,
                random_id=0,
                message=choice(mess)
            )
            print(f'[#{i+1}]Сообщение id{id} отправлено.')

        except vk_api.exceptions.Captcha as captcha:
            print('  [?]Ой, капча...')
            captcha_handler(captcha)
            print(f'[#{i+1}]Сообщение id{id} отправлено.')

        except vk_api.exceptions.ApiError as e:
            if (e.code == 6):
                print(f'  [!{i+1}]Слишком быстро\n  [•{i+1}]Ждем 2 секунды...')
                sleep(2)

            if (e.code == 7):
                print(f'  [!{i+1}]Лимит\n  [•{i+1}]Меняем аккаунт...')
                i += 1
                vk = authvk(i, accounts)
                userlist = getUsers(vk)

            elif (e.code == 5):
                print(f'  [!{i+1}]Невалид\n  [•{i+1}]Меняем аккаунт...')
                i += 1
                vk = authvk(i, accounts)
                userlist = getUsers(vk)

            else:
                print(f'{e.code}:{e}\n[?]Обратитесь к создателю')
                exit()


if __name__ == '__main__':
    accounts = open('accounts.txt', 'r').read().splitlines()
    mess = open('messages.txt', 'r').read().split('|')

    checkFiles(accounts, mess)

    main(i, mess, accounts)
    print('[:)]Рассылка окончена')
    system('pause')
