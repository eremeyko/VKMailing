from os import system
from random import choice, shuffle
from sys import exit
from time import sleep

import vk_api
import vk_captchasolver as vc

i = 0
timing = 0

accounts = open("accounts.txt", "r").read().splitlines()
message = open("messages.txt", "r").read().split("|")


def authvk(accounts):
    global vk
    global i
    for n, j in enumerate(accounts, start=1):
        try:
            print(f"[#{n + i} accounts.txt] Попытка входа в аккаунт...")
            vk_session = vk_api.VkApi(
                login=j.split(":")[0],
                password=j.split(":")[1],
                app_id=2685278,
                scope=4096,
            )
            vk_session.auth()
            vk = vk_session.get_api()

            print(f"[#{n + i} accounts.txt] Успешно вошли.")
            i += n
            return vk

        except IndexError:
            print("  [!accounts.txt] Уберите лишние пробелы или добавьте аккаунты.")
            system("pause")
            exit()

        except vk_api.exceptions.AuthError:
            print("  [!accounts.txt] Токен невалид!")

        except Exception as e:
            print(f"  [!!!] {e}")
            system("pause")
            exit()


def checkFiles(accounts, mess):
    if accounts[0] == "":
        print("  [!accounts.txt] Укажите аккаунты!")
        system("pause")
        exit()

    if mess[0] == "":
        print("  [!messages.txt] Укажите сообщения!")
        system("pause")
        exit()


def captcha_handler(captcha):
    key = vc.solve(sid=captcha.sid, s=1)
    print("  [?] Решили капчу")
    return captcha.try_again(key)


def getUsers(vk):
    friendsIds = []

    for i in range(2):
        friendsList = vk.friends.get(
            fields="can_write_private_message", count=5000, offset=i * 5000
        )["items"]

        for friend in friendsList:
            if friend["can_write_private_message"] == 1 and not friend.get("deactivated"):
                friendsIds.append(friend["id"])

    return shuffle(friendsIds)


def main(i, mess, accounts, timing):
    if vk := authvk(accounts):
        userlist = getUsers(vk)
        for id in userlist:
            try:
                sleep(timing)
                message = choice(mess)
                vk.messages.send(user_id=id, random_id=0, message=message)
                print(f"[#{i+1}] Сообщение id{id} отправлено.")

            except vk_api.exceptions.Captcha as captcha:
                print("  [?]Ой, капча...")
                captcha_handler(captcha)
                print(f"[#{i+1}] Сообщение id{id} отправлено.")

            except vk_api.exceptions.ApiError as e:
                if e.code == 6:
                    print(f"  [!{i}] Слишком быстро\n  [•{i+1}] Ждем 2 секунды...")
                    sleep(2)

                elif e.code == 7:
                    print(f"  [!{i}] Лимит\n  [•{i}] Меняем аккаунт...")
                    vk = authvk(accounts)
                    userlist = getUsers(vk)

                elif e.code == 5:
                    print(f"  [!{i}] Невалид\n  [•{i + 1}] Меняем аккаунт...")
                    vk = authvk(accounts)
                    userlist = getUsers(vk)

                elif e.code == 17:
                    print(f"  [!{i}] Неожиданная валидация\n  [•{i + 1}] Меняем аккаунт...")
                    vk = authvk(accounts)
                    userlist = getUsers(vk)

                elif e.code == 29:
                    print(f"  [!{i}] Лимит на методе\n  [•{i + 1}] Меняем аккаунт...")
                    vk = authvk(accounts)
                    userlist = getUsers(vk)

                elif e.code == 900:
                    print(f"  [!{i}] {id} в черном списке в заданном аккаунте")
                    pass

                elif e.code == 902:
                    print(f"  [!{i}] {id} нельзя отправить сообщение")
                    pass

                elif e.code == 914:
                    print(f"  [!{i}] Очень длинный текст сообщения, ВК не пропускает!\n  Измените, текст в message.txt:\n{message}")
                    system("pause")
                    exit()

                else:
                    print(f"  {e.code}:{e}\n  [?] Обратитесь к создателю\tпж")
                    system("pause")
                    exit()


checkFiles(accounts, message)

while timing <= 0:
    try:
        timing = int(input("[!] Введите задержку между отправкой сообщений\n  \
Рекомендуется 5-10 секунд для лучшей работы\n  "))
    except ValueError:
        system("cls")

main(i, message, accounts, timing)

print("[:)] Рассылка окончена")
system("pause")
