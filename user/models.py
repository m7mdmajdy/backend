from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid
import werkzeug
from keras.preprocessing import image
import os,os.path
from flask import Flask,jsonify,request
import os,os.path
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
from keras.models import Sequential  
from keras.layers import Conv2D, Flatten, Dense, MaxPool2D

class User:

  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200
 
  def signup(self):
    print(request.form)
    
    #redirect('/user/signup/detect')

    # Create the user object
    user = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "email": request.form.get('email'),
      "password": request.form.get('password'),
      "result":" " 
    }
    # Encrypt the password
    user['password'] = pbkdf2_sha256.encrypt(user['password'])
    #  Save detection result
    # Check for existing email address
    if db.users.find_one({ "email": user['email'] }):
      return jsonify({ "error": "Email address already in use" }), 400
      
    if db.users.insert_one(user):
     # print (self.start_session(user))
      return self.start_session(user)

    #res=request.form.get('result')
    #db.users.update_one({"email":request.form.get('email')},{"$set":{"result":res}})

       
  def signout(self):
    session.clear()
    return redirect('/')
  
  def login(self):
    user = db.users.find_one({
      "email": request.form.get('email')
    })
  
    
    if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
      return self.start_session(user)
    return jsonify({ "error": "Invalid login credentials" }), 401

    
  def upload(self):
        if request.method=="POST":
            imagefile=request.files['image']
            print("GGGGGGGGGG")
            numOfFiles=len(os.listdir('D:/dermascope backend/image'))
            print("Num of files from post"+str(numOfFiles))
            
            filename=werkzeug.utils.secure_filename(imagefile.filename)
            imagefile.save("./image/"+ filename)
            os.rename("./image/"+ filename,"./image/"+str(numOfFiles+1)+".jpg")
            print('okstar')
            return "HHH"
        if request.method=="GET":
            numOfFiles=len(os.listdir('D:/dermascope backend/image/'))
            print("Num of files from get"+str(numOfFiles))
            image_path= "D:/dermascope backend/image/"+str(numOfFiles)+".jpg"
            classes = {4: ('nv', ' melanocytic nevi'), 0: ('mel', 'melanoma'), 2 :('bkl', 'benign keratosis-like lesions'), 3:('bcc' , ' basal cell carcinoma'), 5: ('vasc', ' pyogenic granulomas and hemorrhage'), 6: ('akiec', 'Actinic keratoses and intraepithelial carcinomae'),  1: ('df', 'dermatofibroma')}
            
            model_path = "D:/dermascope backend/Skin_Cancer (1).hdf5"
            
            #####################################################################################################################
            def create_model():
                model = Sequential()
                model.add(Conv2D(16, kernel_size = (3,3), input_shape = (28, 28, 3), activation = 'relu', padding = 'same'))
                model.add(MaxPool2D(pool_size = (2,2)))

                model.add(Conv2D(32, kernel_size = (3,3), activation = 'relu', padding = 'same'))
                model.add(MaxPool2D(pool_size = (2,2), padding = 'same'))

                model.add(Conv2D(64, kernel_size = (3,3), activation = 'relu', padding = 'same'))
                model.add(MaxPool2D(pool_size = (2,2), padding = 'same'))
                model.add(Conv2D(128, kernel_size = (3,3), activation = 'relu', padding = 'same'))
                model.add(MaxPool2D(pool_size = (2,2), padding = 'same'))

                model.add(Flatten())
                model.add(Dense(64, activation = 'relu'))
                model.add(Dense(32, activation='relu'))
                model.add(Dense(7, activation='softmax'))
                return model




            def load_trained_model(model_path):
                model = create_model()   
                model.load_weights(model_path)
                return model

            model = load_trained_model(model_path)


            # # preparing image
            img = image.load_img(image_path, target_size=(28, 28))
            img_array = image.img_to_array(img)
            img_batch = np.expand_dims(img_array, axis=0)
            images = np.vstack([img_batch])

            #predict image
            classe = model.predict(images)
            classe = classe[0]
            print(classe)
            max_prob = max(classe)
            print(max_prob)

            if max_prob>0.80:
                class_ind = list(classe).index(max_prob)
                class_name = classes[class_ind]
                # short_name = class_name[0]
                full_name = class_name[1]
                print(full_name)
            else:

                full_name = 'No Disease detected' #if confidence is less than 80 percent then "No disease" 
########################################################################################################################
            #model_path = r"E:\Magdy\4th grade\appp\Skin_Cancer.h5"
            #model = load_model(model_path)
            
           # if full_name=='melanoma':
            #  desData='Pigmented lesions of the skin are commonly called freckles. They include solar lentigo, congenital nevi, mucosal nevi, and special nevi of the palms and soles. This activity will help to differentiate the various pedal nevi from acral lentiginous melanoma clinically. Plantar melanomas are characteristically late to be diagnosed, have a poorer response to treatment, and have a significantly higher mortality rate when compared to more proximal melanomas'

        return jsonify(

            {'resssss' : f'Result ={full_name}'}
            
            ) #returning key-value pair in json format

  def saveresult(self):
  #  result=request.form.get('result')
     res=request.form.get('image')  
     db.users.update_one({"email":request.form.get('email')},{"$set":{"result":res}})
     return jsonify({ "result11": "result is saved"
      })
 