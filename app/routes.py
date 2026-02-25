from flask import jsonify, request, render_template
from . import app
from .models import Job
from .database import db
from .services import save_job_to_db

# Home page route
@app.route('/')
def index():
    # Render the main dashboard template
    return render_template('index.html')


@app.route('/jobs', methods=['GET'])
def get_jobs():
    # Read optional query parameters (e.g., /jobs?status=applied&stacks=python)
    target_status = request.args.get('status')
    target_stack = request.args.get('stacks')

    # Start with a base query
    query = Job.query

    # Apply filters based on available query parameters
    if target_status:
        query = query.filter_by(status=target_status)
    if target_stack:
        query = query.filter(Job.stacks.contains(target_stack))

    # Execute query and serialize response
    jobs = query.order_by(Job.match_score.desc()).all()

    result = [{
        'id': job.id,
        'title': job.title,
        'match_score': job.match_score,
        'status': job.status.value,
        'stacks': job.stacks.split(',') if job.stacks else [],
        'location': job.location,
        'date': job.date.isoformat()
    } for job in jobs]

    return jsonify(result)

@app.route('/jobs', methods=['POST'])
def add_job():
  # Parse request body
  data = request.get_json()
  success, result = save_job_to_db(data)
  
  if success:
    # result is the new_job object
    return jsonify({'message': 'Job created', 'id': result.id}), 201
  else:
    # result is the error message string
    return jsonify({'error': result}), 409 


@app.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    # Fetch a single job by id or return 404
    job = Job.query.get_or_404(job_id)

    # Serialize selected fields
    result = {
        'id': job.id,
        'title': job.title,
        'company': job.company,
        'description': job.description,
        'url': job.url,
        'match_score': job.match_score,
        'feedback': job.feedback,
        'location': job.location,
        'date': job.date.isoformat()
    }

    return jsonify(result)


@app.route('/jobs/<int:job_id>/status', methods=['PUT'])
def update_job_status(job_id):
    # Load job and parse the new status from request body
    job = Job.query.get_or_404(job_id)
    new_status = request.json.get('status')

    # Validate required field
    if not new_status:
        return jsonify({'error': 'Status is required'}), 400

    # Persist status update
    job.status = new_status
    db.session.commit()

    return jsonify({'message': 'Job status updated successfully'}), 200


@app.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    # Delete a job by id
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()

    return jsonify({'message': 'Job deleted successfully'}), 200


@app.route('/jobs/<int:job_id>/feedback', methods=['POST'])
def add_job_feedback(job_id):
    # Load job and get feedback from request body
    job = Job.query.get_or_404(job_id)
    feedback = request.json.get('feedback')

    # Validate required field
    if not feedback:
        return jsonify({'error': 'Feedback is required'}), 400

    # Persist feedback update
    job.feedback = feedback
    db.session.commit()

    return jsonify({'message': 'Feedback added successfully'}), 200