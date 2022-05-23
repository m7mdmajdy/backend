  """"
  def upload(self):
    if request.method=="POST":
        imagefile=request.files['image']
        filename=werkzeug.utils.secure_filename(imagefile.filename)
        imagefile.save("./image/"+ filename)
        print('okstar')
        im="./image/"+ filename
        img = image.load_img(im, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])
        model_path = r"G:\New folder (10)/model (1) (1).h5"
        model = load_model(model_path)
        classes = model.predict(images)
        print(classes)
        classes_str = str(classes)
        match classes_str:
            case "[[0. 0. 0. 0. 0. 1.]]":
                result = 'Atopic Dermatitis'
            case "[[0. 0. 0. 0. 1. 0.]]":
                result = 'Melanocytic Nevi'
            case "[[0. 0. 0. 1. 0. 0.]]":
                result = 'Melanoma'
            case "[[0. 0. 1. 0. 0. 0.]]":
                result = 'Basal Cell Carcinoma'
            case "[[0. 1. 0. 0. 0. 0.]]":
                result = 'Benign Keratosis-like Lesions'
            case "[[1. 0. 0. 0. 0. 0.]]":
                result = 'Eczema' 
        
        print(result)
     
  
       # user= db.users.insert_one({"email":user,"result":result})
        db.users.update_one({"email":request.form.get('email')},{"$set":{"result":result}})

    return jsonify({'greetings' : f'Result ={result}'})
    """