import json
from flask import Flask,render_template,request,redirect,flash,url_for, session
from datetime import datetime

def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

now = datetime.now()

@app.route('/')
def index():
    return render_template('index.html',pageName="Home")

@app.route('/resume')
def resume():
    try:
        club = [club for club in clubs if club['email'] == session.get('user_p11')][0]
    except Exception as e:
        return render_template('index.html',pageName="Home", login=False)
    for comp in competitions:
        date_comp = datetime(int(comp['date'][:4]), int(comp['date'][5:7]), int(comp['date'][8:10]))
        if now > date_comp:
            comp['passed'] = True
        else:
            comp['passed'] = False
    return render_template('welcome.html',club=club,competitions=competitions, pageName="Resume")


@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        session['user_p11'] = request.form['email']
    except Exception as e:
        return render_template('index.html',pageName="Home", login=False)
    for comp in competitions:
        date_comp = datetime(int(comp['date'][:4]), int(comp['date'][5:7]), int(comp['date'][8:10]))
        if now > date_comp:
            comp['passed'] = True
        else:
            comp['passed'] = False
    return render_template('welcome.html',club=club,competitions=competitions, pageName="Resume")



@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition, pageName="book")
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions, pageName="book")


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if placesRequired > 12:
        return render_template('booking.html',club=request.form['club'],competition=request.form['competition'],pageName="book",p_fail=True)
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/displayPoints')
def displayPoints():
    return render_template('display.html', clubs=clubs, pageName="Display")

@app.route('/logout')
def logout():
    session.pop('user_p11', None)
    return redirect(url_for('index'))