from locust import HttpUser, TaskSet, between, task
import re
from http.cookiejar import CookieJar
from http.cookies import SimpleCookie


class AbstractUser(TaskSet):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    login = 'user2'
    password = 'TestPassword'
    key = ""


    def login(self):
        response = self.client.get('/login/', name='login')
        self.key = re.findall("value=\"[a-zA-Z0-9]*\"", response.text)[0].split('\"')[1]

    def login_user(self):
        for cookie in self.cookies:
            print(cookie)
        self.client.post('/login/', {
            'csrfmiddlewaretoken': self.key,
            'username': self.login,
            'password': self.password
        }, name="login", cookies={'csrftoken': self.key})


class LoginUserBehavior(AbstractUser):
        @task(1)
        def scenario(self):
            print("start scenario")
            self.login()
            self.login_user()


class LoginUser(HttpUser):
    tasks = [LoginUserBehavior]
    wait_time = between(1, 3)
