from selenium import webdriver

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import time
import re

menu = "0. Повторно вызвать меню\n\n1. Добавить новый аккаунт\n2. Очистить файл с аккаунтами \
    \n3. Взять следующий аккаунт\n4. Зайти на текущий аккаунт\n5. Отправить рассылку по пользователям \
    \n6. Сделать рассылку со всех аккаунтов всем пользователям\n7. Выйти из программы"
print(menu)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message})

def loginInAccount(tlogin, tpassword):
    try: 
        options = webdriver.ChromeOptions();
        options.add_argument("--disable-extensions")
        options.add_argument("--log-level=3")
 

        driver = webdriver.Chrome(options=options)
        driver.get('https://vk.com')
        driver.maximize_window()
        
        # time.sleep(3) # Сон в 3 секунды

        email = driver.find_element_by_id("index_email")
        email.send_keys(tlogin)
        password = driver.find_element_by_id("index_pass")
        password.send_keys(tpassword)
        button = driver.find_element_by_id("index_login_button")
        button.click()

        print(driver.current_url)
    except Exception as e:
        print(f"Непредвиденная ошибка со стороны драйвера браузера. {e}")


database = []
with open("accounts.txt", 'r+') as accounts:
    counter_accs = 0
    for account in accounts:
        try:
            counter_accs += 1
            login, password = re.split(r";|,|:| ", account.strip())
            database.append((login, password.strip(), counter_accs))
        except:
            print("База данных аккаунтов для использования не была загружена. Формат данных не поддерживается. Строка проблемы = '" + account + "'")
            exit()

receivers = []
with open("receivers.txt", 'r+') as accounts:
    counter_res = 0
    for account in accounts:
        try:
            counter_res += 1
            receivers.append(account.strip())
        except:
            print("База данных пользователей для рассылки не была загружена. Формат данных не поддерживается. Строка проблемы = '" + account + f"' в строке {counter_res}")

if counter_accs > 1:
    pointer = 0
    current_user = (database[pointer][0], database[pointer][1])
else:
    print("\nАккаунтов для использования не было обнаружено")

if counter_accs <= 1:
    print("\nАккаунтов для рассылки не было обнаружено")


def getChoose():
    return input("\nВыберите пункт меню: ")


def setCurrentUser():
    global current_user
    global pointer
    current_user = database[pointer][0], database[pointer][1]
    print(f"Текущий пользователь:\nЛогин: {current_user[0]}\nПароль: {current_user[1]}")


while True:
    choose = getChoose()

    if choose == "0":
        print(menu)
    elif choose == "1":
        new_account = input(
            "Введите логин\пароль в формате loginNpassword, где N - запятая, точка с запятой, двоеточие \n")
        try:
            login, password = re.split(r";|,|:| ", new_account)
            database.append((login, password.strip(), len(database)))
            with open("accounts.txt", 'a') as accounts:
                accounts.write("\n")
                accounts.write(" ".join([login, password]))
        except:
            print("Неверный формат данных!")
    elif choose == "2":
        answer = input("Вы уверены, что хотите удалить все записи? y/n \n")
        if answer == "y":
            with open("accounts.txt", 'w') as file:
                file.write("")
                print("Записи были удалены")
    elif choose == "3":
        if pointer < len(database):
            pointer += 1
            setCurrentUser()
        else:
            print("Все аккаунты были использованы!")
    elif choose == "4":
        print("Вход с текущего пользователя")
        loginInAccount(current_user[0], current_user[1])
    elif choose == "5":
        message = input("Что отправить для рассылки?")

        vk = vk_api.VkApi(login=current_user[0], password=current_user[1])

        for account in receivers:
            try:
                write_msg(account, message)
            except Exception as e:
                print("Ошибка отправки сообщения. Текст ошибки: " + e)
    elif choose == "6":
        print("Сообщения будут отправлены!")
    elif choose == "7":
        exit()
    else:
        print("Неизвестная команда!")
