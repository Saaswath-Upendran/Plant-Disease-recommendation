from django.shortcuts import render
from .forms import PredictionForm
from django.http import HttpResponse
from .vi_transformer import create_vit_classifier
import pickle
import numpy as np
import tensorflow as tf
from PIL import Image
from io import BytesIO
# Create your views here.
with open(r'D:\saaswath\projects\plant disease and recommandation\resultmap.pkl','rb') as f:
    resultmap = pickle.load(f)
with open(r'D:\saaswath\projects\plant disease and recommandation\recommdationmap.pkl','rb') as f:
    recommdation = pickle.load(f)

img_width, img_height = 224, 224
vision_transformer = create_vit_classifier()
vision_transformer.load_weights(r"D:\saaswath\projects\plant disease and recommandation\model\checkpoint.weights.h5")
def home(request):
    return render(request,"home.html")


def PredictionView(request):
    p_completed = False
    disease_type = ''
    recommendation = ''
    if request.method == 'POST':
        form = PredictionForm(request.POST,request.FILES)
        if form.is_valid():
            name = request.FILES['upload_image']
            # load the image
            img = tf.keras.utils.load_img(BytesIO(name.read()), target_size = (img_width, img_height))

            # convert the image to a numpy array
            img = tf.keras.utils.img_to_array(img)
            # expand dimensions so the model can accept the image as input
            img = np.expand_dims(img, axis = 0)
            # make the prediction
            prediction = vision_transformer.predict(img)
            final_pred = np.argmax(prediction)
            disease = resultmap[final_pred]
            recommendations = recommdation[disease]
            return render(request,"upload.html",{
                "disease_type":disease,
                "recommendation": recommendations,
                p_completed : True
            })
        else:
            return HttpResponse("formFalied")
    else:
        form = PredictionForm()
        return render(request,'upload.html',context={'form':form,'p_completed':p_completed,'disease_type': disease_type,
        'recommendation': recommendation})