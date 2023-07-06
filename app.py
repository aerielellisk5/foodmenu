from flask import Flask, render_template, request

import psycopg2

# initialize the app
app = Flask(__name__)
conn = None


# # def get_db_connection():
#     conn = psycopg2.connect(host='localhost',
#                             database='flask_db',
#                             user=os.environ['DB_USERNAME'],
#                             password=os.environ['DB_PASSWORD'])
#     return conn


 
    # with psycopg2.connect(database="foodmenu", host="localhost", user="postgres", password="password123", port="5432") as conn:
    # host originally = localhost, but I actually think this needs to change to be connected to the container
    # for my db container, the hostname = be4ce484a6cb, so want to see if thatll work now

def get_db_connection():
    conn = psycopg2.connect(host='db',
                        database='foodmenu',
                        user="postgres",
                        password="password123",
                        port="5432")
    return conn

conn = get_db_connection()    
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS meal (id serial PRIMARY KEY, mealname varchar(100), mealtype varchar(100));''' )
conn.commit()
cur.close()
conn.close()
# for another day to adjust this create table
# when exactly is a good time to close the connection with the database?
# Having trouble return back to the index page

@app.route('/')
def index():
    conn = get_db_connection()
    print("this actually works")
    cur = conn.cursor()
    cur.execute('''SELECT * FROM meal''')
    data = cur.fetchall()
    cur.close()
    conn.close()
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
        
        conn = get_db_connection()    
        cur = conn.cursor()
        cur.execute("INSERT INTO meal (mealname, mealtype) VALUES (%s, %s)", (mealname, mealtype))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('nextpage.html')
    
    
# except Exception as error:
# # need to add the exceptions here
# print ("Oops! An exception has occured:", error)
# print ("Exception TYPE:", type(error))
# finally:
# if conn:
# conn.close()
# print("Closed connection.")




if __name__ == '__main__':
    # we want the server to keep reloading since we are in developerment so we keep this to true
    # app.debug = True
    app.run(port=3000, host="0.0.0.0")
    
    
    
    # eventually try to seperate the conecerns as far as database setup vs application