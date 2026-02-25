# Define target keywords for matching
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from app import db
from app.enums import JobStatus
from app.models import Job


TARGET_KEYWORDS = ['java', 'spring', 'spring boot', 'junior', 'estagio', 'backend', 'fullstack']

# Function to calculate match score based on keyword presence
def calculate_match_score(title, description):
    # Initialize the score
    score = 0.0
    
    # Combine title and description and convert to lowercase for easier matching
    full_text = f"{title} {description}".lower()
    
    # Loop through your keywords and add points if they exist in the text
    for keyword in TARGET_KEYWORDS:
        if keyword in full_text:
            score += 100.0 / len(TARGET_KEYWORDS)
    return min(score, 100.0)

# Function to save a job to the database
def save_job_to_db(job_data):

  # Validate required fields
  required_fields = ['title', 'company', 'description', 'url']
  for field in required_fields:
    if field not in job_data:
      return False, f'{field} is required'

  # Calculate the strategic match score
  score = calculate_match_score(job_data.get('title', ''), job_data.get('description', ''))
  
  # Instantiate the Job model
  new_job = Job(
      title=job_data.get('title'),
      company=job_data.get('company'),
      description=job_data.get('description'),
      url=job_data.get('url'),
      match_score=score,
      status=JobStatus.PENDING,
      date=job_data.get('date'),
      stacks=','.join(job_data.get('stacks', []))
  )
  
  try:
      # Attempt to insert into the database
      db.session.add(new_job)
      db.session.commit()
      return True, new_job
  except IntegrityError:
      # If the URL already exists, MySQL will throw an IntegrityError
      # We must rollback the session so the script doesn't crash
      db.session.rollback()
      return False, "Job URL already exists"