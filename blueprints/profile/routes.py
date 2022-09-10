from flask import Blueprint, render_template, request
from sql_provider import SQLProvider
from database import work_with_db
from blueprints.authorization.access import login_required
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Ansergart629009',
    'db': 'rk6_vasilyan'
}
profile_app = Blueprint('profile', __name__, template_folder='templates')
provider = SQLProvider('blueprints/profile/sql/')

@profile_app.route('/')
@login_required
def index():
    return render_template('profile-index.html')

@profile_app.route('/prov1', methods = ['GET', 'POST'])
@login_required
def get_sql1():
    if request.method == 'GET':
        return render_template('prov1.html')
    else:
        month = request.form.get('month', None)
        year = request.form.get('year', None)
        if month is not None and year is not None:
            sql = provider.get('task1.sql', month=month, year=year)
            result = work_with_db(db_config, sql)
            if not result:
                return render_template('not_found.html')
            return render_template('output.html', str=result, heads=['Название фильма', 'Количество сеансов', 'Количество проданных билетов'])

@profile_app.route('/prov2', methods = ['GET', 'POST'])
@login_required
def get_sql2():
    if request.method == 'GET':
        return render_template('prov2.html')
    else:
        month = request.form.get('month', None)
        year = request.form.get('year', None)
        if month is not None and year is not None:
            sql = provider.get('task2.sql', month=month, year=year)
            result = work_with_db(db_config, sql)
            if not result:
                return render_template('not_found.html')
            return render_template('output.html', str=result, heads=['Название фильма', 'Дата сеанса', 'Выручка'])