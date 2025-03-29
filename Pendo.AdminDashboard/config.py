from flask import Flask
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'reallyStrongPwd123'
app.permanent_session_lifetime = timedelta(minutes=30)

api_url = 'https://pendo-gateway.clsolutions.dev'
