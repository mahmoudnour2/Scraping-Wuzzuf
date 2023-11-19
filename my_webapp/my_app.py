from flask import Flask,render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import text
from datetime import datetime
import string, datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+mysqlconnector://mahmoudnour2:Abdalla2008@db4free.net/wuzzuf_mahmoud'

db=SQLAlchemy(app)

class Company(db.Model):
    __tablename__ = 'company'

    name = db.Column(db.String(50), primary_key=True, nullable=False)
    website_url = db.Column(db.String(200))
    description = db.Column(db.String(2000))
    location = db.Column(db.String(100))
    city = db.Column(db.String(20))
    country = db.Column(db.String(20))
    size = db.Column(db.String(50))
    min_size = db.Column(db.String(10))
    max_size = db.Column(db.String(10))
    foundation_year = db.Column(db.Integer)


class CategoriesOfJob(db.Model):
    __tablename__ = 'categories_of_job'

    job_title = db.Column(db.String(50),  nullable=False)
    company_name = db.Column(db.String(50),  nullable=False)
    category = db.Column(db.String(50), nullable=False)

    job_posting= db.relationship('JobPosting', backref=db.backref('categories', lazy=True))
    
    __table_args__ = (
        PrimaryKeyConstraint('job_title', 'company_name', 'category'),
        ForeignKeyConstraint(['job_title', 'company_name'], ['job_posting.title', 'job_posting.company_name'])
    )

class JobPosting(db.Model):
    __tablename__ = 'job_posting'

    title = db.Column(db.String(50), nullable=False)
    enrollment_status = db.Column(db.String(50), nullable=True)
    company_name = db.Column(db.String(50), db.ForeignKey('company.name'), nullable=False)
    open_positions = db.Column(db.Integer, nullable=True)
    experience_needed = db.Column(db.String(50), nullable=True)
    career_level = db.Column(db.String(50), nullable=True)
    education_level = db.Column(db.String(50), nullable=True)
    salary = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(3000), nullable=True)
    job_requirment = db.Column(db.String(3000), nullable=True)
    min_salary = db.Column(db.String(10), nullable=True)
    max_salary = db.Column(db.String(10), nullable=True)
    work_from_home = db.Column(db.String(50), nullable=True)
    company= db.relationship('Company', backref=db.backref('job_postings', lazy=True))
    apply= db.relationship('Apply', backref=db.backref('job_posting', lazy=True))
    __table_args__ = (
        PrimaryKeyConstraint('title', 'company_name'),
    )
    
class SkillsAndToolsOfJob(db.Model):
    __tablename__ = 'skills_and_tools_of_job'

    job_title = db.Column(db.String(50), nullable=False)
    company_name = db.Column(db.String(50), nullable=False)
    skill_or_tool = db.Column(db.String(50), nullable=False)

    job_posting = db.relationship('JobPosting', backref=db.backref('skills_and_tools', lazy=True))
    
    __table_args__ = (
        PrimaryKeyConstraint('job_title', 'company_name', 'skill_or_tool'),
        ForeignKeyConstraint(['job_title', 'company_name'], ['job_posting.title', 'job_posting.company_name'])
    )


class CompanySectors(db.Model):
    __tablename__ = 'company_sectors'

    company_name = db.Column(db.String(50), db.ForeignKey('company.name'), nullable=False)
    sector = db.Column(db.String(50),  nullable=False)

    company = db.relationship('Company', backref=db.backref('sectors', lazy=True))

    __table_args__ = (
        PrimaryKeyConstraint('company_name', 'sector'),
    )  

class User(db.Model):
    __tablename__ = 'user'
    
    username = db.Column(db.String(20), primary_key=True, nullable=False)
    gender = db.Column(db.String(1), nullable=True)
    DOB = db.Column(db.Date, nullable=True)
    gpa = db.Column(db.Numeric(3, 2), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    applies = db.relationship('Apply', backref=db.backref('user', lazy=True))

class SkillsOfUser(db.Model):
    __tablename__ = 'skills_of_user'

    username = db.Column(db.String(20), db.ForeignKey('user.username'), primary_key=True, nullable=False)
    skill = db.Column(db.String(20), primary_key=True, nullable=False)

    user = db.relationship('User', backref=db.backref('skills', lazy=True))

class Apply(db.Model):
    __tablename__ = 'apply'
    cover_letter=db.Column(db.String(10000), nullable=True)
    username=db.Column(db.String(20), nullable=False)
    job_title=db.Column(db.String(50), nullable=False)
    company_name=db.Column(db.String(50), nullable=False)
    application_date=datetime.datetime.now()
    __table_args__ = (
        PrimaryKeyConstraint('job_title','company_name', 'username'),
        ForeignKeyConstraint(['job_title', 'company_name'], ['job_posting.title', 'job_posting.company_name']),
        ForeignKeyConstraint(['username'], ['user.username'])
    )  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query1_results', methods=['POST'])
def query1_results():
    username=request.form['query1a_input']
    gender=request.form['query1b_input']
    DOB=request.form['query1c_input']
    GPA=request.form['query1d_input']
    Email=request.form['query1e_input']
    username=str(username)
    gender=str(gender)
    DOB = datetime.datetime.strptime(DOB, '%Y-%m-%d').date()
    GPA=float(GPA)
    Email=str(Email)
    try:
        # SQL insert statement
        insert_query = text("INSERT INTO user (username, gender, DOB, gpa, email) VALUES ('{}', '{}', '{}', {}, '{}')".format(username, gender, DOB, GPA, Email))
        # Execute the insert query
        db.session.execute(insert_query)
        db.session.commit()
        return render_template('query1.html')
    except Exception as e:
        #print("Error:", str(e))
        return render_template('query1_failed.html')
    
@app.route('/query2_results', methods=['POST'])
def query2_results():
    job_title=request.form['query2a_input']
    company_name=request.form['query2b_input']
    username=request.form['query2c_input']
    cover_letter=request.form['query2d_input']

    job_title=str(job_title)
    cover_letter=str(cover_letter)
    username=str(username)
    job_title=str(job_title)
    company_name=str(company_name)
    application_date=datetime.datetime.now().strftime('%Y-%m-%d')

    try:
        # SQL insert statement
        insert_query = text(
        "INSERT INTO apply (job_title, company_name, username, application_date, cover_letter) "
        "VALUES (:job_title, :company_name, :username, :application_date, :cover_letter)"
        )

    # Bind parameters to the query
        parameters = {
        'job_title': job_title,
        'company_name': company_name,
        'username': username,
        'application_date': application_date,
        'cover_letter': cover_letter,
        }

    # Execute the query
        result = db.session.execute(insert_query, parameters)
    # Commit the transaction
        db.session.commit()
        return render_template('query2.html')
    except Exception as e:
        print("Error:", str(e))
        return render_template('query2_failed.html')


@app.route('/query3_results', methods=['POST'])
def query3_results():
    query_input=request.form['query3_input']
    # Perform your query here
    query = text("SELECT * FROM job_posting JP INNER JOIN company_sectors ON JP.company_name = company_sectors.company_name WHERE company_sectors.sector = :query_input")

    results = db.session.execute(query, {'query_input': query_input})
    
    
    return render_template('query3.html', job_postings=results)


@app.route('/query4_results', methods=['POST'])
def query4_results():
    query_input=request.form['query4_input']
    query_input_array = query_input.split(',')

    condition = "skills.skill_or_tool IN ({})".format(', '.join([':param{}'.format(i) for i in range(len(query_input_array))]))
   
    query = text("SELECT * FROM job_posting JP INNER JOIN skills_and_tools_of_job skills ON JP.title = skills.job_title WHERE {}".format(condition))
    
    params = {'param{}'.format(i): value for i, value in enumerate(query_input_array)}
    
    results = db.session.execute(query, params)
    row_count = results.rowcount
    print(row_count)

    return render_template('query4.html', job_postings=results)



@app.route('/query5_results', methods=['POST'])
def query5_results():
    query=text("SELECT sector, AVG(CASE WHEN max_salary > 0 AND min_salary > 0 THEN (max_salary + min_salary) / 2 ELSE NULL END) AS avg_salary from job_posting jp inner join company_sectors cs on jp.company_name = cs.company_name group by sector order by count(*) desc limit 5 ")
    results = db.session.execute(query)
    return render_template('query5.html', sectors=results)

@app.route('/query6_results', methods=['POST'])
def query6_results():
    query=text("Select skill_or_tool from skills_and_tools_of_job group by skill_or_tool order by count(*) desc limit 5 ")
    results = db.session.execute(query)
    return render_template('query6.html', skills=results)


@app.route('/query7_results', methods=['POST'])
def query7_results():
    query=text("Select company.name,sum(open_positions)/(2024- company.foundation_year) as vacancies_per_year from company inner join job_posting on company.name = job_posting.company_name group by company.name order by 2 desc limit 5")
    #the current year is set to 2024 to avoid division by zero in case a company is founded in 2023
    results = db.session.execute(query)
    return render_template('query7.html', companies=results)

@app.route('/query8_results', methods=['POST'])
def query8_results():
    query=text("Select sum((max_salary-min_salary)/2) as paying,company.name from company inner join job_posting JP on JP.company_name=company.name where company.country= \"Egypt\" group by company.name order by 1 desc limit 5")
    results = db.session.execute(query)
    return render_template('query8.html', companies=results)

@app.route('/query9_results', methods=['POST'])
def query9_results():
    query_input=request.form['query9_input']
    query=text("Select * from job_posting inner join company on company.name = job_posting.company_name where company.name = :query_input")
    results = db.session.execute(query, {'query_input': query_input})
    return render_template('query9.html', job_postings=results)

@app.route('/query10_results', methods=['POST'])
def query10_results():
    query=text("Select category from categories_of_job group by category order by count(*) desc limit 6")
    results = db.session.execute(query)
    return render_template('query10.html', categories=results)

if __name__ == '__main__':
    app.run(debug=True)