from flask import Flask, render_template, jsonify
from JobDB import Job
from flask_sqlalchemy import SQLAlchemy
import settings
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./sqlite.data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def sa_obj_to_dict(obj):
    return {k: v for (k, v) in obj.__dict__.items() if not k.startswith('_')}

@app.route('/')
def index3():
    return render_template('index.html',LAT=settings.LAT,LNG=settings.LNG,RANK=settings.RANK)

@app.route('/api/jobs')
def jobs_json():

    jobs = [sa_obj_to_dict(j) for j in Job.query.all()]
    # print(jobs)
    return jsonify(error=0, total=len(jobs), items=jobs)

if __name__ == '__main__':
    # db.create_all()
    app.run(debug=False,port=8888)
