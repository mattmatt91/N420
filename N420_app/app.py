
from flask import Flask, g, redirect, render_template, request, session, url_for, Response, jsonify
from cam import Cam
import pandas as pd
import json as js
from growbox import Growbox, Lamp, Fan, Pot
from threading import Thread
import numpy as np
from picamera import PiCamera
from users import Users

###################################################################
# LOGIN 

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


    def __repr__(self):
        return {'User':self.username} 

users = []
for user in Users.users:
    users.append(User(id=user['id'], username=user['username'], password=user['pwd'])) 


##########################################################


app = Flask(__name__)
app.secret_key = Users.secret_key

Growbox.init_actuators()

###########################################################################################
@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

username = ''
password = ''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('video'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('login'))
# 
# 
#   @app.route('/')
#   def test():
#        return 'test'
# 
# ##########################################################################
@app.route('/')
def index():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('start.html')


@app.route("/data")
def start():
    if not g.user:
        return redirect(url_for('login'))
    data = Growbox.build_data()  # {'time':time.time()}
    return jsonify({"data": data})



###########################################################################################

functions = {'phase': Lamp.set_phase, 
    'time_start': Lamp.set_starttime,
    'irrigation_duration': Pot.set_irrigation_duration, 
    'irrigation_interval': Pot.set_irrigation_interval, 
    'soil_moist_hyst_max': Pot.set_soil_moist_hyst_max, 
    'soil_moist_hyst_min':  Pot.set_soil_moist_hyst_min,
    'hum_hyst_max': Fan.set_hum_hyst_max,
    'hum_hyst_min':  Fan.set_hum_hyst_min,
    'temp_hyst_max':  Fan.set_temp_hyst_max,
    'temp_hyst_min': Fan.set_temp_hyst_min}


@app.route("/preferences",methods=["GET", "POST"])
def preferences():
    if not g.user:
        return redirect(url_for('login'))
    data = Growbox.build_data()
    if request.method == "POST":   
            print(dict(request.form))    
            for i in request.form:
                print(functions[i])
                functions[i](request.form[i])
    
    return render_template('preferences.html', data=data)
    # return render_template('test.html')
  
########################################################################

def get_data(options):
    # print(options)
    with open(Growbox.path_data(), 'r') as f:
            data =[js.loads(i[i.find('{'): i.rfind('}')+1]) for i in f.readlines()]
            df = pd.DataFrame(data)
            lengthPlot = int(options.pop('days'))  
            lengthData = len(df.index)   
            index = lengthData-lengthPlot
            index = lengthData-lengthPlot
            thisData = df.iloc[index:][[i for i in options]]  
            try:
                max = thisData.select_dtypes(include=[np.number]).to_numpy().max()
                min = thisData.select_dtypes(include=[np.number]).to_numpy().min()
            except:
                max = 1
                min = 0
            for option in options:
                if thisData[option].iloc[0] == True or thisData[option].iloc[0] == False:
                    values = [max if i == True else min for i in thisData[option]]                
                    thisData[option] = values
            thisData['time'] = df['time'][index:]  
            thisData = thisData.reset_index().to_json(orient='records')     

            print(thisData)
            return(thisData)

##################################################################
@app.route('/plots/options',methods=["GET", "POST"])
def plots_options(): 
    if not g.user:
        return redirect(url_for('login')) 
    options = dict(request.form)
    data = get_data(options)
    # print(data)
    return data


@app.route('/plots')
def plots():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('plots.html')

################################################################



@app.route('/video_feed')
def video_feed():
    if not g.user:
        return redirect(url_for('login'))
    return Response(gen(Cam()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video')
def video():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('video.html')

def gen(cam):
    while True:
        frame =  cam.get_frame() #(0).to_bytes(2, byteorder='big')#
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == "__main__":
# 

    Thread(target=Growbox.main_loop).start()
    Cam.save_img_loop()
    app.run(host='0.0.0.0', port=8090, debug=False)
       
