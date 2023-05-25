from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# initialize the app
app = Flask(__name__)




ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password123@localhost:5432/foodmenu"
    
    # app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://username:password@localhost:port/DBNAME"
    
    # app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://<username>:<password>@localhost/<database_name>"
    
    db = SQLAlchemy(app)
    
    

    
else:
    app.debug =True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
    

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


with app.app_context():
        db.create_all()






class Meals(db.Model):
    __tablename__ = 'meal'
    id = db.Column(db.Integer, primary_key=True)
    mealname = db.Column(db.String(100), unique=True)
    mealtype = db.Column(db.String(100))

def __init__(self, mealname, mealtype):
    self.mealname = mealname
    self.mealtype = mealtype
    
    


@app.route('/')
def index():
    print("this actually works")
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    print("hello")
    if request.method == 'POST':
        mealname = request.form['mealname']
        print("meal name is working")
        mealtype = request.form['mealtype']
        print("meal type is working")
        # print("here is the print statement")
        # print(mealtype, mealtype)
        # how to get the print statement to show up in the console?
        
        
        
        return render_template('nextpage.html')

if __name__ == '__main__':
    # we want the server to keep reloading since we are in developerment so we keep this to true
    # app.debug = True
    app.run(host="0.0.0.0", port=3000)