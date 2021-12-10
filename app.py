from flask import Flask, jsonify, request, make_response, redirect
import jwt
import datetime
from functools import wraps
from flask_swagger_ui import get_swaggerui_blueprint
import mysql.connector
import json

token_id = ''
app = Flask(__name__)

### end swagger specific ###
app.config['SECRET_KEY'] = 'weengineers'


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


@app.route('/house/<title>', methods=['GET'])
@app.route('/house/<title>/<bedroom>', methods=['GET'])
@app.route('/house/<title>/<bedroom>/<sleeps>', methods=['GET'])
@app.route('/house/<title>/<bedroom>/<sleeps>/<bathroom>', methods=['GET'])
@app.route('/house/<title>/<bedroom>/<sleeps>/<bathroom>/<price>', methods=['GET'])
@app.route('/house/<title>/<bedroom>/<sleeps>/<bathroom>/<price>/<location>', methods=['GET'])
def house(title='any', bedroom='0', sleeps='0', location='any'):

    condo = []

    db_connector = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ra3g_Df7wy",
        database="vrbo"
    )

    cursor = db_connector.cursor()

    query = ("SELECT * FROM Condo_House WHERE Location Like"+f"'%{location}%'")
    cursor.execute(query)

    results = cursor.fetchall()

    for x in results:
        data = {
            "Title": x[0],
            "Sleeps": x[1],
            "Bedrooms": x[2],
            "Bathrooms": x[3],
            "Price": x[7],
            "Picture": {
                "Picture_1": x[4][1:-1],
                "Picture_2": x[5][1:-1],
                "Picture_3": x[6][1:-1],
            },
            "Location": x[8],
        }
        condo.append(data)

    houseJson = json.dumps(condo, indent=4)
    print(houseJson)
    # print(title, bedroom, sleeps, location)
    return houseJson


# Protected Route and function
@app.route('/protected')
@token_required
def protected():
    # return jsonify({'message': 'Only available to people with valid tokens.'})
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
