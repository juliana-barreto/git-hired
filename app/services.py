# Define target keywords for matching
from datetime import datetime

from flask import jsonify
from sqlalchemy.exc import IntegrityError
from app import db
from app.enums import JobStatus
from app.models import Job

# Define weighted keywords categorized by importance
TARGET_KEYWORDS = {
    'tech': {
        'java': 25.0,
        'spring boot': 20.0,
        'spring': 15.0,
        'python': 5.0,
        'react': 5.0
    },
    'seniority': {
        'junior': 20.0,
        'estagio': 15.0,
    },
    'role': {
        'backend': 15.0,
        'fullstack': 5.0
    }
}

# Function to calculate match score based on weighted categories
def calculate_match_score(title, description):
    score = 0.0
    found_stacks = []
    
    # Combine title and description for easier matching
    full_text = f"{title} {description}".lower()
    
    # Iterate through the dictionary to calculate the final score
    for category, keywords in TARGET_KEYWORDS.items():
        for keyword, weight in keywords.items():
            if keyword in full_text:
                score += weight
                found_stacks.append(keyword)

    # Return the final score capped at 100.0 and the list of found stacks
    return min(score, 100.0), found_stacks

# Function to save a job to the database
def save_job_to_db(job_data):

  # Validate required fields
  required_fields = ['title', 'company', 'description', 'url']
  for field in required_fields:
    if field not in job_data:
      return False, f'{field} is required'

  # Calculate the strategic match score
  score, found_stacks = calculate_match_score(job_data.get('title', ''), job_data.get('description', ''))
  
	job_date = datetime.now() # Default fallback
	raw_date = job_data.get('date')
	if raw_date:
			try:
					# Convert ISO format string to a Python datetime object
					job_date = datetime.fromisoformat(raw_date.replace('Z', '+00:00'))
			except ValueError:
					pass

  # Instantiate the Job model
  new_job = Job(
      title=job_data.get('title'),
      company=job_data.get('company'),
      description=job_data.get('description'),
      url=job_data.get('url'),
      match_score=score,
      status=JobStatus.PENDING,
      location=job_data.get('location'),
      date=job_data.get('date'),
      stacks=','.join(found_stacks)
  )
  
  try:
      # Attempt to insert into the database
      db.session.add(new_job)
      db.session.commit()
      return True, new_job
  except IntegrityError:
      # If the URL already exists, MySQL will throw an IntegrityError
      db.session.rollback()
      return False, "Job URL already exists"