import time
from flask import Flask, render_template, request, session
import yaml

from mendeley import Mendeley
from mendeley.session import MendeleySession


with open('config/config.yml') as f:
    config = yaml.load(f)

REDIRECT_URI = 'http://localhost:5000/oauth'

app = Flask(__name__)
app.debug = True
app.secret_key = config['clientSecret']

mendeley = Mendeley(config['clientId'], config['clientSecret'], REDIRECT_URI)
token = None


@app.route('/')
def home():

    auth = mendeley.start_authorization_code_flow()
    session['state'] = auth.state

    return render_template('home.html', login_url=(auth.get_login_url()))


@app.route('/oauth')
def auth_return():
    global token
    auth = mendeley.start_authorization_code_flow(state=session['state'])
    mendeley_session = auth.authenticate(request.url)

    session.clear()
    session['token'] = mendeley_session.token
    token = mendeley_session.token
    shutdown_server()
    return "<p>Good</p>"


def get_session_from_cookies():
    global token
    while token is None:
        time.sleep(1)
    return MendeleySession(mendeley, token)


def start():
    app.run(host='0.0.0.0', use_reloader=False)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
