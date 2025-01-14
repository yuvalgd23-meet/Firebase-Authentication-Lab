from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
# // For Firebase JS SDK v7.20.0 and later, measurementId is optional
# const firebase
Config = {
  "apiKey": "AIzaSyAN8UwgwzALWj-pSOnAahPiqsK3hPmGVN0",
  "authDomain": "yuvals-project-e0ce2.firebaseapp.com",
  "projectId": "yuvals-project-e0ce2",
  "storageBucket": "yuvals-project-e0ce2.appspot.com",
  "messagingSenderId": "448930320727",
  "appId": "1:448930320727:web:d0fa8e7e198f6de82fee12",
  "measurementId": "G-9HZD5RJY78",
  "databaseURL":"https://yuvals-project-e0ce2-default-rtdb.europe-west1.firebasedatabase.app/"
};

firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
	error = ''
	if request.method == 'POST':
		password = request.form['password']
		email = request.form['email']
		try:
			login_session['user'] =auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('home'))
		except:
			error = "Authentication failed"
	return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			user = {"name":request.form['full_name'],"username":request.form['username'], "email":request.form['email'],"password":request.form['password'], "bio":request.form['bio'] }
			db.child('user').child(login_session['user'])
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
	return render_template("signup.html")




@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
	if request.method == 'POST':
		try:
			tweet = {"title_t": request.form['title_t'],"tweet": request.form['tweet'], "uid":login_session['user']['localId']}
			db.child("Tweets").push(tweet)
			return redirect(url_for('all_tweets'))

		except Exception as e:
			raise
			return render_template("add_tweet.html", eror=str(e))

	return render_template("add_tweet.html")


@app.route('/all_tweets',methods=['get','post'])
def all_tweets():
	tweets = db.child("Tweets").get().val()
	return render_template("tweets.html", tweets = tweets)


	# return render_template("tweets.html", db.child("Tweets").child().get().val())

if __name__ == '__main__':
    app.run(debug=True)