from flask import Flask, render_template, request

import psycopg2

# initialize the app
app = Flask(__name__)


conn = psycopg2.connect(database="foodmenu", host="db", user="postgres", password="password123", port="5432")
# host originally = localhost, but I actually think this needs to change to be connected to the container
# for my db container, the hostname = be4ce484a6cb, so want to see if thatll work now

# now that I'm running docker compose, looks like host should actually be "db".  It should be db because this is the service name I chose for the database in my docker file


cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS meal (id serial PRIMARY KEY, mealname varchar(100), mealtype varchar(100));''' )
conn.commit()

# when exactly is a good time to close the connection with the database?
# Having trouble return back to the index page

@app.route('/')
def index():
    print("this actually works")
    cur.execute('''SELECT * FROM meal''')
    data = cur.fetchall()
    return render_template('index.html', data = data)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        mealname = request.form['mealname']
        print("meal name is working")
        print(type(mealname))
        mealtype = request.form['mealtype']
        print(type(mealtype[0]))
        print("meal type is working")

        cur.execute("INSERT INTO meal (mealname, mealtype) VALUES (%s, %s)", (mealname, mealtype))
        conn.commit()
        
        return render_template('nextpage.html')
    




if __name__ == '__main__':
    # we want the server to keep reloading since we are in developerment so we keep this to true
    # app.debug = True
    app.run(port=3000, host="0.0.0.0")