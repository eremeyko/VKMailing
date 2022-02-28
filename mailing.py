from os import system
from random import choice, shuffle
from sys import exit
from time import sleep

import vk_api
import vk_captchasolver as vc

i = 0


def authvk(strt, accounts):
    global vk
    global i
    while True:
        try:
            print(f"[#{strt+1} accounts.txt] Попытка входа в аккаунт...")
            vk_session = vk_api.VkApi(
                login=accounts[strt].split(":")[0],
                password=accounts[strt].split(":")[1],
                app_id=2685278,
                scope=4096,
            )
            vk_session.auth()
            vk = vk_session.get_api()

            if vk is not None:
                print(f"[#{strt+1} accounts.txt] Успешно вошли.")
                return vk

        except IndexError:
            print("  [!accounts.txt] Уберите лишние пробелы или добавьте аккаунты.")
            system("pause")
            exit()

        except vk_api.exceptions.AuthError:
            print("  [!accounts.txt] Токен невалид!")
            i += 1
            strt += 1

        except Exception as e:
            print(f"  [!!!] {e}")
            system("pause")
            exit()


def checkFiles(accounts, userlist, mess):
    if accounts[0] == "":
        print("  [!accounts.txt] Укажите аккаунты!")
        system("pause")
        exit()

    elif userlist == "":
        print("  [!userlist.txt] Укажите страницы!")
        system("pause")
        exit()

    elif mess[0] == "":
        print("  [!messages.txt] Укажите сообщения!")
        system("pause")
        exit()


def captcha_handler(captcha):
    key = vc.solve(sid=captcha.sid, s=1)
    print("  [?] Решили капчу.")
    return captcha.try_again(key)


def main(userlist, i, mess, accounts, timing):
    vk = authvk(i, accounts)
    for ids in userlist:
        id = ids.strip("https://vk.com/")
        try:
            sleep(timing)
            if id.startswith("id"):
                vk.messages.send(
                    user_id=id.strip("id"), random_id=0, message=choice(mess)
                )
                print(f"[#{i+1}] Сообщение {id} отправлено.")
            else:
                vk.messages.send(domain=id, random_id=0, message=choice(mess))
                print(f"[#{i+1}] Сообщение {id} отправлено.")

        except vk_api.exceptions.Captcha as captcha:
            print("  [?] Ой, капча...")
            captcha_handler(captcha)
            print(f"[#{i+1}] Сообщение {id} отправлено.")

        except vk_api.exceptions.ApiError as e:
            if e.code == 7:
                print(f"  [!{i+1}] Лимит\n  [•{i+1}] Меняем аккаунт...")
                i += 1
                vk = authvk(i, accounts)

            elif e.code == 5:
                print(f"  [!{i+1}] Невалид\n  [•{i+1}] Меняем аккаунт...")
                i += 1
                vk = authvk(i, accounts)

            else:
                print(f"  {e.code}:{e}\n  [?] Обратитесь к создателю\tпж)")
                system("pause")
                exit()


if __name__ == "__main__":
    timing = 0
    accounts = open("accounts.txt", "r").read().splitlines()
    userlist = open("userlist.txt", "r").read().splitlines()
    mess = open("messages.txt", "r").read().split("|")

    checkFiles(accounts, userlist, mess)

    system("cls")
    while timing <= 0:
        try:
            timing = int(input("[!] Введите задержку между отправкой сообщений\n  "))
        except ValueError:
            pass

    main(shuffle(userlist), i, mess, accounts, timing)
    print("[:)] Рассылка окончена.")
    system("pause")
