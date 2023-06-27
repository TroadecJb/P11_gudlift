import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


competitions = loadCompetitions()
clubs = loadClubs()

app = Flask(__name__)
app.secret_key = "something_special"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
    except IndexError:
        flash("Invalid email address")
        return redirect(url_for("index"))
    else:
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]

    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )

    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    # competition related var
    competitionName = request.form["competition"]
    competition = [c for c in competitions if c["name"] == competitionName][0]
    competitionIndex = competitions.index(competition)

    # club related var
    clubName = request.form["club"]
    club = [c for c in clubs if c["name"] == clubName][0]
    clubIndex = clubs.index(club)

    # places related var
    placesRequired = int(request.form["places"])

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if (
        placesRequired < int(club["points"])
        and placesRequired <= 12
        and placesRequired < int(competition["numberOfPlaces"])
        and date < competition["date"]
    ):
        club["points"] = int(club["points"]) - placesRequired
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - placesRequired
        )

        # updatating loaded competitions & clubs global
        competitions[competitionIndex]["numberOfPlaces"] = str(
            competition["numberOfPlaces"]
        )
        clubs[clubIndex]["points"] = str(club["points"])

        flash("Great-booking complete!")
        return render_template("welcome.html", club=club, competitions=competitions)

    elif placesRequired > 12:
        flash(f"You can not book more than 12 places for any competition.")
        return render_template("welcome.html", club=club, competitions=competitions)

    elif placesRequired > int(competition["numberOfPlaces"]):
        flash(
            f"There is only {competition['numberOfPlaces']} available for this competiton."
        )
        return render_template("welcome.html", club=club, competitions=competitions)

    else:
        flash(f"Not enough points, you can only book {club['points']}.")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/dashboard")
def dashboard():
    return render_template("board.html", clubs=clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
