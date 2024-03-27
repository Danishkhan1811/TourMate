from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
# import mysql.connector
import MySQLdb.cursors
import re

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'tourmateproject.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'tourmateproject'
app.config['MYSQL_PASSWORD'] = 'tourmate18'
app.config['MYSQL_DB'] = 'tourmateproject$mydb'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/sign-up', methods=['GET','POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form and 'Email' in request.form :
        username = request.form['Username']
        password = request.form['Password']
        email = request.form['Email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s', (username, ))
        user = cursor.fetchone()
        if user:
            msg = 'You are already our Tour Mate!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s)', (password, email, username, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('login.html', msg = msg)
    # return ("signup successful")

@app.route('/login', methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']
            msg = 'Welcome Tour Mate. Let the journey begin!'
            return render_template('TourMate.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('landing.html')

@app.route('/main')
def main():
    return render_template('TourMate.html')

@app.route('/city')
def city():
    return render_template('city.html')

@app.route('/translate')
def translate():
    return render_template('translate.html')

@app.route('/weather')
def weather():
    return render_template('weather.html')

@app.route('/tourist')
def tourist():
    city = request.args.get('city_name') #get the name of the city when the tourist icon is clicked
    # data.city_name = city
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT name FROM tourist_spot WHERE location = % s",(city,)) #query tourist spot details corresponding to the city
    spot = cursor.fetchall()
    spot_names = [spot[i]['name'] for i in range(len(spot))]

    cursor.execute("SELECT image FROM tourist_spot WHERE location = %s",(city,))
    image=cursor.fetchall()
    image_display = [image[i]['image'] for i in range(len(image))]
    print(image_display)

    cursor.execute("SELECT description FROM tourist_spot WHERE location = % s",(city,)) #query tourist spot details corresponding to the city
    description = cursor.fetchall()
    desc = [description[i]['description'] for i in range(len(description))]

    cursor.execute("SELECT timings FROM tourist_spot WHERE location = % s",(city,)) #query tourist spot details corresponding to the city
    timings = cursor.fetchall()
    time = [timings[i]['timings'] for i in range(len(timings))]

    cursor.execute("SELECT address FROM tourist_spot WHERE location = % s",(city,)) #query tourist spot details corresponding to the city
    address = cursor.fetchall()
    addr = [address[i]['address'] for i in range(len(address))]

    return render_template('tourist.html',city_name=city,spot=spot_names,description=desc,image=image_display,timings=time,address=addr)



def generate_star_rating(rating):
    stars = int(rating)
    return '{}'.format(stars * '★')


@app.route('/restaurant')
def restaurant():
    city = request.args.get('city_name') #get the name of the city when the restaurant icon is clicked

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT name FROM restaurant WHERE location = % s",(city,)) #query restaurant details corresponding to the city
    restaurant = cursor.fetchall()
    names = [restaurant[i] for i in range(len(restaurant))]

    cursor.execute("SELECT type FROM restaurant WHERE location = % s",(city,)) #query restaurant details corresponding to the city
    type = cursor.fetchall()
    rest_type = [type[i]['type'] for i in range(len(type))]

    cursor.execute("SELECT image FROM restaurant WHERE location = %s",(city,))
    rest_image=cursor.fetchall()
    rest_image_display = [rest_image[i]['image'] for i in range(len(rest_image))]

    cursor.execute("SELECT id FROM restaurant WHERE location = % s",(city,))
    rest_id = cursor.fetchall()

    ids=[]
    for i in range(len(rest_id)):
        j = rest_id[i]['id']
        ids.append(j)
    print(ids)
    timing = []
    for i in range(len(ids)):
        cursor.execute("SELECT timing FROM rest_info WHERE id = % s",(ids[i],)) #query restaurant details corresponding to the city
        time = cursor.fetchone()
        timing.append(time)

    rest_time = [timing[i]['timing'] for i in range(len(timing))]

    address = []
    for i in range(len(ids)):
        cursor.execute("SELECT address FROM rest_info WHERE id = % s",(ids[i],)) #query restaurant details corresponding to the city
        addr = cursor.fetchone()
        address.append(addr)

    addr_info = [address[i]['address'] for i in range(len(address))]

    contact = []
    for i in range(len(ids)):
        cursor.execute("SELECT contact FROM rest_info WHERE id = % s",(ids[i],)) #query restaurant details corresponding to the city
        cont = cursor.fetchone()
        contact.append(cont)

    contact_info = [contact[i]['contact'] for i in range(len(contact))]

    ratings = []
    for i in range(len(rest_id)):
        cursor.execute("SELECT rating FROM rest_info WHERE id = % s",(ids[i],))
        rating = cursor.fetchone()
        ratings.append(rating['rating'])

    return render_template('restaurants.html',city_name=city,restaurant=names,type=rest_type,rest_image=rest_image_display,time=rest_time, addr=addr_info,rating=ratings,ids=ids,cont=contact_info)


@app.route('/hotel')
def hotel():
    city = request.args.get('city_name') #get the name of the city when the hotel icon is clicked

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT image FROM hotel WHERE location = %s",(city,))
    hotel_image=cursor.fetchall()
    hotel_image_display = [hotel_image[i]['image'] for i in range(len(hotel_image))]

    cursor.execute("SELECT name FROM hotel WHERE location = % s",(city,)) #query hotel details corresponding to the city
    hotel = cursor.fetchall()
    hotel_names = [hotel[i]['name'] for i in range(len(hotel))]

    cursor.execute("SELECT type FROM hotel WHERE location = % s",(city,)) #query hotel details corresponding to the city
    type = cursor.fetchall()
    hotel_type = [type[i]['type'] for i in range(len(type))]


    cursor.execute("SELECT hotel_id FROM hotel WHERE location = % s",(city,))
    hotel_id = cursor.fetchall()

    hotel_ids=[]
    for i in range(len(hotel_id)):
        j = hotel_id[i]['hotel_id']
        hotel_ids.append(j)

    hotel_address = []
    for i in range(len(hotel_ids)):
        cursor.execute("SELECT address FROM hotel_info WHERE hotel_id = % s",(hotel_ids[i],)) #query restaurant details corresponding to the city
        hotel_addr = cursor.fetchone()
        hotel_address.append(hotel_addr)

    hotel_address_info = [hotel_address[i]['address'] for i in range(len(hotel_address))]

    distance = []
    for i in range(len(hotel_ids)):
        cursor.execute("SELECT distance FROM hotel_info WHERE hotel_id = % s",(hotel_ids[i],)) #query restaurant details corresponding to the city
        dist = cursor.fetchone()
        distance.append(dist)

    hotel_dist = [distance[i]['distance'] for i in range(len(distance))]

    ratings = []
    for i in range(len(hotel_id)):
        cursor.execute("SELECT rating FROM hotel_info WHERE hotel_id = % s",(hotel_ids[i],))
        rating = cursor.fetchone()
        ratings.append(rating['rating'])

    hotel_price = []
    for i in range(len(hotel_ids)):
        cursor.execute("SELECT price FROM hotel_info WHERE hotel_id = % s",(hotel_ids[i],)) #query restaurant details corresponding to the city
        price = cursor.fetchone()
        hotel_price.append(price)

    hotel_price_display = [hotel_price[i]['price'] for i in range(len(hotel_price))]

    return render_template('hotel.html',city_name=city,hotel=hotel_names,hotel_image=hotel_image_display,type=hotel_type,hotel_addr=hotel_address_info,dist=hotel_dist,rating=ratings, price=hotel_price_display)

@app.route('/hotel-booking')
def hotel_booking():
    hotel = request.args.get('hotel_name')
    city = request.args.get('city_name')
    price = request.args.get('price')
    print(hotel)
    return render_template('hotel-booking.html',city_name=city,hotel_name=hotel,price=price)

@app.route('/add-booking', methods=['POST','GET'])
def add_booking():

    if request.method=='POST':
        hotel = request.args.get('hotel_name')
        price = request.args.get('price')
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        arrival_date = request.form['arrival-date']
        departure_date = request.form['departure-date']
        adults = request.form['adults']
        arrival_time = request.form['arrival-time']
        departure_time = request.form['departure-time']
        children = request.form['children']
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO bookings (name, email, mobile, arrival_date, departure_date, adults, arrival_time, departure_time, children,hotel_name,price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (name, email, mobile, arrival_date, departure_date, adults, arrival_time, departure_time, children,hotel,price))
            mysql.connection.commit()
            print('Booking added successfully', 'success')
            return redirect(url_for('booking_confirmation'))
        except Exception as e:
            print(f"An error occurred while adding the booking: {e}", 'error')
    return render_template('hotel-booking.html',city_name=city,hotel_name=hotel,price=price)


@app.route('/confirmation')
def booking_confirmation():
    return render_template('booking-confirmation.html')

@app.route('/cabs')
def cabs():
    city = request.args.get('city_name') #get the name of the city when the hotel icon is clicked

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT image FROM car_info WHERE location = %s",(city,))
    car_image=cursor.fetchall()
    car_image_display = [car_image[i]['image'] for i in range(len(car_image))]

    cursor.execute("SELECT car_name FROM car_info WHERE location = % s",(city,)) #query hotel details corresponding to the city
    car = cursor.fetchall()
    car_names = [car[i]['car_name'] for i in range(len(car))]

    cursor.execute("SELECT capacity FROM car_info WHERE location = % s",(city,)) #query hotel details corresponding to the city
    capacity = cursor.fetchall()
    cap = [capacity[i]['capacity'] for i in range(len(capacity))]

    cursor.execute("SELECT driver_name FROM driver_info WHERE location = % s",(city,)) #query hotel details corresponding to the city
    driver_name = cursor.fetchall()
    driver = [driver_name[i]['driver_name'] for i in range(len(driver_name))]

    cursor.execute("SELECT contact FROM driver_info WHERE location = % s",(city,)) #query hotel details corresponding to the city
    contact = cursor.fetchall()
    driver_contact = [contact[i]['contact'] for i in range(len(contact))]

    cursor.execute("SELECT fees FROM driver_info WHERE location = % s",(city,)) #query hotel details corresponding to the city
    fees = cursor.fetchall()
    driver_fees = [fees[i]['fees'] for i in range(len(fees))]

    cursor.execute("SELECT rating FROM driver_info WHERE location = % s",(city,)) #query hotel details corresponding to the city
    rating = cursor.fetchall()
    ratings = [rating[i]['rating'] for i in range(len(rating))]

    return render_template('cabs.html',city_name=city,car_image=car_image_display,car=car_names,capacity=cap,driver_name=driver,contact=driver_contact,fees=driver_fees,rating=ratings)



@app.route('/cab-booking')
def cab_booking():
    city = request.args.get('city_name')
    cab = request.args.get('car_name')
    driver = request.args.get('driver_name')
    fees = request.args.get('fees')
    return render_template('cab-booking.html',city_name=city,car_name=cab,driver_name=driver,fees=fees)

@app.route('/add-cab-booking', methods=['POST'])
def add_cab_booking():
    if request.method=='POST':
        cab = request.args.get('car_name')
        fees = request.args.get('fees')
        driver = request.args.get('driver_name')
        name = request.form['name']
        mobile = request.form['mobile']
        passenger = request.form['passenger']
        pickup_address = request.form['pick-up-address']
        destination = request.form['destination']
        departure_time = request.form['departure-time']
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO cab_bookings (name, mobile, passenger, pickup_address, destination, departure_time,driver_name,fees,car_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (name, mobile, passenger, pickup_address, destination, departure_time, driver, fees, cab))
            mysql.connection.commit()
            print('Booking added successfully', 'success')
            return redirect(url_for('booking_confirmation'))
        except Exception as e:
            print(f"An error occurred while adding the booking: {e}", 'error')
    return render_template('cab-booking.html',city_name=city)


# @app.route('/cab-confirmation')
# def cab_booking_confirmation():
#     return render_template('booking-confirmation.html')


#ADMIN PANEL

@app.route('/admin')
def tourist_spots():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tourist_spot")
    data = cur.fetchall()
    cur.close()
    return render_template('admin.html', data=data)

@app.route('/update_spot', methods=['POST'])
def update_spot():
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tourist_spot SET name=%s, description=%s, location=%s, image=%s, timings=%s, address=%s WHERE id=%s", (request.form['name'], request.form['description'], request.form['location'], request.form['image'], request.form['timings'], request.form['address'], request.form['id']))
    mysql.connection.commit()
    cur.close()
    return 'success'

@app.route('/delete_spot/<int:id>', methods=['POST'])
def delete_spot(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tourist_spot WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return 'success'

@app.route('/add_spot', methods=['POST'])
def add_spot():
    name = request.form['name']
    description = request.form['description']
    location = request.form['location']
    image = request.form['image']
    timings = request.form['timings']
    address = request.form['address']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tourist_spot (name, description, location, image, timings, address) VALUES (%s, %s, %s, %s, %s, %s)", (name, description, location, image, timings, address))
    mysql.connection.commit()
    cur.close()
    return redirect('/admin')

#ADMIN PANEL ENDS



#RESTAURANT ADMIN PANEL

@app.route('/restaurantadmin')
def restaurants():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM restaurant")
    data = cur.fetchall()
    cur.close()
    return render_template('restaurantadmin.html', data=data)

@app.route('/update_restaurant', methods=['POST'])
def update_restaurant():
    cur = mysql.connection.cursor()
    cur.execute("UPDATE restaurant SET name=%s, location=%s, type=%s, image=%s WHERE id=%s", (request.form['name'], request.form['location'], request.form['type'], request.form['image'], request.form['id']))
    mysql.connection.commit()
    cur.close()
    return 'success'

@app.route('/delete_restaurant/<int:id>', methods=['POST'])
def delete_restaurant(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM restaurant WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return 'success'

@app.route('/add', methods=['POST'])
def add_restaurant():
    name = request.form['name']
    location = request.form['location']
    type = request.form['type']
    image = request.form['image']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO restaurant (name, location, type, image) VALUES (%s, %s, %s, %s)", (name, location, type, image))
    mysql.connection.commit()
    cur.close()
    return redirect('/restaurantadmin')

#RESTAURANT ADMIN PANEL ENDS


app.jinja_env.globals.update(generate_star_rating=generate_star_rating)

if __name__ == "__main__":
     app.run(debug=True ,port=8080,use_reloader=False)
