from flask import Flask
from flask_oauth import OAuth

app = Flask(__name__)
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
    facebook.authorize(callback=url_for('crunch',
        next=request.args.get('next') or request.referrer or None))

@app.route('/crunch')
def crunch():
    if resp is None:
        flash(u'You denied the request to sign in.')
        return

    print session
    return session

if __name__ == "__main__":
    app.run()
