from datetime import datetime
from configuration import app, db
from flask_bcrypt import Bcrypt
from flask import session, request, json, jsonify, redirect
from db import Driver, Klient, Driver_products,Klient_products
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
sec = URLSafeTimedSerializer('SECRETKEYITSISSECRETNAXUYILYA')
bcrypt = Bcrypt(app)


@app.before_first_request
def creat_all():
    db.create_all()

@app.route('/')
def first():
    return 'hello'

@app.route('/v1/regist', methods=["POST"])
def regist():
    request_data = request.get_json()
    name = request_data['name']
    email = request_data['email']
    pswd = request_data['password']
    flag = request_data['flag']
    hash_pswd = bcrypt.generate_password_hash(pswd).decode('utf-8')
    if flag == "1":
        if Driver.query.filter_by(email=email).first():
            return 'Email registred'
        else:
            account = Driver(sname=name, email=email, pswd=hash_pswd)
            db.session.add(account)
            db.session.commit()
            return 'succesuful registred'
    else:
        if Klient.query.filter_by(email=email).first():
            return 'Email registred'
        else:
            account = Klient( sname=name, email=email, pswd=hash_pswd)
            db.session.add(account)
            db.session.commit()
            return 'succesuful registred'


@app.route('/v1/login', methods=['POST'])
def login():
    request_data = request.get_json()
    email = request_data['email']
    pswd = request_data['password']
    flag = request_data['flag']
    if flag == '1':
        author_login = Driver.query.filter_by(email=email).first()
        print(author_login.pswd)
        print(bcrypt.check_password_hash(author_login.pswd, pswd))
        if author_login and bcrypt.check_password_hash(author_login.pswd, pswd):
            session['id'] = author_login.id
            return {
                'id': author_login.id,
                'type': 'Driver'
            }
        else:
            return 'Password or email is not correct'
    else:
        author_login = Klient.query.filter_by(email=email).first()
        if author_login and bcrypt.check_password_hash(author_login.pswd, pswd):
            session['id'] = author_login.id
            return {
                'id': author_login.id,
                'type': 'Klient'
            }
        else:
            return 'Password or email is not correct'

@app.route('/v1/logout')
def logout():
    session.clear()  # remove author from session
    return redirect('/')

def driver_product_serializer(Driver_products):
    return {
        'id': Driver_products.id,
        'img': Driver_products.img,
        'date': Driver_products.date,
        'obyom': Driver_products.obyom,
        'type_kuzov': Driver_products.type_kuzov,
        'lokatsiya_strana': Driver_products.lokatsiya_strana,
        'lokatsiy_gorod': Driver_products.lokatsiya_gorod,
        'phone': Driver_products.phone,
        'driverID': Driver_products.driverID
    }


def klient_product_serializer(Klient_products):
    return {
        'id': Klient_products.id,
        'title': Klient_products.title,
        'type_kuzov': Klient_products.type_kuzov,
        'start_strana': Klient_products.start_starana,
        'start_gorod': Klient_products.start_gorod,
        'finish_strana': Klient_products.finish_starana,
        'finish_gorod': Klient_products.finish_gorod,
        'obyom': Klient_products.obyom,
        'text': Klient_products.text,
        'phone': Klient_products.phone,
        'klientID': Klient_products.klientID
    }





def Driver_serializer(Driver):
    return {
        'id': Driver.id,
        'sname': Driver.sname,
        'email': Driver.email,
        'password': Driver.pswd,

    }





def Klient_serializer(Klient):
    return {
        'id': Klient.id,
        'sname': Klient.sname,
        'email': Klient.email,
        'password': Klient.pswd,
        'izbranniy_id': Klient.liked,
        'user_type': 'Klinet'
    }



@app.route('/v1/products', methods=['GET'])
def products():
    return jsonify([*map(klient_product_serializer, Klient_products.query.all())], [*map(driver_product_serializer, Driver_products.query.all())])


# @app.route('/filter_prudcts', methods=['GET','POST'])
# def filtr():
#     request_filtr = request.get_json()
#     mode = request_filtr['mode']
#     if mode == 'klient':
#         if  request_filtr['start_strana']!='Null':
#             if request_filtr['start_gorod']!='Null':
#                 if request_filtr['finish_strana']!='Null':
#                     if request_filtr['finish_gorod']!='Null':
#             Klient_products.query.filter_by(start_strana=request_filtr['start_strana']).all()




@app.route('/v1/add_product', methods=['POST'])
def add_product():
    request_data = request.get_json()
    flag = request_data['flag']
    id_sesiya = request_data['id']
    if flag == '1':
        if Driver.query.filter_by(id=id_sesiya).first():
            author_login = Driver.query.filter_by(id=id_sesiya).first()
            img = request_data['img']
            obyom = request_data['obyom']
            type_kuzov = request_data['type_kuzov']
            lokatsiya_strana = request_data['lokatsiya_strana']
            lokatsiya_gorod = request_data['lokatsiya_gorod']
            phone = request_data['phone']
            print(img, obyom, type_kuzov, lokatsiya_strana, lokatsiya_gorod, phone)

            product = Driver_products(img=img, obyom=obyom, type_kuzov=type_kuzov, lokatsiya_strana=lokatsiya_strana, lokatsiya_gorod=lokatsiya_gorod, phone=phone, driverID=request_data['id'])
            db.session.add(product)
            db.session.commit()
            print('dafasfasfas')
            return 'Succseful added'
        else:
            return "No such kind of Driver"


    else:
        if Klient.query.filter_by(id=id_sesiya).first():
            author_login = request_data['id']
            title = request_data['title']
            type_kuzov = request_data['type_kuzov']
            start_staran = request_data['start_strana']
            start_gorod = request_data['start_gorod']
            finish_strana = request_data['finish_strana']
            finish_gorod = request_data['finish_gorod']
            obyom = request_data['obyom']
            text = request_data['text']
            phone = request_data['phone']

            product = Klient_products(title=title, type_kuzov=type_kuzov, start_starana=start_staran, start_gorod=start_gorod, finish_starana=finish_strana, finish_gorod=finish_gorod, obyom=obyom, text=text,phone=phone,klientID=author_login)
            db.session.add(product)
            db.session.commit()
            return 'Succseful added'
        else:
            return 'No such kind of klient'


@app.route('/v1/profile', methods=['GET', 'POST'])
def profile():
    request_id = request.get_json()
    session_id = "1"
    type = 'Driver'
    if type == 'Driver':
        return jsonify(Driver_serializer(Driver.query.filter_by(id=session_id).first()))




if __name__=="__main__":
    app.run(debug=True)



