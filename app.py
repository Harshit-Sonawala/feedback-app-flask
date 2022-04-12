from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sendmail import send_mail

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
  app.debug = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/feedbacksys'
else:
  app.debug = False
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/feedbacksys'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
  __tablename__ = 'feedbackdata'
  id = db.Column(db.Integer, primary_key=True)
  student_name = db.Column(db.String(100))
  student_email = db.Column(db.String(100))
  student_year = db.Column(db.String(30))
  student_rating = db.Column(db.Integer)
  student_comment = db.Column(db.Text())

  def __init__(self, student_name, student_email, student_year, student_rating, student_comment):
    self.student_name = student_name
    self.student_email = student_email
    self.student_year = student_year
    self.student_rating = student_rating
    self.student_comment = student_comment

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
  if request.method == 'POST':
    student_name = request.form['student_name']
    student_email = request.form['student_email']
    student_year = request.form['student_year']
    student_rating = request.form['student_rating']
    student_comment = request.form['student_comment']
    # print(f'Name: ${student_name}\nEmail: {student_email}\nYear: {student_year}\nRating: {student_rating}\nComment: {student_comment}')
    if student_name == '' or student_email == '' or student_year == '' or '@' not in student_email:
      return render_template('index.html', message='Please enter all the required fields correctly.')
    if db.session.query(Feedback).filter(Feedback.student_name == student_name).count() == 0:
      data_to_submit = Feedback(student_name, student_email, student_year, student_rating, student_comment)
      db.session.add(data_to_submit)
      db.session.commit()
      send_mail(student_name, student_email, student_year, student_rating, student_comment)
      return render_template('success.html')
    return render_template('index.html', message='You can only submit feedback once per user.')

if __name__ == '__main__':
  app.debug = True
  app.run()