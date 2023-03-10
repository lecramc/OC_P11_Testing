import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime

def loadClubs():
    with open('clubs.json') as c:
        return json.load(c)['clubs']


def loadCompetitions():
    with open('competitions.json') as comps:
        return json.load(comps)['competitions']


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try :
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',club=club,competitions=competitions)
    except IndexError:
        return render_template('index.html', error="Email does not exist")

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if is_past_date(foundCompetition["date"]):
        flash("Cannot book past competitions")
        return render_template('welcome.html', club=club, competitions=competitions)
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if placesRequired > 12 :
        return render_template('booking.html', club=club, competition=competition, error="You cannot book more than 12 places")
    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        flash('Great-booking complete!')
        club["points"] = int(club["points"]) - placesRequired
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/pointsBoard', methods=['GET'])
def pointsBoard():
    return render_template('points_board.html', clubs=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))


def is_past_date(compet_date):
    date_format = "%Y-%m-%d %H:%M:%S"
    compet_date = datetime.strptime(compet_date, date_format)
    return compet_date < datetime.now()