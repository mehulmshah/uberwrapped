from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from constants import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
import os
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/faq', methods=['GET', 'POST'])
def faq():
    return render_template('faq.html', alerttype='success', url=url)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['tripData']
      analyticsObj = basic_analytics(f)
      return render_template('analytics.html', data=analyticsObj)


def basic_analytics(file):
    
