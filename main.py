from flask import Flask, render_template, g, session, request, redirect, url_for, flash
from assets_blueprint import assets_blueprint
import flask,  urllib.parse
from flask_session import Session
import hashlib


# Dummy database of users
PSW_FILE="./psw.d"

PSW_DATA = open(PSW_FILE)
PSW_DATA =  [l.strip() for l in PSW_DATA]

# Set up application.
app = Flask(
    __name__,
    static_url_path="/",
    static_folder="public",
    template_folder="templates",
)
sess = Session()
app.secret_key = 'super secret key' 
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)

# Provide Vite context processors and static assets directory.
print("assets_blueprint: ", assets_blueprint)
app.register_blueprint(assets_blueprint)




# Setup application routes.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")       
        user_psw = f"{username}:{password}"
        psw = hashlib.sha256(user_psw.encode('utf8')).digest().hex()
        
        print(f"username : {username}, password : {password}, psw ; {psw}")
 # Check credentials (you'll replace this with your own logic)
        if psw in PSW_DATA:
            session['logged_in'] = True
            session['user_id'] = username
            return redirect(url_for("homepage"))
        else:
            flash('Wrong username or password')
            #return 'Invalid username/password combination'
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Remove all keys from the session dictionary
    session.clear()
    return redirect(url_for('login'))


@app.get("/")
def homepage():
    if not 'logged_in' in session:
        return redirect(url_for('login'))

    base_url = flask.request.base_url
    hostname = str(urllib.parse.urlparse(base_url).hostname)
    session["base_url"] = base_url
    session["hostname"] = hostname

    msg =  f"base_url:{base_url}, hostname:{hostname}"
    print("msg: ", msg)
    return render_template("homepage.html")


# Start the app if the file is run directly.
if __name__ == "__main__":
    app.run()
