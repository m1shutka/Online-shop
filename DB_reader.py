import sqlite3

class DbReader():
    def __init__(self):
        self.__db = sqlite3.connect('shop.db', check_same_thread=False)



    #Методы для товаров
    def get_all_items(self):
        """Получение списка всех товаров"""
        cursor = self.__db.cursor()
        return cursor.execute("SELECT * FROM items").fetchall()
    
    def add_item(self, name, price, photo):
        """Добавление новго товара"""
        cursor = self.__db.cursor()
        cursor.execute("INSERT INTO items (item_id, name, price, image) VALUES (?, ?, ?, ?)", (self.rand_item_id(), name, price, photo))
        self.__db.commit()

    def rand_item_id(self):
        """Генерирование случайного id товара"""
        last_id = self.get_last_item_id()
        new_id = last_id[:3]+str(int(last_id[2:])+1)
        while len(new_id) < 9:
            new_id = new_id[:3]+ '0' + new_id[3:]
        return new_id

    def get_last_item_id(self):
        """Получение последнего зарегестрированного id"""
        cursor = self.__db.cursor()
        users = cursor.execute("SELECT * FROM items").fetchall()
        return users[len(users)-1][0]

    def get_item_photo(self, item_id):
        """Получение фото товара"""
        cursor = self.__db.cursor()
        image = cursor.execute("SELECT image FROM items WHERE item_id=?", (item_id,)).fetchone()[0]
        return image

    def get_item_name(self, item_id):
        """Получение названия товара"""
        cursor = self.__db.cursor()
        name = cursor.execute("SELECT name FROM items WHERE item_id=?", (item_id,)).fetchone()[0]
        return name

    def get_item_price(self, item_id):
        """Получение цены товара"""
        cursor = self.__db.cursor()
        price = cursor.execute("SELECT price FROM items WHERE item_id=?", (item_id,)).fetchone()[0]
        print(price)
        return price



    #Методы для заказов
    def get_all_oredrs(self):
        """Получение списка всех заказов"""
        cursor = self.__db.cursor()
        return cursor.execute("SELECT * FROM orders").fetchall()[::-1]



    #Методы для корзины
    def add_item_in_cart(self, user_id, item_id):
        """Добавление товара в корзину"""
        cursor = self.__db.cursor()
        items = cursor.execute("SELECT items FROM cart where user_id=?", (user_id,)).fetchone()
        if items != None:
            new_items = items[0] + ' ' + item_id
            cursor.execute("UPDATE cart SET items=? WHERE user_id = ?", (new_items, user_id))
        else:
            new_items = item_id
            cursor.execute("INSERT INTO cart (user_id, items) VALUES (?, ?)", (user_id, new_items))
        self.__db.commit()

    def get_user_cart(self, user_id):
        """Получение корзины пользователя"""
        cursor = self.__db.cursor()
        items = cursor.execute("SELECT items FROM cart where user_id=?", (user_id,)).fetchone()
        if items != None:
            return items[0].split()
        else:
            return []

    def erase_item_from_cart(self, user_id, item_id):
        """Удаление товара из корзины"""
        cursor = self.__db.cursor()
        items = cursor.execute("SELECT items FROM cart where user_id=?", (user_id,)).fetchone()
        if items != None:
            new_items = items[0].split()
            new_items.remove(item_id)
            cursor.execute("UPDATE cart SET items=? WHERE user_id = ?", (new_items, user_id))
        self.__db.commit()

    def is_item_in_cart(self, user_id, item_id):
        """Проверка на наличие товара в корзине"""
        cursor = self.__db.cursor()
        items = cursor.execute("SELECT items FROM cart where user_id=?", (user_id,)).fetchone()
        if items != None:
            itmes_lst = items[0].split()
            if item_id in itmes_lst:
                return True
            else:
                return False
        else:
            return False
            


    #Методы дляь пользователей
    def get_last_id(self):
        """Получение последнего зарегестрированного id"""
        cursor = self.__db.cursor()
        users = cursor.execute("SELECT * FROM users").fetchall()
        return users[len(users)-1][0]
    
    def get_user_quantity(self):
        """Получение количества пользователей"""
        cursor = self.__db.cursor()
        return len(cursor.execute("SELECT * FROM users").fetchall())

    def get_user_name(self, id):
        """Получение имени пользователя по id"""
        cursor = self.__db.cursor()
        return cursor.execute("SELECT name FROM users WHERE user_id=?", (id,)).fetchone()[0]

    def get_user_phone(self, id):
        """Получение имени пользователя по id"""
        cursor = self.__db.cursor()
        return cursor.execute("SELECT phone_number FROM users WHERE user_id=?", (id,)).fetchone()[0]

    def is_admin(self, id):
        """Проверка на права"""
        cursor = self.__db.cursor()
        if cursor.execute("SELECT admin FROM users WHERE user_id=?", (id,)).fetchone()[0] == 1:
            return True
        else:
            return False

    def rand_user_id(self):
        """Генерирование случайного id пользователя"""
        last_id = self.get_last_id()
        new_id = last_id[:3]+str(int(last_id[2:])+1)
        while len(new_id) < 9:
            new_id = new_id[:3]+ '0' + new_id[3:]
        return new_id

    def add_user(self, name, phone, login, password):
        """Добавление нового пользователя"""
        cursor = self.__db.cursor()
        cursor.execute("INSERT INTO users (user_id, name, phone_number, admin, login, password) VALUES (?, ?, ?, ?, ?, ?)", (self.rand_user_id(), name, phone, 0, login, password))
        self.__db.commit()

    def password_check(self, login, password):
        """Проверка пароля и возвращение id"""
        cursor = self.__db.cursor()
        if cursor.execute("SELECT password FROM users WHERE login=?", (login,)).fetchone()[0] == password:
            return cursor.execute("SELECT user_id FROM users WHERE login=?", (login,)).fetchone()[0]
        else:
            return None

    def is_registered(self, login):
        """Проверка на регистрацию"""
        cursor = self.__db.cursor()
        if cursor.execute("SELECT password FROM users WHERE login=?", (login,)).fetchone() != None:
            return True
        else: 
            return False

if __name__ == '__main__':
    reader = DbReader()
    print(reader.is_registered('admin@am.com'))