import datetime 
from .database import db
from .enums import JobStatus

class Job(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(255), nullable=False)
  company = db.Column(db.String(255), nullable=False)
  description = db.Column(db.Text, nullable=False)
  url = db.Column(db.String(255), nullable=False)
  match_score = db.Column(db.Float, nullable=False, default=0.0)
  status = db.Column(db.Enum(JobStatus), nullable=False, default=JobStatus.PENDING)
  date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  def __repr__(self):
    return f'<Job {self.title} - score: {self.match_score} - status: {self.status.value}>'