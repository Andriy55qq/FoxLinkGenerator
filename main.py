import random
import string
from browser import *


grade = str(input('Класс: '))
if int(grade) not in range(1, 12):
    print('Неверно указан класс')
    exit()

count = int(input('Количество ссылок: '))
if count > 50:
    print('Не рекомендуется генерировать столько ссылок за раз')
    exit()


def random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

def random_phone():
    return '+7908' + str(random.randint(1000000, 9999999))


for i in range(count):
    email = f'{random_string(9)}@gmail.com'
    Registration(
        {"name": 'Пупкин', "surname":'Владислав',"middleName":'Олегович', "phone": random_phone(), "email": email, 'password': 'Qwerty132'}, 
        {"name": 'Пупкин', "surname":'Алексей',"middleName":'Владиславович',"grade": grade}
    ).reg()
    print(Auth(email, 'Qwerty132').get_fox_url(grade))