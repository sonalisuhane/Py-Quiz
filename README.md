# Py-Quiz
Python questionnaire to check your proficiency! <br>
The above project has been a group effort of Dilip Kotha & Sonali Suhane. <br> 

# File contents
### Page 1 : Index
Introduction to the webpage with links to login and register and about.
#### Page 1.1
Login page
#### Page 1.2
Registration page
#### Page 1.3
About Page
### Page 2 : Tests
#### Page 2.1
Beginner Quiz consisting of set of Multipile choice questions.
#### Page 2.2
Advacned Quiz consisting of set of short answer questions.
### Page 3: Previous Tests
Space to check the recently attempted test marks and feedback.
### AdminView
Space for the admin to set the question sets,<br>
review answer sets for questions given by the users and provide feedback.
#### Admin Functions available
Add or Edit or Delete Users <br>
Add or Edit or Delete Questions <br>
Mark answers <br>
Provide feedback to Users.

# Set Up and Running 
Install virtual environment by using:
#### python3 -m venv agile 

Then enter the virtual environment using:
#### On windows: agile/Scripts/activate
#### On Mac-os or Linux: source agile/bin/activate

Set the app to flask using:
#### On windows:set FLASK_APP=agile_web_flask.py
#### On Mac-os or Linux: export FLASK_APP=agile_web_flask.py

And install the requirements listed in requirements.txt:
#### pip install -r requirements.txt  

Once all packages are installed and the flask app is set, the app can be run using:
#### flask run

### Testing:
Unit tests can be run using the 
#### python -m unit.py

System tests can be run using
#### python -m system.py
