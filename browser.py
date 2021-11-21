import requests
import base64

PARENT_REG_URL = 'https://gate.educont.ru/api/v1/profile/registration'
ADD_STUDENT_URL = 'https://gate.educont.ru/api/v1/student/add-student'
TOKEN_URL = 'https://gate.educont.ru//oauth/token'
PROMO_ACTIVATE_URL = ' https://gate.educont.ru/api/v1/smartcode/student-promo/{}'
PROFILE_INFO_URL = 'https://gate.educont.ru/api/v1/profile'


class Registration(object):
    def __init__(self, parent, student):
        self.parent = parent
        self.student = student
        self.token = ''
        self.ses = requests.Session()

    def _get_token(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        q = self.ses.post(TOKEN_URL, headers=headers, params={
            'grant_type': 'password',
            'username': self.parent['email'],
            'password': self.parent['password']
        })

        return q.json()['access_token']

    def parent_reg(self):
        headers = {'Content-Type': 'application/json'}
        self.ses.post(PARENT_REG_URL, headers=headers,
                      json={
                          "name": self.parent['name'], "surname": self.parent['surname'],
                          "middleName": self.parent['middleName'],
                          "fullName": self.parent['name'] + ' ' + self.parent['surname'] + ' ' + self.parent[
                              'middleName'],
                          "phone": self.parent['phone'], "email": self.parent['email'],
                          "password": self.parent['password'], "confirmPassword": self.parent['password'],
                          "role": "PARENT",
                          "confirm": True,
                          "subscribe": False,
                      }
                      )
        self.token = self._get_token()

    def promo_activate(self, student_id):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        self.ses.post(PROMO_ACTIVATE_URL.format(student_id), headers=headers)

    def add_student(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }

        student_id = self.ses.post(ADD_STUDENT_URL, headers=headers,
                                   json=[{
                                       "name": self.student['name'], "surname": self.student['surname'],
                                       "middleName": self.student['middleName'],
                                       "fullName": self.student['name'] + ' ' + self.student['surname'] + ' ' +
                                                   self.student[
                                                       'middleName'],
                                       "birthdate": "2004-10-13", "grade": self.student['grade'], "letter": "А",
                                       "roles": ["STUDENT"], "role": "STUDENT",
                                       "studentGradeEducationalInstitutions": [
                                           {
                                               "gradeEducationalInstitution": {
                                                   "educationalInstitution": {
                                                       "id": "de221341-d937-4f6a-8630-de45908a4f31"
                                                   },
                                                   "educationalInstitutionId": "de221341-d937-4f6a-8630-de45908a4f31",
                                                   "grade": int(self.student['grade']),
                                                   "letter": "А"
                                               },
                                               "isActual": True
                                           }
                                       ],
                                   }]
                                   ).json()[0]
        self.promo_activate(student_id)


def get_fox_url(grade, token):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/94.0.4606.81 Safari/537.36',
        'Authorization': 'Bearer ' + token
    }

    r = requests.get(PROFILE_INFO_URL, headers=headers)

    return 'https://foxford.ru/educont/codes/new/' + base64.b64encode(
        (
                'id=' + r.json()['students'][0]['id'] + f'_userType=STUDENT_grade={grade}'
        ).encode("UTF-8")).decode("UTF-8")

