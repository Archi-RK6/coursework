from flask import Flask, render_template, session
from blueprints.profile.routes import profile_app
from blueprints.authorization.routes import auth_app
from blueprints.basket.routes import basket_app
from sql_provider import SQLProvider

app = Flask(__name__)
app.register_blueprint(profile_app, url_prefix='/profile')#1 - приложение, которое к этому app привязать, 2 - то, как его идентифицировать
app.register_blueprint(auth_app, url_prefix='/authorization')
app.register_blueprint(basket_app, url_prefix='/basket')
#все url, начинающиеся с profile, будут передаваться в routes - nfv ,eltn
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Ansergart629009',
    'db': 'rk6_vasilyan'
}

provider = SQLProvider('blueprints/profile/sql/')
app.config['SECRET_KEY'] = 'super secret key'

@app.route('/')
def index():
    return render_template('menu.html')

@app.route('/exit')
def exit_handler():
    session.clear()
    return render_template('exit.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)