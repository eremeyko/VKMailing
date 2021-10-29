import vk_api
from os import system
from sys import exit
from random import choice
from vk_api import exceptions

i = 0
mess1 = open('messages.txt', 'r')
mess = (mess1.read()).split(',')

for token in open("tokens.txt", 'r'):
    token = token.split(':')
    try:
        i += 1
        vk_session = vk_api.VkApi(login=token[0], password=token[1])
        vk = vk_session.get_api()
        print(f'[•{i}]Вошел в аккаунт.')

    except vk_api.exceptions.ApiError as e:
        print('\t[!]Токен невалид!')

    except IndexError:
        print('\t[!]Вы не задали страницы в текстовике tokens.txt')
        exit()

    if vk.users.get:
        try:
            for ids in open("userlist.txt", 'r+'):
                id = ids.split('https://vk.com/')
                if ids.startswith('id'):
                    vk.messages.send(user_ids=int(id),
                                     message=choice(mess), random_ids=0)
                else:
                    vk.messages.send(domain=id,
                                     message=choice(mess), random_ids=0)
                print(f'[•{i}]Сообщение {id} отправлено.')
        except vk_api.exceptions.ApiError as e:
            print('\t[!]Токен невалид!')
    else:
        pass

system('pause')
