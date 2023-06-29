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
purchaseRecap = {}

app = Flask(__name__)
app.secret_key = "something_special"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    currentDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    email = request.form["email"]
    try:
        club = [club for club in clubs if club["email"] == email][0]
    except IndexError:
        flash("Invalid email address")
        return redirect(url_for("index"))
    else:
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions,
            currentDate=currentDate,
        )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    currentDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]

    if foundClub and foundCompetition and foundCompetition["date"] > currentDate:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions,
            currentDate=currentDate,
        )


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

    todayDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # control for total purchases of club in comp
    alreadyPurchasedPlaces = 0
    if purchaseRecap.get(competitionName) is not None:
        competitionPurchaseRecap = purchaseRecap[competitionName][0]

        if competitionPurchaseRecap.get(clubName) is not None:
            alreadyPurchasedPlaces = int(competitionPurchaseRecap[clubName])
        else:
            purchaseRecap[competitionName].append(
                {clubName: str(alreadyPurchasedPlaces)}
            )
    else:
        purchaseRecap[competitionName] = [{clubName: str(alreadyPurchasedPlaces)}]

    totalPurchasedPlaces = alreadyPurchasedPlaces + placesRequired

    # logic for booking
    if todayDate > competition["date"]:
        flash(f"This competition is over.")
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions,
            currentDate=todayDate,
        )
    elif alreadyPurchasedPlaces == 12:
        flash("You have already booked the maximum allowed numbers of places.")
        return render_template(
            "welcome.html", club=club, competitions=competitions, currentDate=todayDate
        )
    elif int(club["points"]) < placesRequired:
        flash(f"Not enough points, you can only book {club['points']} places")
        return render_template(
            "welcome.html", club=club, competitions=competitions, currentDate=todayDate
        )

    elif placesRequired > int(competition["numberOfPlaces"]):
        flash(
            f"There is only {competition['numberOfPlaces']} available for this competiton."
        )
        return render_template(
            "welcome.html", club=club, competitions=competitions, currentDate=todayDate
        )
    elif totalPurchasedPlaces > 12:
        flash("You can not book more than 12 places for any competition.")
        return render_template(
            "welcome.html", club=club, competitions=competitions, currentDate=todayDate
        )

    else:
        updatedClubPoints = int(club["points"]) - placesRequired
        updatedCompetitionPlaces = int(competition["numberOfPlaces"]) - placesRequired

        # updatating loaded competitions & clubs global
        competitions[competitionIndex]["numberOfPlaces"] = str(updatedCompetitionPlaces)
        clubs[clubIndex]["points"] = str(updatedClubPoints)

        # adding key/value to count how many places a club purchases for a competition, even if doig multiple purchases.
        purchaseRecap[competitionName][0][clubName] = str(totalPurchasedPlaces)

        flash("Great-booking complete!")
        return render_template(
            "welcome.html", club=club, competitions=competitions, currentDate=todayDate
        )


@app.route("/dashboard")
def dashboard():
    return render_template("board.html", clubs=clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
