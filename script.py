from selenium import webdriver

import time
import re

menu = "0. Повторно вызвать меню\n1. Добавить новый аккаунт\n2. Очистить файл с аккаунтами \
    \n3. Открыть следующий аккаунт\n4. Отправить рассылку по пользователям \
    \n5. Выйти из программы"
print(menu)


def loginInAccount(tlogin, tpassword):
    try:
        driver = webdriver.Chrome()
        driver.get('https://vk.com')

        # time.sleep(3) # Сон в 3 секунды

        email = driver.find_element_by_id("index_email")
        email.send_keys(tlogin)
        password = driver.find_element_by_id("index_pass")
        password.send_keys(tpassword)
        button = driver.find_element_by_id("index_login_button")
        button.click()
    except:
        print("Непредвиденная ошибка со стороны драйвера браузера")


database = []
with open("accounts.txt", 'r+') as accounts:
    counter = 1
    for account in accounts:
        try:
            login, password = re.split(r";|,|:| ", account)
            database.append((login, password.strip(), counter))
            counter += 1
        except:
            print("База данных не была загружена. Формат данных не поддерживается. Строка проблемы = " + account)
            exit()

if counter > 0:
    pointer = 0
else:
    print("Аккаунтов не было обнаружено")
    exit()

def getChoose():
    return input("\nВыберите пункт меню: ")


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
        login, password = database[pointer][0], database[pointer][1]
        print(login)
        print(password)
        loginInAccount(login, password)
        pointer += 1
    elif choose == "4":
        message = input("Что отправить для рассылки?")
    elif choose == "5":
        exit()
    else:
        print("Неизвестная команда!")
