from flask import Flask, render_template, g, session, request, redirect, url_for
from assets_blueprint import assets_blueprint
import flask,  urllib.parse
from flask_session import Session

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
        # Check credentials (you'll replace this with your own logic)
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['logged_in'] = True
            return redirect(url_for("homepage"))
        else:
            return 'Invalid username/password combination'
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
