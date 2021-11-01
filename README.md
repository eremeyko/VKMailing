# VKMailing (Рассылка сообщений)
> Синий текст кликабелен

 Функционал | Описание | Стадия |
|----------------|:---------:|:---------:
| [По заданному списку](https://github.com/eremeyko/VKMailing/tree/To-List) | Задается список страниц, кому будут отправляться сообщения | [Готово](https://github.com/eremeyko/VKMailing/tree/To-List)
| [**По друзьям пользователя**](https://github.com/eremeyko/VKMailing/edit/To-Friends) | Сообщения будут отправляться друзьям заданного аккаунта | [Готово*](https://github.com/eremeyko/VKMailing/edit/To-Friends)

> *но требует теста

## Введение: 
1. [Установка библиотек](https://github.com/eremeyko/VKMailing#%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-%D0%B1%D0%B8%D0%B1%D0%BB%D0%B8%D0%BE%D1%82%D0%B5%D0%BA)
2. [Заполнение параметров](https://github.com/eremeyko/VKMailing#%D0%97%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BF%D0%B0%D1%80%D0%B0%D0%BC%D0%B5%D1%82%D1%80%D0%BE%D0%B2)

    2.1 [accounts.txt](https://github.com/eremeyko/VKMailing#accountstxt)

    2.2 [messages.txt](https://github.com/eremeyko/VKMailing#messagestxt)

3. [Запуск](https://github.com/eremeyko/VKMailing#%D0%97%D0%B0%D0%BF%D1%83%D1%81%D0%BA)

4. [Лимиты и ограничения](https://github.com/eremeyko/VKMailing#%D0%9B%D0%B8%D0%BC%D0%B8%D1%82%D1%8B-%D0%B8-%D0%BE%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%B8%D1%8F)
____
## Установка библиотек
Для работы требуется лишь библиотека VK_api и [vk_captchasolver](https://github.com/DedInc/vk_captchasolver)

Открываем консоль и вводим:
```
pip install vk_api
```
Дожидаемся конца загрузки и читаем следующий пункт

1. Зайдите в репозиторий с [vk_captchasolver (**открой**)](https://github.com/DedInc/vk_captchasolver/releases)

2. Скачайте первый файл `vk_captchasolver-1.0.0-py3-none-any.whl` 

3. Перекиньте в любую удобную нам папку

3. Откройте консоль в папке с файлом 

4. Пропишите в консоль команду `pip install vk_captchasolver-1.0.0-py3-none-any.whl`
____
## Заполнение параметров
Чтобы всё корректно работало, необходимо заполнить лежайшие в папке со скриптом текстовики

### accounts.txt
Принимается неограниченное число аккаунтов формата

1 строка = 1 аккаунт
```
логин:пароль[:токен]
```
Авторизация происходит через Логин и Пароль, поэтому Токен учитываться не будет
____
### messages.txt
Список сообщений __через запятую__. Случайно берёт сообщение из списка и отправляет пользователю

```
Привет!| Как дела?| Репозиторий говно
```

Можно также и одно сообщение, но без знака `|`
____
## Запуск
<details>
<summary>1. Для запуска откройте консоль в папке с файлом (открой)</summary>
<img src="https://i.imgur.com/bu5qQne.png">
</details>

<details>
<summary>2. Пропишите py mailing.py (открой)</summary>
<img src="https://i.imgur.com/lNaIpQk.png">
</details>

<details>
<summary>3. Запустите!</summary>
<pre>
    <kbd>Enter</kbd> нажми...
</pre> 
</details>

____
## Лимиты и ограничения
1. В принципе, проблем быть не должно. Рассылка производится друзьям, поэтому ограничения на отправку сообщений быть не может. В случае чего см 3 пункт

2. Заданные аккаунты могут отлететь. Нет никакой гарантии, что этого не случится, все вопросы к госпоже удаче
> Нет, серьёзно. Если какой-то чухан пометит Ваше сообщение как спам, то Ваш аккаунт отлетит 

3. Если у Вас появятся ошибки, то милости прошу в [Личку ВК](https://vk.me/eremey) или в [Вопросы](https://github.com/eremeyko/VKMailing/issues)
