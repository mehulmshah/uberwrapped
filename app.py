from flask import Flask, render_template, request
from utils import ArkeoStatusUpdate
from cryptography.fernet import Fernet
from constants import ADMIN_PW

app = Flask(__name__)

@app.route('/faq', methods=['GET', 'POST'])
def faq():
    return render_template('faq.html', alerttype='success', url=url)

@app.route('/')
def index():
    return render_template('layout.html')
