from flask import Flask, g, redirect, render_template, request, session, url_for, Response, jsonify


from my_user import Users


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