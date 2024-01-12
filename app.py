from flask import Flask, render_template, redirect, url_for, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_application_to_db

app = Flask(__name__)

@app.route("/")
def hello_hafsa():
  jobs = load_jobs_from_db()
  return render_template('home.html', 
                           jobs=jobs)

#@app.route("/api/jobs")
#@app.route('/jobs/<int:job_id>', methods=['GET'])
@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)

@app.route("/job/<job_id>")
def show_job(job_id):
    job = load_job_from_db(job_id)

    if not job:
        return "Job not found", 404

    return render_template('jobpage.html', job=job)


@app.route("/job/<id>")
def show_job_api(id):
  job = load_job_from_db(id)
  return jsonify(job)


#@app.route("/job/<int:id>/apply", methods=['GET', 'POST'])
@app.route("/job/<int:id>/apply", methods=['post'])
def apply_to_job(id):
  #get data from the form
  data = request.form
  #get job id (for HTML so we can print out job title)
  job = load_job_from_db(id)

  #add data to database
  add_application_to_db(id, data)
  
  return render_template('application_submitted.html', application=data, role=job)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
