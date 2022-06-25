from os import system
from random import choice, shuffle
from sys import exit
from time import sleep

import vk_api
import vk_captchasolver as vc

i = 0
timing = 0

accounts = open("accounts.txt", "r", encoding="utf-8").read().splitlines()
userlist = open("userlist.txt", "r", encoding="utf-8").read().splitlines()
message = open("messages.txt", "r", encoding="utf-8").read().split("|")


def authvk(accounts):
    global vk
    global i
    for n, j in enumerate(accounts):
        try:
            print(f"[#{n + 1} accounts.txt] Попытка входа в аккаунт...")
            vk_session = vk_api.VkApi(
                login=j.split(":")[0],
                password=j.split(":")[1],
                app_id=2685278,
                scope=4096,
            ).auth()
            vk = vk_session.get_api()

            print(f"[#{n + 1} accounts.txt] Успешно вошли.")
            return vk

        except IndexError:
            print("  [!accounts.txt] Уберите лишние пробелы или добавьте аккаунты.")
            system("pause")
            exit()

        except vk_api.exceptions.AuthError:
            print("  [!accounts.txt] Токен невалид!")
            i += 1

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

    system("cls")


def captcha_handler(captcha):
    key = vc.solve(sid=captcha.sid, s=1)
    print("  [?] Решили капчу.")
    return captcha.try_again(key)


def main(userlist, i, mess, accounts, timing):
    if vk := authvk(accounts):
        for ids in userlist:
            id = ids.strip("https://vk.com/")
            try:
                sleep(timing)
                if id.startswith("id"):
                    vk.messages.send(
                        user_id=id.strip("id"), random_id=0, message=choice(mess)
                    )
                else:
                    vk.messages.send(domain=id, random_id=0, message=choice(mess))
                print(f"[#{i + 1}] Сообщение {id} отправлено.")
            except vk_api.exceptions.Captcha as captcha:
                print("  [?] Ой, капча...")
                captcha_handler(captcha)
                print(f"[#{i + 1}] Сообщение {id} отправлено.")

            except vk_api.exceptions.ApiError as e:
                if e.code == 7:
                    i += 1
                    print(f"  [!{i}] Лимит\n  [•{i}] Меняем аккаунт...")
                    vk = authvk(i, accounts)

                elif e.code == 5:
                    i += 1
                    print(f"  [!{i + 1}] Невалид\n  [•{i + 1}] Меняем аккаунт...")
                    vk = authvk(i, accounts)

                else:
                    print(f"  {e.code}:{e}\n  [?] Обратитесь к создателю\tпж")
                    system("pause")
                    exit()


checkFiles(accounts, userlist, message)

while timing <= 0:
    try:
        timing = int(input("[!] Введите задержку между отправкой сообщений\n  "))
    except ValueError:
        system("cls")

shuffle(userlist)
main(userlist, i, message, accounts, timing)

print("[:)] Рассылка окончена.")
system("pause")
