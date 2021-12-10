from flask import Flask, jsonify, request, make_response, redirect
import jwt
import datetime
from functools import wraps
from flask_swagger_ui import get_swaggerui_blueprint
import mysql.connector
import json
import operator

token_id = ''
app = Flask(__name__)

app.config['SECRET_KEY'] = 'weengineers'
#### Swagger path initialized ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "shaibal657"
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


### end swagger specific ###

# Token Decorator


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is missing'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated


@app.route('/')
def index():
    return redirect("http://127.0.0.1:5000/login", code=302)


# Unprotected Route and function
@app.route('/unprotected')
def unprotected():
    return jsonify({'message': 'Anyone can view this.'})


@app.route('/house', methods=['GET'])
def house():
    title = request.args.get('title')
    bedroom = request.args.get('bedroom')
    sleeps = request.args.get('sleeps')
    bathroom = request.args.get('bathroom')
    price = request.args.get('price')
    location = request.args.get('location')

    condo = []

    db_connector = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ra3g_Df7wy",
        database="vrbo"
    )
    check = False
    query = "SELECT * FROM Condo_House WHERE"
    cursor = db_connector.cursor()
    if title != None:
        if check == False:
            query += " Name LIKE" + f"'%{title}%'"
            check = True
        else:
            query += " AND Name LIKE" + f"'%{title}%'"

    if bedroom != None:
        if check == False:
            query += " Bedroom >=" + f"'{bedroom} Bedrooms'"
            check = True
        else:
            query += " AND Bedroom >=" + f"'{bedroom} Bedrooms'"

    if bathroom != None:
        if check == False:
            query += " Bathroom >=" + f"'{bathroom} Bathrooms'"
            check = True
        else:
            query += " AND Bathroom >=" + f"'{bathroom} Bathrooms'"

    if sleeps != None:
        if check == False:
            query += " Sleeps >=" + f"'Sleeps {sleeps}'"
            check = True
        else:
            query += " AND Sleeps >=" + f"'Sleeps {sleeps}'"

    if price != None:
        if check == False:
            query += " Price >=" + f"'${price}'"
            check = True
        else:
            query += " AND Price >=" + f"'${price}'"

    if location != None:
        if check == False:
            query += " Location LIKE" + f"'%{location}%'"
        else:
            query += " AND Location LIKE" + f"'%{location}%'"
    print(query)
    cursor.execute(query)
    results = cursor.fetchall()
    for result in results:
        data = {
            "Title": result[0],
            "Sleeps": result[1],
            "Bedrooms": result[2],
            "Bathrooms": result[3],
            "Price": result[7],
            "Image": {
                "Image_url_1": result[4][1:-1],
                "Image_url_2": result[5][1:-1],
                "Image_url_3": result[6][1:-1],
            },
            "Location": result[8],
        }
        condo.append(data)
    condo.sort(key=operator.itemgetter('Bedrooms'))
    houseJson = json.dumps(condo, indent=4)
    print(condo)
    print(houseJson)
    print(query)
    return houseJson


# Protected Route and function
@app.route('/protected')
@token_required
def protected():
    # return jsonify({'message': 'Only available to people with valid tokens.'})

    return redirect("http://127.0.0.1:5000/swagger", code=302)


# Login Route and function
@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'smartboy':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=50)},
                           app.config['SECRET_KEY'])
        token_id = token
        return jsonify({'token': token})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm:"Login Required"'})


if __name__ == "__main__":
    app.run()
