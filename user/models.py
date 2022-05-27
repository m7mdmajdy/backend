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
 
  def start_session2(self,disease):
       session['diseases'] = disease
       return jsonify(disease), 200
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

            {'resssss' : f'{full_name}'}
            
            ) #returning key-value pair in json format

  def saveresult(self):
  #  result=request.form.get('result')
     res=request.form.get('image')  
     db.users.update_one({"email":request.form.get('email')},{"$set":{"result":res}})
     return jsonify({ "result11": "result is saved"
      })
  def desInfo(self):
      diseases = db.diseases.find_one({
      "name": request.form.get('disease')
        })

      return self.start_session2(diseases)


      """"
   res=request.form.get('disease')
   if res =='basal cell carcinoma':
     id=1
     name="basal cell carcinoma"
     description = "Nevoid basal cell carcinoma syndrome is a group of defects passed down through families. The disorder involves the skin, nervous system, eyes, endocrine glands, urinary and reproductive systems, and bones."
    
     prevention="The preventive measures include: \n Sunscreen: While going out in the sun, apply sunscreen creams or lotions \n  Seek shade: Avoid going out during 10 am to 2 pm. Seek shade if you are exposed to sun for a longer time\n Cover your body: Protect your body from exposing it to sunlight. Wear protective clothing while going out on a sunny day \n Use extra caution near water or sand, as this can reflect sun rays"
     symptoms="If you are experiencing new, severe, or persistent symptoms, contact a health care provider. \n Symptoms include  \n A pearly white, skin-colored or pink bump \n A brown, black or blue lesion \n A flat, scaly, reddish patch \n A white, waxy, scar-like lesion"
     treatement="Topical creams and ointments: Topical creams accelerate the immune system to act on tumor cells."
   elif res =='pyogenic granulomas and hemorrhage':
     id=2
     name="pyogenic granulomas and hemorrhage"
     description = "Pyogenic granulomas are skin growths that are small, round, and usually bloody red in color. They tend to bleed because they contain a large number of blood vessels. They’re also known as lobular capillary hemangioma or granuloma telangiectaticum."
     prevention="The preventive measures include: \n Sunscreen: While going out in the sun, apply sunscreen creams or lotions \n  Seek shade: Avoid going out during 10 am to 2 pm. Seek shade if you are exposed to sun for a longer time\n Cover your body: Protect your body from exposing it to sunlight. Wear protective clothing while going out on a sunny day \n Use extra caution near water or sand, as this can reflect sun rays"
     symptoms=" Pyogenic granulomas are commonly found on the: hands fingers arms face neck chest back \n They can also grow on the:\n lips eyelids genitals inside of the mouthIn rare cases, they can grow on the conjunctiva or cornea in your eye. The conjunctiva is the clear tissue over the white area of your eye. The cornea is the clear covering over your pupil and iris.When they occur in pregnant women, they often grow on the gums and are called “pregnancy tumors.”"
     treatement="Generally, the only way to cure pyogenic granuloma is to: Remove the lesion.,Eliminate any suspected triggers, such as medications, piercings or dental problems causing irritation in your mouth.,In people who are pregnant, granulomas typically disappear after delivery."
   elif res =='melanoma':
     id=3
     name="melanoma"
     description = "Melanoma is a type of skin cancer that begins in pigment-producing cells called melanocytes. This cancer typically occurs in areas that are only occasionally sun-exposed; tumors are most commonly found on the back in men and on the legs in women. Melanoma usually occurs on the skin (cutaneous melanoma), but in about 5 percent of cases it develops in melanocytes in other tissues, including the eyes (uveal melanoma) or mucous membranes that line the body's cavities, such as the moist lining of the mouth (mucosal melanoma). Melanoma can develop at any age, but it most frequently occurs in people in their fifties to seventies and is becoming more common in teenagers and young adults"
     prevention="The preventive measures include: \n Sunscreen: While going out in the sun, apply sunscreen creams or lotions \n  Seek shade: Avoid going out during 10 am to 2 pm. Seek shade if you are exposed to sun for a longer time\n Cover your body: Protect your body from exposing it to sunlight. Wear protective clothing while going out on a sunny day \n Use extra caution near water or sand, as this can reflect sun rays"
     symptoms="The symptoms include: \n The earliest symptom is typically a change in an existing mole or a new mole arising \n The development of a new pigmented or unusual-looking growth on your skin \n The below mentioned strategies helps discriminate the melanoma from other skin cancers. \n The ABCDE’s of melanoma helps identify the disease condition ,Asymmetry: The mole may not be uniform, one half looks different from the other half ,Border irregularity: The moles may be uneven or notched Color: The moles may be of different colors and irregular patterns ,Diameter: The mole may be bigger in size, at least a 6mm size,Evolving: The mole may be changing colors, size and texture and might also bleed,Evolving: The mole may be,changing colours, size and texture and might also bleed"
     treatement="Chemotherapy: Uses a combination of drugs to kill cancer cells."

   elif res =='benign keratosis-like lesions':
     id=4
     name="benign keratosis-like lesions"
     description =" A seborrheic keratosis grows gradually. Signs and symptoms might include:\n A round or oval-shaped waxy or rough bump, typically on the face, chest, a shoulder or the back\n A flat growth or a slightly raised bump with a scaly surface, with a characteristic 'pasted on' look\n Varied size, from very small to more than 1 inch (2.5 centimeters) across\n Varied number, ranging from a single growth to multiple growths\nVery small growths clustered around the eyes or elsewhere on the face, sometimes called flesh moles or dermatosis papulosa nigra, common on Black or brown skin\nVaried in color, ranging from light tan to brown or black \n Itchiness"
     prevention="The preventive measures include: \n Sunscreen: While going out in the sun, apply sunscreen creams or lotions \n  Seek shade: Avoid going out during 10 am to 2 pm. Seek shade if you are exposed to sun for a longer time\n Cover your body: Protect your body from exposing it to sunlight. Wear protective clothing while going out on a sunny day \n Use extra caution near water or sand, as this can reflect sun rays"
     symptoms="Flat, purple bumps that itch \n Slow-growing blisters that create sores and scabs when they burst\n White, lacy patches of skin in and around your mouth\nPainful sores\n Hair loss where the sores appear"
   
     treatement="Moles are usually not harmful. In fact, they are also considered to be symbolic of beauty. However, if a mole is suspected to be a possible cancer, a dermatologist would perform a biopsy to confirm that it is indeed cancerous. A cancerous lesion would need to be excised entirely with the surrounding skin by your physician. A cancerous condition that can be confused with a mole is melanoma."
 
   elif res =='melanocytic nevi':
     id=5
     name="melanocytic nevis"
     
     description ="Giant congenital melanocytic nevus is a skin condition characterized by an abnormally dark, noncancerous skin patch (nevus) that is composed of pigment-producing cells called melanocytes. It is present from birth (congenital) or is noticeable soon after birth.,"
     prevention="The preventive measures include: \n Sunscreen: While going out in the sun, apply sunscreen creams or lotions \n  Seek shade: Avoid going out during 10 am to 2 pm. Seek shade if you are exposed to sun for a longer time\n Cover your body: Protect your body from exposing it to sunlight. Wear protective clothing while going out on a sunny day \n Use extra caution near water or sand, as this can reflect sun rays"
     symptoms="The typical mole is a brown spot. But moles come in different colors, shapes and sizes: \n 1. Color and texture. Moles can be brown, tan, black, red, blue or pink. They can be smooth, wrinkled, flat or raised. They may have hair growing from them. \n 2. Shape. Most..."
     treatement="Generally, it is very safe for your child’s doctor to simply watch a nevus sebaceous over time. This is especially true while your child is young (before puberty). A nevus sebaceous will not affect your child’s health, but you or your child may still want."
   elif res =='Dermatofibroma':
     id=6
     name="Dermatofibroma"
     description =" A dermatofibroma is a common benign fibrous nodule usually found on the skin of the lower legs.,A dermatofibroma is also called a cutaneous fibrous histiocytoma. "
     prevention="The preventive measures include: \n Sunscreen: While going out in the sun, apply sunscreen creams or lotions \n  Seek shade: Avoid going out during 10 am to 2 pm. Seek shade if you are exposed to sun for a longer time\n Cover your body: Protect your body from exposing it to sunlight. Wear protective clothing while going out on a sunny day \n Use extra caution near water or sand, as this can reflect sun rays"
     symptoms="Dermatofibromas usually develop slowly. These small, hard, raised skin growths: \nUsually appear on the lower legs, but may appear on the arms or trunk  \nMay be red, pink, purplish, gray or brown and may change color over time \nMay be as small as a BB pellet but rarely grow larger than a fingernail  \nAre often painless but may be tender, painful or itchy \nUsually dimple inward when pinched ."
     treatement="Dermatofibromas rarely require treatment. Some people may prefer to have their dermatofibromas removed if the growth is unsightly, is in an inconvenient location (such as in a place that repeatedly becomes nicked while shaving or is irritated by clothing), or is painful or itchy. \nBecause a dermatofibroma grows deep, removal requires excising it below the surface level of the skin. This process usually leaves a noticeable scar. Alternatively, the nodule may be flattened to the surface of the skin by shaving the top off with a surgical knife, but this removes only the top layers of the dermatofibroma, leaving the deeper layers so that the nodule may grow back again after several years. \nVery rarely, a certain skin cancer that initially resembles a dermatofibroma can spread. This skin cancer has a long name called a dermatofibrosarcoma protuberans (DFSP)."
   elif res =='Actinic keratoses and intraepithelial carcinomae':
     id=7
     name="Actinic keratoses and intraepithelial carcinomae"
     description =" Actinic keratoses (AKs) most commonly present as a white, scaly plaque of variable thickness with surrounding redness; they are most notable for having a sandpaper-like texture when felt with a gloved hand. Skin nearby the lesion often shows evidence of solar damage characterized by notable pigmentary alterations, being yellow or pale in color with areas of hyperpigmentation; deep wrinkles, coarse texture, purpura and ecchymoses, dry skin, and scattered telangiectasias are also characteristic."
     prevention="The preventive measures include: \n Sunscreen: While going out in the sun, apply sunscreen creams or lotions \n  Seek shade: Avoid going out during 10 am to 2 pm. Seek shade if you are exposed to sun for a longer time\n Cover your body: Protect your body from exposing it to sunlight. Wear protective clothing while going out on a sunny day \n Use extra caution near water or sand, as this can reflect sun rays"
     symptoms="The symptoms include:\nThe earliest symptom is typically a change in an existing mole or a new mole arising\nThe development of a new pigmented or unusual-looking growth on your skin\nThe below mentioned strategies helps discriminate the melanoma from other skin cancers. The ABCDE’s of melanoma helps identify the disease condition\nAsymmetry: The mole may not be uniform, one half looks different from the other half\nBorder irregularity: The moles may be uneven or notched\nColor: The moles may be of different colors and irregular patterns\nDiameter: The mole may be bigger in size, at least a 6mm size\nEvolving: The mole may be changing colors, size and texture and might also bleed\nEvolving: The mole may be changing colours, size and texture and might also bleed"
     treatement="Chemotherapy: Uses a combination of drugs to kill cancer cells."
    

   diseases  = {
      "_id": id,
      "name": name ,     
      "description":description,
      "prevention": prevention,
      "symptoms":symptoms,
      "treatement":treatement

    }
       db.diseases.insert_one(diseases)                 دي لو عايز تخزنها اوتوماتك  وتحذفها اول ما الامراض كلها تتسجل
      return self.start_session2(diseases)

    """


