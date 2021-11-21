import random
import string
from browser import *

FAKE_CREDS = {
    'parent': {
        'name': 'Пупкин', 'surname': 'Владислав', 'middleName': 'Олегович',
        'phone': '', 'email': '', 'password': 'Qwerty132'
    },
    'student': {
        'name': 'Пупкин', 'surname': 'Алексей', 'middleName': 'Владиславович',
        "grade": ''
    }
}


def _random_email(length=9):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for _ in range(length))
    return f'{rand_string}@gmail.com'


def _random_phone():
    return '+7908' + str(random.randint(1000000, 9999999))


def get_links(grade, count):
    for _ in range(count):
        FAKE_CREDS['parent']['email'] = _random_email()
        FAKE_CREDS['parent']['phone'] = _random_phone()
        FAKE_CREDS['student']['grade'] = grade
        acc = Registration(FAKE_CREDS['parent'], FAKE_CREDS['student'])
        acc.parent_reg()
        acc.add_student()
        print(get_fox_url(grade, acc.token))
        
if __name__ == '__main__':
    grade = str(input('Класс: '))
    if int(grade) not in range(1, 12):
        print('Неверно указан класс')
        exit()

    count = int(input('Количество ссылок: '))
    if count > 50:
        print('Не рекомендуется генерировать столько ссылок за раз')
        exit()


    get_links(grade, count)
