import os
from flask import Blueprint, render_template, request, session, redirect
from sql_provider import SQLProvider
from database import work_with_db, make_update
from blueprints.basket.utils import add_to_basket, clear_basket
from blueprints.authorization.access import login_required

basket_app = Blueprint('basket', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Ansergart629009',
    'db': 'rk6_vasilyan'
}

@basket_app.route('/', methods=['GET', 'POST'])
@login_required
def movies():
    if request.method == 'GET':
        sql = provider.get('movie_selection.sql')
        movies = work_with_db(db_config, sql)
        return render_template('movie_selection.html', movies=movies)
    else:
        session['m_id'] = request.form.get('m_id', '')
        return redirect('/basket/movie_session')

@basket_app.route('/movie_session', methods=['GET', 'POST'])
def sessions():
    if request.method == 'GET':
        sql = provider.get('session_selection.sql', m_id=session.get('m_id', ''))
        sessions = work_with_db(db_config, sql)
        return render_template('session_selection.html', sessions=sessions)
    else:
        session['chosen_session_number'] = request.form.get('chosen_session_number', '')
        session['selected'] = []
        return redirect('/basket/basket_page')

@basket_app.route('/basket_page', methods=['GET', 'POST'])
def list_orders_handler():
    if request.method == 'GET':
        current_basket = session.get('basket', [])
        sql = provider.get('order_list.sql', m_id=session.get('m_id', ''), session_number=session.get('chosen_session_number', ''))
        items = work_with_db(db_config, sql)
        return render_template('basket_order_list.html', items=items, basket=current_basket)
    else:
        selected = session.get('selected', '')
        ticket_id = request.form['ticket_id']
        for i in selected:
            if i == ticket_id:
                return redirect('/basket/basket_page')
        sql = provider.get('order_item.sql', ticket_id=ticket_id)
        items = work_with_db(db_config, sql)
        if not items:
            return 'Item not found'
        add_to_basket(items)
        selected.append(ticket_id)
        session['selected'] = selected
        return redirect('/basket/basket_page')

@basket_app.route('/clear')
def clear_basket_handler():
    clear_basket()
    session['selected'] = []
    return redirect('/basket/basket_page')

@basket_app.route('/buy')
def basket_buy():
    total_cost = 0
    num_of_tickets = 0
    items = session.get('basket', [])
    if items:
        for item in items:
            sql = provider.get('insert_item.sql', revenue=item['avarage_ticket_price'], session_number=item['session_number_t'], title=item['title'], ticket_id=item['ticket_id'])
            make_update(db_config, sql)
            total_cost += item['avarage_ticket_price']
            num_of_tickets += 1
        sql_c = provider.get('new_cheque.sql', num_of_tickets=num_of_tickets, total_cost=total_cost, m_id=item['m_id'], session_number=item['session_number_t'], title=item['title'], ticket_id=item['ticket_id'])
        make_update(db_config, sql_c)
        clear_basket()
        session['selected'] = []
        message = 'Ваша покупка подтверждена!'
    else:
        message = 'Корзина пуста. Нажмите на "добавить" у одного из сеансов.'
    return render_template('purchase_confirmed.html', message=message)
