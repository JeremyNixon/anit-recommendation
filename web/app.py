import flask
from flask_oauth import OAuth

app = flask.Flask(__name__)
app.debug = True
#app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'i&ACb>P_ECp^%WDQYBGNLkDh>nwvDi9WFRoX~HhSqGs5j.?|msaS%i|;mN{|%1%+'

oauth = OAuth()

FACEBOOK_APP_ID = '391076870930417'
FACEBOOK_APP_SECRET = '86ca5d474aec57d0ebb77288802c58ef'

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

@app.route("/")
def home():
    return "Hello World!"

@app.route('/login')
def login():
    return facebook.authorize(callback=flask.url_for('crunch', _external=True))

@app.route('/crunch')
@facebook.authorized_handler
def crunch(resp):
    if resp is None:
        flash(u'You denied the request to sign in.')
        return

    print resp
    return "You're logged in, bitch"

if __name__ == "__main__":
    app.run()
