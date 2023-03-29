import json
from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, url_for


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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    club = None
    for c in clubs:
        if c['email'] == email:
            club = c
            break
    if club is None:
        flash(f'This email: {email} does not exist')
        return render_template('index.html', club=club, competitions=competitions)
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    flash("Something went wrong-please try again")
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    today_date = datetime.now()
    date_formatted = today_date.strftime("%Y-%m-%d %H:%M:%S")
    if date_formatted < competition['date']:
        placesRequired = int(request.form['places'])
        if placesRequired > int(competition['numberOfPlaces']):
            flash('There is not enough places')
        elif placesRequired <= int(club['points']):
            if placesRequired <= 12:
                club['points'] = int(club['points']) - placesRequired
                competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
                flash('Great-booking complete!')
            else:
                flash('you book more than 12 places')
        else:
            flash('You do not have enough points to book!')
    else:
        flash('The competition has already passed')

    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/display')
def display():
    return render_template('display.html', my_table=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
