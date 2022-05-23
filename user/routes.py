import email
from re import X
from charset_normalizer import detect
from flask import Flask, redirect,request, url_for
from psutil import users
from requests import session
from app import app
from user.models import User
#from user.api import Detect


@app.route('/user/signup', methods=['POST','GET'])
def signup():
        return User().signup()
        

    #if request.method=="POST":
     #  imagefile=request.files['image']

     #  return User().signup() 
     # else:
      #   return User().signup()
      #if request.files['image']:

#def upload(): 
 # if request.files['image']:
  # return User().upload() 
#@app.route('/signup', methods=['POST','GET'])
#def saveresult():
   
 # return User().saveresult(em)

@app.route('/user/detect', methods=['POST','GET'])
def upload():
  return User().upload()



@app.route('/user/save', methods=['POST','GET'])
def save():
  return User().saveresult()


@app.route('/user/signout')
def signout():
  return User().signout()

@app.route('/user/login', methods=['POST','GET'])
def login():
  return User().login()

    
