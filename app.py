import os
import csv
import datetime
from flask_cors import CORS
from flask import Flask, request, jsonify, abort, send_file
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from flask_bcrypt import Bcrypt

# others
from auth.schema import validate_user
from models.models import *

HOST = '0.0.0.0'
PORT = 3502

# initialize flask application
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'pearl'  # os.environ.get('SECRET')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
cors = CORS(app)
jwt = JWTManager(app)
flask_bcrypt = Bcrypt(app)

# mysql
DB_UNAME = os.environ.get('DATABASE_USER')
DB_PASSWORD = os.environ.get('DATABASE_PASS')
DB_PORT = os.environ.get('DATABASE_PORT')
DB_HOST = os.environ.get('DATABASE_HOST')
DB_NAME = os.environ.get('DATABASE_NAME')

# local mysql
# DB_UNAME = 'root'
# DB_PASSWORD = 'root'
# DB_HOST = 'localhost'
# DB_PORT = '3306'
# DB_NAME = 'test'
# config
DB_DATA_NAME = 'rehab_data'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_UNAME + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + DB_PORT + '/' + DB_NAME
app.config[
    'SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_BINDS'] = {
    'db2': 'mysql+pymysql://' + DB_UNAME + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + DB_PORT + '/' + DB_NAME
}
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'harilab'
db.init_app(app)


# user authorization
@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'ok': False,
        'message': 'Missing Authorization Header'
    }), 401


@app.route('/login', methods=['POST'])
def auth_user():
    """ auth endpoint """
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        current_user = UserModel.find_user_by_email(data['email'])
        user = {}
        if not current_user:
            return jsonify({'ok': False, 'message': 'User {} doesn\'t exist'.format(data['email'])})

        if flask_bcrypt.check_password_hash(current_user.password, data['password']):
            access_token = create_access_token(identity=data)
            refresh_token = create_refresh_token(identity=data)
            user['email'] = data['email']
            user['token'] = access_token
            user['refresh'] = refresh_token
            return jsonify({'ok': True, 'data': user}), 200
        else:
            return jsonify({'ok': False, 'message': 'invalid username or password'}), 401
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@app.route('/register', methods=['POST'])
def register():
    """ register user endpoint """
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        email = data['email']
        checkEmail = UserModel.find_user_by_email(email)
        if "@pitt.edu" not in email:
            return jsonify({'ok': False, 'message': 'Wrong user email'}), 401
        elif checkEmail is not None:
            return jsonify({'ok': False, 'message': 'User already exists!'}), 402
        else:
            data['password'] = flask_bcrypt.generate_password_hash(
                data['password'].encode('utf8'))
            user = UserModel(data['email'], data['password'])
            user.save_to_db()
            return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'}), 400


@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    """ refresh token endpoint """
    current_user = get_jwt_identity()
    ret = {
        'token': create_access_token(identity=current_user)
    }
    return jsonify({'ok': True, 'data': ret}), 200


# endpoint to show all dataset
@app.route('/api/dataset/all', methods=['POST'])
@jwt_required
def get_all_tables():
    tables = TableModel.find_all_tables()
    data = []
    for t in tables:
        data.append(t.json())
    # print(data)
    return jsonify({'ok': True, 'data': data})


# visualization
@app.route("/api/vis/date_count_day", methods=["POST"])
@jwt_required
def get_date_count_day():
    rows = DateCount.find_all_values()
    data = []
    for t in rows:
        data.append(t.json())
    return jsonify({'ok': True, 'data': data})


@app.route("/api/vis/date_count_month", methods=["POST"])
@jwt_required
def get_date_count_month():
    rows = DateCountByMonth.find_all_values()
    data = []
    for t in rows:
        data.append(t.json())
    return jsonify({'ok': True, 'data': data})


@app.route("/api/vis/date_count_year", methods=["POST"])
@jwt_required
def get_date_count_year():
    rows = DateCountByYear.find_all_values()
    data = []
    for t in rows:
        data.append(t.json())
    return jsonify({'ok': True, 'data': data})


@app.route("/api/vis/proc_cate", methods=["POST"])
@jwt_required
def get_proc_cate():
    rows = ProcedureCategory.find_all_values()
    data = []
    for t in rows:
        data.append(t.json())
    return jsonify({'ok': True, 'data': data})


@app.route("/api/vis/proc_subcate", methods=["POST"])
@jwt_required
def get_proc_subcate():
    rows = ProcedureSubCategory.find_all_values()
    data = []
    for t in rows:
        data.append(t.json())
    return jsonify({'ok': True, 'data': data})


@app.route("/api/download/<file_name>", methods=["GET"])
@jwt_required
def download_file(file_name):
    sql = """select * from rehab_data.""" + file_name
    results = db.engine.execute(sql)
    header = results.keys()
    data = results.fetchall()
    outfile = "./datasets/" + file_name + ".csv"
    with open(outfile, "w", newline="") as datacsv:
        csvwriter = csv.writer(datacsv)
        csvwriter.writerow(header)
        for row in data:
            csvwriter.writerow([getattr(row, c) for c in header])
    print("file ready")
    return send_file(outfile, as_attachment=True, attachment_filename=file_name + ".csv")


if __name__ == '__main__':
    from database import db

    db.init_app(app)


    @app.before_first_request
    def create_tables():
        db.create_all()


    app.run(host=HOST,
            debug=True,
            port=PORT)
