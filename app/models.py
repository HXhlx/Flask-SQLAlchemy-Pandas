from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    UserID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Username = db.Column(db.String(10), nullable=False)
    Email = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, email, password):
        self.Username = username
        self.Email = email
        self.Password = password


class Passengers(db.Model):
    PassengerId = db.Column(db.SmallInteger, autoincrement=True, primary_key=True)
    Survived = db.Column(db.Boolean, nullable=False)
    Pclass = db.Column(db.SmallInteger, nullable=False)
    Name = db.Column(db.String(100), nullable=False)
    Sex = db.Column(db.Enum('male', 'female'), nullable=False)
    Age = db.Column(db.Float)
    SibSp = db.Column(db.SmallInteger, nullable=False)
    Parch = db.Column(db.SmallInteger, nullable=False)
    Ticket = db.Column(db.String(30), nullable=False)
    Fare = db.Column(db.Float)
    Cabin = db.Column(db.String(20))
    Embarked = db.Column(db.Enum('C', 'Q', 'S'))

    def __init__(self, PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked):
        self.PassengerId = eval(PassengerId)
        self.Survived = eval(Survived)
        self.Pclass = eval(Pclass)
        self.Name = Name
        self.Sex = Sex
        self.Age = eval(Age)
        self.SibSp = eval(SibSp)
        self.Parch = eval(Parch)
        self.Ticket = Ticket
        self.Fare = eval(Fare)
        self.Cabin = Cabin
        self.Embarked = Embarked

    def keys(self):
        return 'PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked'

    def __getitem__(self, item):
        return getattr(self, item)
