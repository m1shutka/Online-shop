from flask import Flask, render_template, redirect, request
from DB_reader import DbReader

app = Flask(__name__)
reader = DbReader()
local_id = None
local_cart = []

def str_to_str(items):
    items = items.split()
    dict_items = {}
    result = ''
    for i in items:
        if i in dict_items.keys():
            dict_items[i] += 1
        else:
            dict_items[i] = 1

    for i in dict_items.keys():
        result += str(dict_items[i]) + 'x ' + i + ', '

    result = result[:len(result)-2]
    result += '.'
    return result

def str_to_dict(items):
    items = items.split()
    dict_items = {}
    for i in items:
        if i in dict_items.keys():
            dict_items[i] += 1
        else:
            dict_items[i] = 1
    return dict_items


@app.route('/add_item_in_cart/<id>', methods = ['POST', 'GET'])
def add_item_in_cart(id):
    if local_id == None:
        local_cart.append(id)
    else:
        reader.add_item_in_cart(local_id, id)
    return redirect('/')

@app.route('/erase_item_from_cart/<id>', methods = ['POST', 'GET'])
def erase_item_from_cart(id):
    if local_id == None:
        if id in local_cart:
            local_cart.remove(id)
    else:
        reader.erase_item_in_cart(local_id, id)
    return redirect('/')

@app.route('/')
def index():
    global local_id
    global local_cart
    items = reader.get_all_items()
    items_info = []
    if local_id != None:
        for i in items:
            item_info = []
            item_info.append(i)
            if reader.is_item_in_cart(local_id, i[0]):
                item_info.append(['В корзине', '/erase_item_from_cart/', 'btn btn-success'])
            else:
                item_info.append(['В корзину', '/add_item_in_cart/', 'btn btn-primary'])
            items_info.append(item_info)

        if reader.is_admin(local_id) == True:
            header_tegs = [['Главная', '#', "nav-link px-2 link-secondary"], ['Заказы', '/orders', 'nav-link px-2'], ['Добавление товара', '/create_new_item', 'nav-link px-2']]
            header_buttons = [[reader.get_user_name(local_id), '#', 'btn btn-primary'], ['Выйти', '/exit', "btn btn-outline-primary"]]
        else:
            header_tegs = [['Главная', '#', "nav-link px-2 link-secondary"], ['Корзина', '/cart', 'nav-link px-2']]
            header_buttons = [[reader.get_user_name(local_id), '#', 'btn btn-primary'], ['Выйти', '/exit', "btn btn-outline-primary"]]
    else:
        for i in items:
            item_info = []
            item_info.append(i)
            if i[0] in local_cart:
                 item_info.append(['В корзине', '/erase_item_from_cart/', 'btn btn-success'])
            else:
                item_info.append(['В корзину', '/add_item_in_cart/', 'btn btn-primary'])
            items_info.append(item_info)

        header_tegs = [['Главная', '#', 'nav-link px-2 link-secondary'], ['Корзина', '/cart', 'nav-link px-2']]
        header_buttons = [['Войти', '/sign_in', 'btn btn-outline-primary'], ['Зарегистрироваться', '/registration', "btn btn-primary"]]
    
    return render_template('index.html', items=items_info, header_tegs=header_tegs, header_buttons=header_buttons)


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    global local_id
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        if reader.is_registered(login):
            local_id = reader.password_check(login, password)
            if local_id != None:
                return redirect('/')
            else:
                return render_template('sign_in.html')
        else:
            return render_template('sign_in.html')
    else:
        return render_template('sign_in.html')

@app.route('/create_new_item', methods=['POST', 'GET'])
def create_new_item():
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_photo = request.form['item_photo']
        item_price = request.form['item_price']
        reader.add_item(item_name, item_price, item_photo)
        return redirect('/')
    else:
        return render_template('create_new_item.html')

@app.route('/registration', methods=['POST', 'GET'])
def registration():
    global local_id
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        login = request.form['login']
        password = request.form['password']
        if not reader.is_registered(login):
            reader.add_user(name, phone, login, password)
            local_id = reader.password_check(login, password)
            return redirect('/')
        else:
            return render_template('registration.html')
    else:
        return render_template('registration.html')

@app.route('/orders')
def orders():
    orders = reader.get_all_oredrs()[::-1]
    data = []
    for i in orders:
        order_info = []
        order_info.append(i[4])
        order_info.append(reader.get_user_name(i[0]))
        order_info.append(reader.get_user_phone(i[0]))
        items = str_to_str(i[1])
        order_info.append(items)
        order_info.append(i[3])
        if i[2] == 1:
            order_info.append(['Обработано', '#', "btn btn-success"])
        else:
            order_info.append(['Обработать', '/processin_order', "btn btn-warning"])
        data.append(order_info)
    return render_template('orders.html', data=data)

@app.route('/cart')
def cart():
    global local_id
    global local_cart
    new_items = {}
    items_info = []
    if local_id == None:
        items = local_cart
    else:
        items = reader.get_user_cart(local_id)
    for i in items:
        if i in new_items.keys():
            new_items[i] += 1
        else:
            new_items[i] = 1

    total_sum = 0
    for i in new_items.keys():
        items_info.append([i, new_items[i], reader.get_item_name(i), reader.get_item_photo(i), reader.get_item_price(i)])
        total_sum += reader.get_item_price(i)
    return render_template('cart.html', items=items_info, sum=total_sum)

@app.route('/exit')
def exit():
    global local_id
    global local_cart
    local_id = None
    local_cart.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
