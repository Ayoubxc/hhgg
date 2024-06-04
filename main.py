from flask import Flask, jsonify, render_template, request
from bs4 import BeautifulSoup
import requests
import random

app = Flask(__name__)

class FacebookAccountCreator:
    def __init__(self):
        self.cookies = {
            "lsd": "", "jazoest": "", "ccp": "", "reg_instance": "", "submission_request": "", "reg_impression_id": ""
        }
        self.password = "".join(random.choice("1234567890qpwoeirutyalskdjfhgmznxbcv") for _ in range(10))
        self.email = random.choice('klxjxjwa') + "".join(random.choice("1234567890qpwoeirutyalskdjfhgmznxbcv") for _ in range(15))
        self.name = "nino" 
        self.name2 = "haha"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, مثل Gecko) Chrome/58.0.3029.110 Safari/537.3"

    def create_account(self):
        self.get_cookies()
        return self.register()

    def get_cookies(self):
        url = "https://mbasic.facebook.com/reg/?cid=103&refsrc=deprecated&_rdr"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        self.cookies['lsd'] = soup.select_one('input[name=lsd]')['value']
        self.cookies['jazoest'] = soup.select_one('input[name=jazoest]')['value']
        self.cookies['ccp'] = soup.select_one('input[name=ccp]')['value']
        self.cookies['reg_instance'] = soup.select_one('input[name=reg_instance]')['value']
        self.cookies['submission_request'] = soup.select_one('input[name=submission_request]')['value']
        self.cookies['reg_impression_id'] = soup.select_one('input[name=reg_impression_id]')['value']

    def register(self):
        url = "https://mbasic.facebook.com/reg/submit/?cid=103"
        headers = {
            "Host": "mbasic.facebook.com",
            "Cookie": f"datr={self.cookies['reg_instance']}",
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://mbasic.facebook.com/reg/?cid=103&refsrc=deprecated&_rdr",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://mbasic.facebook.com",
            "Dnt": "1",
            "Upgrade-Insecure-Requests": "1"
        }
        data = {
            "lsd": self.cookies['lsd'],
            "jazoest": self.cookies['jazoest'],
            "ccp": self.cookies['ccp'],
            "reg_instance": self.cookies['reg_instance'],
            "submission_request": self.cookies['submission_request'],
            "reg_impression_id": self.cookies['reg_impression_id'],
            "firstname": self.name,
            "lastname": self.name2,
            "reg_email__": f"{self.email}@gmail.com",
            "sex": "2",
            "birthday_month": "9",
            "birthday_day": "5",
            "birthday_year": "1990",
            "reg_passwd__": self.password,
            "submit": "Sign Up"
        }
        r = requests.post(url, headers=headers, data=data)
        if 'take you through a few steps to confirm your account on Facebook' in r.text:
            account_details = {
                "email": self.email,
                "password": self.password,
                "user_agent": self.user_agent
            }
            return account_details
        else:
            return {"error": "There was an error with your registration. Please try again."}

@app.route('/')
def display_webview():
    return render_template('index.html')

@app.route('/create-facebook-account', methods=['POST'])
def create_facebook_account():
    account_creator = FacebookAccountCreator()
    account_details = account_creator.create_account()
    return jsonify(account_details)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
