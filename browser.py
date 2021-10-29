import requests
import base64

REG_URL = 'https://gate.educont.ru/api/v1/smartcode/student'
TOKEN_URL = 'https://gate.educont.ru//oauth/token'

class Registration(object):
    def __init__(self, parent, student):
        self.parent = parent
        self.student = student

    def reg(self):
        headers = {'Content-Type': 'application/json'}
        r = requests.post(REG_URL, headers=headers, 
            json={
                "name": self.parent['name'], "surname":self.parent['surname'],"middleName":self.parent['middleName'],"fullName":self.parent['name']+' '+self.parent['surname']+' '+self.parent['middleName'],
                "role":"PARENT","phone":self.parent['phone'],"email":self.parent['email'],
                "password":self.parent['password'],
                "isActive":None,
                "students":[{
                    "name": self.student['name'], "surname":self.student['surname'],"middleName":self.student['middleName'],"fullName":self.student['name']+' '+self.student['surname']+' '+self.student['middleName'],
                    "studentGroup":None, "birthdate":"2004-10-13","grade":self.student['grade'],"role":"STUDENT","letter":"А","isActive":None
                }]
            }
        )


class Auth(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password        


    def get_fox_url(self, grade):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        s = requests.Session()
        q = s.post(TOKEN_URL, headers=headers, params={
            'grant_type': 'password',
            'username': self.email,
            'password': self.password
        })
        
        r = s.get('https://gate.educont.ru/api/v1/profile', 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36', 
            'Authorization':'Bearer '+q.json()['access_token']},
            
        )
        return 'https://foxford.ru/educont/codes/new/'+ base64.b64encode(('id='+r.json()['students'][0]['id']+f'_userType=STUDENT_grade={grade}').encode("UTF-8")).decode("UTF-8")

