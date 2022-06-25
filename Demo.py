from flask import Flask, render_template, request, redirect, url_for, session
import flask_session
import warnings
warnings.filterwarnings("ignore")
from datetime import date
import speech_recognition as spr
import mysql.connector
import joblib
import pyttsx3
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
flask_session.Session(app)
logindb = mysql.connector.connect(host='localhost', user='root', password='root', database="userLogin")
registerdb = mysql.connector.connect(host='localhost', user='root', password='root', database="userLogin")
coviddb = mysql.connector.connect(host='localhost', user='root', password='root', database="userLogin")
breastdb = mysql.connector.connect(host='localhost', user='root', password='root', database="userLogin")
loginCursor = logindb.cursor()
registerCursor = registerdb.cursor()
covidCursor = coviddb.cursor()
breastCursor = breastdb.cursor()
selQueryUID = "select * from userInfo"
loginCursor.execute(selQueryUID)
userids = loginCursor.fetchall()
today = date.today()
@app.route('/')
def home():
    # if not session.get('idd'):
    #     return redirect('/login')
    return render_template('home.html')
@app.route('/logout')
def logout():
    session['idd'] = None
    return redirect('/')
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        fname = request.form.get('fnamed')
        lname = request.form.get('lnamed')
        contact = request.form.get('ctd')
        city = request.form.get('cityd')
        email = request.form.get('idd')
        pas = request.form.get('passd')
        sqlQueryInsert = "insert into resgiterUser(fname, lname, contact,  city, email) values(%s,%s,%s,%s,%s)"
        value = (fname, lname, contact, city, email)
        registerCursor.execute(sqlQueryInsert, value)
        registerdb.commit()
        selQueryLogin = "insert into userInfo (uid,pass) values(%s, %s)"
        loginValue = (email, pas)
        loginCursor.execute(selQueryLogin, loginValue)
        logindb.commit()
        return redirect('/login')
    else:
        return render_template('regiter.html')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        uid = request.form.get('idd')
        passw = request.form.get('passd')
        loginCursor.execute(selQueryUID)
        userids = loginCursor.fetchall()
        for i in userids:
            if uid == i[0] and passw == i[1]:
                session["idd"] = request.form.get('idd')
                return redirect('/detection')
        else:
            return "enter valid crediential"
    else:
        return render_template('login.html')
data = {}
@app.route('/detection', methods=['GET', 'POST'])
def detection():
    if request.method == 'POST':
        text = request.form.get('originalurl')
        # text = "my name is "
        engine = pyttsx3.init()
        model = joblib.load('NLP.sav')
        lang = model.predict([text])  # predicting the language
        print("Given Text is :-", text)
        print("The langauge is in", lang[0])  # printing the language
        text1 = "you enter text is "+text
        data[text] = lang
        engine.say(text1)
        engine.say("detected language is  "+lang[0])
        engine.runAndWait()
        return render_template('index.html', ans=lang[0], original=text)
    return render_template('index.html')
@app.route('/history')
def history_get():
    return render_template('history.html', data=data.items())
@app.route('/texttosppech', methods=['GET', 'POST'])
def texttosppech():
    if request.method == 'POST':
      # initialize Text-to-speech engine
        engine = pyttsx3.init()
        # convert this text to speech
        # text = 'my name is '
        text = request.form.get('originalurl')
        engine.say(text)
        # play the speech
        engine.runAndWait()
        return render_template('texttospech.html')
    return render_template('texttospech.html')
@app.route('/speechtotext', methods=['GET', 'POST'])
def speechtotext():
    if request.method == 'POST':
        mc = spr.Microphone()
        recog1 = spr.Recognizer()
        MyText = "hello"
        # will recognise it.
        if 'hello' in MyText:
            with mc as source:
                print("Speak a stentence...")
                recog1.adjust_for_ambient_noise(source, duration=1)
                audio = recog1.listen(source, timeout=3, phrase_time_limit=3)
                get_sentence = recog1.recognize_google(audio)
                print("Phase to be Translated :" + get_sentence)
                try:
                    return render_template('converted.html', text=get_sentence)
                    print("Phase to be Translated :" + get_sentence)
                except:
                    print("Unable to locate")
    else:
        return render_template('converted.html')
if __name__ == "__main__":
    app.run(debug=True)
