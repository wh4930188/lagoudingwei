from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)


class Job(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.String(40), primary_key=True)
    title = db.Column(db.String(40))
    company_name = db.Column(db.String(128))
    location = db.Column(db.String(128))
    ctime = db.Column(db.Integer)
    salary = db.Column(db.String(40))
    field = db.Column(db.String(40))
    company_size = db.Column(db.String(40))
    stage = db.Column(db.String(40))
    lng = db.Column(db.Float)
    lat = db.Column(db.Float)
    gis_loc = db.Column(db.String(128))
    jid = db.Column(db.Integer)

    def __init__(self, job_id):
        self.id = job_id

    def __repr__(self):
        return '<Job %r %r>' % (self.company_name, self.salary)
