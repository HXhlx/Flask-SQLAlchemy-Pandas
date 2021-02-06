import sys

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from pandas import read_sql_table
from sqlalchemy import and_

from app.auth import login_required
from app.models import Passengers, db

home = Blueprint('home', __name__, url_prefix='/home')


def dataframe2list(data0, col):
    my_dict = data0.groupby(col).count().iloc[:, 0].to_dict()
    return [list(my_dict.keys()), list(my_dict.values())]


@home.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('home/home.html')


@home.route('/details')
@login_required
def details():
    passenger_search = [
        Passengers.PassengerId.like(f"%{request.args['PassengerId']}%"),
        Passengers.Pclass.like(f"%{request.args['Pclass']}%"),
        Passengers.Name.like(f"%{request.args['Name']}%"),
        Passengers.Sex.like(f"%{request.args['Sex']}%"),
        Passengers.SibSp.like(f"%{request.args['SibSp']}%"),
        Passengers.Parch.like(f"%{request.args['Parch']}%"),
        Passengers.Ticket.like(f"%{request.args['Ticket']}%")
    ]
    if request.args['Survived']:
        passenger_search.append(Passengers.Survived == eval(request.args['Survived']))
    if request.args['Age']:
        passenger_search.append(Passengers.Age.like(f"%{request.args['Age']}%"))
    if request.args['Cabin']:
        passenger_search.append(Passengers.Cabin.like(f"%{request.args['Cabin']}%"))
    if request.args['Embarked']:
        passenger_search.append(Passengers.Embarked.like(f"%{request.args['Embarked']}%"))
    if request.args['Fare']:
        passenger_search.append(Passengers.Fare.like(f"%{request.args['Fare']}%"))
    passengers = list(map(dict, Passengers.query.filter(and_(*passenger_search))))
    return jsonify(passengers)


@home.route('/insert', methods=['POST'])
@login_required
def insert():
    try:
        Passenger = Passengers(**request.form)
        db.session.add(Passenger)
        db.session.commit()
        return redirect(url_for('home.index'))
    except:
        return render_template('home/home.html', error=sys.exc_info())


@home.route('/<passenger_id>')
@login_required
def passenger(passenger_id):
    data = read_sql_table('passengers', db.session.bind)
    passenger_data = data.iloc[int(passenger_id) - 1, [1, 2, 5, 6, 7, 9]].fillna(0).to_list()
    passenger_max = data.max().iloc[[1, 2, 5, 6, 7, 9]].to_dict()
    passenger_max['Pclass'] = 1
    passenger_max['Survived'] = 1
    passenger_data[1] = 1 / passenger_data[1]
    passenger_data[0] = 1 if passenger_data[0] else 0
    return render_template('home/passenger.html',
                           passenger=Passengers.query.filter_by(PassengerId=passenger_id).first(),
                           passenger_max=passenger_max,
                           passenger_data=passenger_data)


@home.route('/stats')
@login_required
def stats():
    data = read_sql_table('passengers', db.session.bind)
    return render_template('home/stats.html',
                           embarks=data.groupby('Embarked').count().iloc[:, 0].to_dict(),
                           survive=data.groupby('Survived').count().iloc[:, 0].to_dict(),
                           pclass=data.groupby('Pclass').count().iloc[:, 0].to_dict(),
                           sex=data.groupby('Sex').count().iloc[:, 0].to_dict(),
                           sibsp=dataframe2list(data, 'SibSp'),
                           parch=dataframe2list(data, 'Parch'),
                           age=dataframe2list(data.round(), 'Age'),
                           ticket=dataframe2list(data, 'Ticket'),
                           fare=dataframe2list(data.round(), 'Fare'))
