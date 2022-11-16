import cv2
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template, request
from IPython.display import Audio
from playsound import playsound
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from twilio.rest import Client

app = Flask(__name__)

model = load_model('forest1.h5')


 
def predictImage(filename):
  img1=image.load_img(filename,target_size=(128,128))
  plt.imshow(img1)
  y=image.img_to_array(img1)
  x=np.expand_dims(y,axis=0)
  val=model.predict(x)
  print(val)
  if val==0:
    message="No Fire"
  elif val==1:
    account_sid='AC2eb1ef0f60792aa19ad09be1f89a8dba'
    auth_token='a428f3fd3bd8ded0d44a6c4cbdd1945f'
    client=Client(account_sid,auth_token)
    message=client.messages \
      .create(
          body="Forest fire is detected ,stay alert",
          from_='+1 314 948 5657',
          to='+91 9344099941')
    message="Fire"
  return message
		



# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")



@app.route("/about")
def about_page():
	return "Please subscribe  Artificial Intelligence Hub..!!!"

@app.route("/submit1", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)

		p = predictImage(img_path)

	return render_template("index.html", prediction = p, img_path = img_path)

@app.route("/submit2", methods = ['GET', 'POST'])
def new_get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)

		p = predictVideo(img_path)

	return render_template("index.html", prediction = p, img_path = img_path)


if __name__ =='__main__':
	
	app.run(debug=True)