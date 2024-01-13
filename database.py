from sqlalchemy import create_engine, text
from flask import request
import os

#below has been changed for github, you need to insert your information that was given by your AWS Cloud (ex: planetscale) or MySQL server
db_connection = "mysql+pymysql://<username>:<password>@<host>/<dbname>?charset=utf8mb4"

#connect to our mysql database
engine = create_engine(db_connection,
                      connect_args={
                        "ssl": {
                          "ssl_ca": "/etc/ssl/cert.pem"
                        }
                      })

with engine.connect() as conn: 
  result = conn.execute(text("SELECT * FROM jobs"))


def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))

    # Fetch the column names from the result set
    columns = result.keys()

    # Create a list of dictionaries from the result set
    jobs = [dict(zip(columns, row)) for row in result]
    
    return jobs

def load_job_from_db(job_id):
  with engine.connect() as conn:
    # Get job with ID from the jobs table using parameter binding
    query = text("SELECT * FROM jobs WHERE id = :job_id")
    result = conn.execute(query, {'job_id': job_id})

    row = result.fetchone()
    # If the job with the specified ID exists, return it as a dictionary
    if row:
        columns = result.keys()
        job_dict = dict(zip(columns, row))
        return job_dict

  return None

#Adding data into our table 
def add_application_to_db(job_id, data):
  with engine.connect() as conn:
    #have form request variables
    query = text(f"INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES ({job_id}, '{data['full_name']}', '{data['email']}', '{data['linkedin_url']}', '{data['education']}', '{data['work_experience']}', '{data['resume_url']}')")

    conn.execute(query)


  
