from flask import Flask, jsonify, request, make_response,redirect
import jwt
import datetime
from functools import wraps
from flask_swagger_ui import get_swaggerui_blueprint
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
    return redirect("http://127.0.0.1:5000/login",code=302)


# Unprotected Route and function
# @app.route('/unprotected')
# def unprotected():
#     return jsonify({'message': 'Anyone can view this.'})


# @app.route('/unprotected/<token>/<id>', methods=['GET'])
# def unprotected(id):
#     print(id)
#     return jsonify(id)


# Protected Route and function
@app.route('/protected')
@token_required
def protected():
    #return jsonify({'message': 'Only available to people with valid tokens.'})
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
    return redirect("http://127.0.0.1:5000/swagger",code=302)


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
