from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bhava@04",   # 👈 Inga unga MySQL password podunga
    database="bus_tracking"
)

cursor = db.cursor()

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/check_login', methods=['POST'])
def check_login():

    username = request.form['username']
    password = request.form['password']

    if username == "admin" and password == "admin123":
        return redirect('/dashboard')
    else:
        return "Invalid Username or Password"


@app.route('/dashboard')
def dashboard():

    cursor.execute("SELECT COUNT(*) FROM buses")
    total_buses = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM buses WHERE status='Running'")
    active_buses = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(DISTINCT route) FROM buses")
    total_routes = cursor.fetchone()[0]

    return render_template(
        "dashboard.html",
        total_buses=total_buses,
        active_buses=active_buses,
        total_routes=total_routes
    )

@app.route('/tracking')
def tracking():
    return render_template('tracking.html')


@app.route('/add_bus')
def add_bus():
    return render_template('add_bus.html')


@app.route('/save_bus', methods=['POST'])
def save_bus():

    bus_number = request.form['bus_number']
    driver_name = request.form['driver_name']
    route = request.form['route']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    driver_mobile = request.form['driver_mobile']
    status = request.form['status']

    sql = """
    INSERT INTO buses
    (bus_number, driver_name, route, latitude, longitude, driver_mobile, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        bus_number,
        driver_name,
        route,
        latitude,
        longitude,
        driver_mobile,
        status
    )

    cursor.execute(sql, values)
    db.commit()

    return """
    <h2 style='color:green;text-align:center;'>✅ Bus Added Successfully!</h2>

    <center>
        <a href="/dashboard">
            <button>Go to Dashboard</button>
        </a>
    </center>
    """
@app.route('/view_buses')
def view_buses():

    cursor.execute("SELECT * FROM buses")
    buses = cursor.fetchall()

    return render_template("view_buses.html", buses=buses)
@app.route('/delete_bus/<int:id>')
def delete_bus(id):

    sql = "DELETE FROM buses WHERE id=%s"
    value = (id,)

    cursor.execute(sql, value)
    db.commit()

    return redirect('/view_buses')
@app.route('/edit_bus/<int:id>')
def edit_bus(id):

    cursor.execute("SELECT * FROM buses WHERE id=%s", (id,))
    bus = cursor.fetchone()

    return render_template("edit_bus.html", bus=bus)


@app.route('/update_bus/<int:id>', methods=['POST'])
def update_bus(id):

    bus_number = request.form['bus_number']
    driver_name = request.form['driver_name']
    route = request.form['route']
    driver_mobile = request.form['driver_mobile']
    status = request.form['status']

    sql = """
    UPDATE buses
    SET
        bus_number=%s,
        driver_name=%s,
        route=%s,
        driver_mobile=%s,
        status=%s
    WHERE id=%s
    """

    values = (
        bus_number,
        driver_name,
        route,
        driver_mobile,
        status,
        id
    )

    cursor.execute(sql, values)
    db.commit()

    return redirect('/view_buses')
@app.route('/search_bus', methods=['GET', 'POST'])
def search_bus():

    buses = []

    if request.method == 'POST':
        search = request.form['search']

        sql = """
        SELECT * FROM buses
        WHERE bus_number LIKE %s
           OR driver_name LIKE %s
           OR route LIKE %s
        """

        value = (
            '%' + search + '%',
            '%' + search + '%',
            '%' + search + '%'
        )

        cursor.execute(sql, value)
        buses = cursor.fetchall()

    return render_template("search_bus.html", buses=buses)

if __name__ == '__main__':
    app.run(debug=True)