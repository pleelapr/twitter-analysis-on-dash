# Twitter Analysis on Dash

## What?
The project is created the prototype the dash project for twitter hashtag analysis.
 
## How to setup?
1. Clone the project to local
2. Open terminal at the project directory
3. Initialize gitrepo ```git init```
4. Create Python virtual environment ```virtualenv venv```
5. Activate Python virtual environment ```source venv/bin/activate``` for Mac and ```venv\Scripts\activate.bat``` for Windows
6. Install following Python Libraries:
```
pip install dash
pip install plotly
pip install pandas
pip install dash_bootstrap_components
pip install matplotlib
pip install pandasql
```
7. (Optional) check app.py files
8. (Optional) create .gitignore
9. (Optional) create Procfile for Heroku Deployment Note: app = app.py, server = server in app.py
10. (Optional) ```pip freeze > requirements.txt```
11. Install heroku cli
12. Initiate heroku and deploy
```
heroku login
heroku create <app-name>
git add .
git commit -m 'Initialize App'
git push heroku master
heroku ps:scale web=1 # run the app with a 1 heroku dyno
```
13. Update the code and redeploy
```
git status
git add .
git commit -m 'Description of Changes'
git push heroku master
```


