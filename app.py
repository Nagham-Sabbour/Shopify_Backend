from crypt import methods
import sqlite3 as sq
from distutils.log import debug
from flask import Flask, render_template, url_for, redirect, request

# Here we create a connection with the SQLite database and create the 2 tables "Merchants" and "Inventory"
# Merchants is a table made to be pre set up and verified so I already added 5 companies in there by using the commented out code
# Inventory is the table where are going to store the items created by the web app
# If you want to clear the Inventory table to start agian then uncomment "cursor.execute("DROP TABLE inventory")"
conn = sq.connect("logistics_comp.db")
cursor  = conn.cursor()

# cursor.execute("""CREATE TABLE IF NOT EXISTS merchants (company TEXT PRIMARY KEY,
#     pick_up_loc TEXT, size TEXT);""")

# cursor.execute("INSERT INTO merchants (company, pick_up_loc, size) VALUES ('Shopify', 'Mississauga', 'Large');")
# cursor.execute("INSERT INTO merchants (company, pick_up_loc, size) VALUES ('Clothing Retailer', 'Vaughan', 'Small');")
# cursor.execute("INSERT INTO merchants (company, pick_up_loc, size) VALUES ('Product Warehouse', 'Mississauga', 'Large');")
# cursor.execute("INSERT INTO merchants (company, pick_up_loc, size) VALUES ('Small Bussiness', 'USA', 'Small');")
# cursor.execute("INSERT INTO merchants (company, pick_up_loc, size) VALUES ('Car Manufacturer', 'Japan', 'Large');")

# cursor.execute("DROP TABLE inventory")
cursor.execute("""CREATE TABLE IF NOT EXISTS inventory (item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    warehouse_id INTEGER, item_count INTEGER, company INTEGER, drop_off_loc TEXT, 
    FOREIGN KEY (company) 
      REFERENCES merchants (company));""")

conn.commit()
conn.close()


app = Flask(__name__)

# This is the landing/ main page of the webpage where it connects to the database
# and accesses all the data in inventory to display it in the form of a table
@app.route('/')
def home():
    conn = sq.connect("logistics_comp.db")
    cursor  = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    data = cursor.fetchall()
    conn.commit()
    conn.close()

    return render_template("home.html", inventory=data)


# This function is called on when we search for any filters
# It uses the filter value to detirmin what to display in the table 
# "None" displays all the shipments
# "Item Count (100+)" diplays any shipment that has more than a 100 items
# "Company Size (Large)" displays the shipments made by large companies
# the size of the company is a caegory found in the merchants database 
@app.route('/', methods=['POST'])
def filter():
    conn = sq.connect("logistics_comp.db")
    cursor  = conn.cursor()

    if (request.form["filter"] == "none"):
        cursor.execute("SELECT * FROM inventory")
        data = cursor.fetchall()

    elif(request.form["filter"] == "Item Count (100+)"):
        cursor.execute("SELECT * FROM inventory WHERE item_count>= 100")
        data = cursor.fetchall()

    elif(request.form["filter"] == "Company Size (Large)"):
        cursor.execute("SELECT company FROM merchants Where size= 'Large'")
        large_comp = cursor.fetchall()

        data=[]
        for comp in large_comp:
            cursor.execute("SELECT * FROM inventory Where company= '%s'" % (comp[0]))
            list = cursor.fetchall()
            for item in list:
                data.append(item)

    conn.commit()
    conn.close()

    return render_template("home.html", inventory=data)

# This function loads the create page and loads the drop down Company menu from the merchants database
@app.route('/create')
def goToCreate():
    conn = sq.connect("logistics_comp.db")
    cursor  = conn.cursor()
    cursor.execute("SELECT company FROM merchants")
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return render_template("create.html", merchants=data)


# This function retrives all the data inputs from create page when you click submit
# It also handles redirecting you to the main page weather you click "Cancel" or "Submit"
# This fuction also has a try block to handle the exception if any of the parameters are left empty
@app.route('/create', methods=["POST"])
def create():
    try:
        if (request.method == "POST"):
            if (request.form["Button"] == "Cancel"):
                return redirect("/")

            else:
                conn = sq.connect("logistics_comp.db")
                cursor  = conn.cursor()

                warehouse_id = request.form['warehouse_id']
                item_count = request.form['item_count']
                company = request.form['company']
                drop_off_loc = request.form['drop_off_loc']
                
                sql ="INSERT INTO inventory(warehouse_id, item_count, company, drop_off_loc) VALUES (%s, %s, '%s', '%s')"
                val = (warehouse_id, item_count, company, drop_off_loc)
                
                cursor.execute(sql % val)
                conn.commit()
                conn.close()
                return redirect("/")
    except:
        return redirect("/create")


# This delete function retrieves an id as a parameter from the frontend to know which item to remove
# Each item has a unique id that is auto incremented to prevent any errors
# It then reruns the main page viewing function to update and remove the deleted entry
@app.route('/delete/<id>')
def delete(id):
    print(id)
    conn = sq.connect("logistics_comp.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE item_id = %s" % (id))
    conn.commit()
    conn.close()
    return redirect("/")


# This function loads the update page and loads the drop down Company menu from the merchants database
# It also retrieves an id as a parameter from the frontend to know which item to update
# I also cretaed a global variable "temp_id" to be able to refrence it in the coming "update" function
@app.route('/update/<id>')
def goToUpdate(id):
    conn = sq.connect("logistics_comp.db")
    cursor  = conn.cursor()
    cursor.execute("SELECT company FROM merchants")
    data = cursor.fetchall()
    
    global temp_id
    temp_id = id
    item = cursor.execute("SELECT * FROM inventory WHERE item_id=%s" %(id))

    return render_template("update.html", inventory=item, merchants=data)


# The update funtion looks very similar to the create function with just the addition of dispalying and 
# using the global variable temp_id to know which item to edit
@app.route('/update', methods=["POST"])
def update():
    try:
        if (request.method == "POST"):
            if (request.form["Button"] == "Cancel"):
                return redirect("/")
            else:
                conn = sq.connect("logistics_comp.db")
                cursor  = conn.cursor()

                warehouse_id = request.form['warehouse_id']
                item_count = request.form['item_count']
                company = request.form['company']
                drop_off_loc = request.form['drop_off_loc']

                sql = "UPDATE inventory SET warehouse_id = %s, item_count = %s, company = '%s', drop_off_loc = '%s' WHERE item_id = %s"
                val = (warehouse_id, item_count, company, drop_off_loc, temp_id)
                
                cursor.execute(sql % val)
                conn.commit()
                conn.close()
                return redirect("/")
    except:
        return redirect(url_for('goToUpdate', id=temp_id))


if __name__ == "__main__" :
    app.run(debug= True)