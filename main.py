import configparser

import psycopg2

# DB_USER
db_users = configparser.ConfigParser()
db_users.read("db_user.ini")
sql_user = db_users['db_admin']
sql_login = sql_user['user']
sql_pass = sql_user['pass']


class Client:
    def __init__(self, name=None, surname=None, mail=None):
        self.name = name
        self.surname = surname
        self.mail = mail
        self.phones = []
        self.client_id = None


# Функция, создающая структуру БД (таблицы)
def create_databases():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            client_id SERIAL PRIMARY KEY,
            name VARCHAR(40) NOT NULL,
            surname VARCHAR(50) NOT NULL,
            mail VARCHAR(80) NOT NULL
            );
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            phone VARCHAR(12),
            client_id INTEGER NOT NULL REFERENCES clients(client_id) ON DELETE CASCADE
            );
        """)
    conn.commit()


def fetch(data):
    if type(data) is tuple:
        if len(data) == 5:
            print(f"Client_id: {data[0]}, Имя: {data[1]}, Фамилия: {data[2]}, Почта: {data[3]}, Телефон: {data[4]}")
        elif len(data) == 4:
            print(f"Client_id: {data[0]}, Имя: {data[1]}, Фамилия: {data[2]}, Почта: {data[3]}")
        elif len(data) == 3:
            print(f"phone_id: {data[0]}, Телефон: {data[1]} Client_id: {data[2]}")
        elif len(data) == 2:
            print(f"Телефон: {data[0]} Client_id: {data[1]}")
    elif type(data) is list:
        for i in data:
            print(f"Client_id: {i[0]}, Имя: {i[1]}, Фамилия: {i[2]}, Почта: {i[3]}, Телефон: {i[4]}")
    return


def get_client_id(name, surname, mail):
    cur.execute("""
        SELECT client_id FROM clients
        WHERE name=%s AND surname=%s AND mail=%s;
        """, (name, surname, mail))
    return cur.fetchone()[0]


def get_phone_id(phone):
    cur.execute("""
        SELECT id FROM phones
        WHERE phone=%s;
        """, (phone,))
    return cur.fetchone()[0]


# Функция, позволяющая добавить нового клиента
def add_client():
    person = Client(name=input('Введите имя клиента: '),
                    surname=input('Введите фамилию клиента: '),
                    mail=input('Введите почту клиента: '))
    cur.execute("""
        INSERT INTO clients(name, surname, mail) VALUES(%s, %s, %s);
        """, (person.name, person.surname, person.mail))
    conn.commit()
    phones = input('Введите телефоны через пробел (опционально): ').split()
    while len(phones) > 0:
        for p in range(len(phones)):
            cur.execute("""
                        INSERT INTO phones(phone, client_id) VALUES(%s, %s);
                        """, (phones[p], int(get_client_id(person.name, person.surname, person.mail))))
        phones.clear()
    conn.commit()
    cur.execute("""
        SELECT client_id, name, surname, mail FROM clients
        WHERE name=%s AND surname=%s AND mail=%s;
        """, (person.name, person.surname, person.mail))
    print('Клиент добавлен.')
    return fetch(cur.fetchone())


# Функция, позволяющая добавить телефон для существующего клиента
def add_phone():
    phone = input('Введите номер телефона: ')
    while phone.isdigit() is not True:
        print('Номер содержит буквы')
        phone = input('Введите номер телефона: ')
    client_id = int(input('Введите клиентский id: '))
    cur.execute("""
                INSERT INTO phones(phone, client_id) VALUES(%s, %s);
                """, (phone, client_id))
    conn.commit()
    cur.execute("""
                SELECT phone, client_id FROM phones
                WHERE phone=%s;
                """, (phone, ))
    print('Телефон добавлен.')
    return fetch(cur.fetchone())


# Функция, позволяющая изменить данные о клиенте
def change_client():
    print("Укажите кол-во данных которые необходимо заменить, на основании client_id. Кол-во параметров от 1 до 3")
    f = int(input('Введите значение: '))
    cl_id = int(input('Укажите client_id: '))
    if f == 1:
        pos = input('Укажите столбец который необходимо изменить: name, surname, mail: ')
        value = input('Укажите новое значение: ')
        cur.execute(f"""
        UPDATE clients SET {pos}='{value}' WHERE client_id={cl_id};
        """)
    if f == 2:
        pos1 = input('Укажите столбец который необходимо изменить: name, surname, mail: ')
        while pos1 not in ['name', 'surname', 'mail']:
            pos1 = input('Укажите столбец который необходимо изменить: name, surname, mail: ')
        value1 = input('Укажите новое значение: ')
        pos2 = input('Укажите столбец который необходимо изменить: name, surname, mail: ')
        while pos2 not in ['name', 'surname', 'mail']:
            pos2 = input('Укажите столбец который необходимо изменить: name, surname, mail: ')
        value2 = input('Укажите новое значение: ')
        cur.execute(f"""
        UPDATE clients SET {pos1}='{value1}', {pos2}='{value2}' WHERE client_id={cl_id};
        """)
    if f == 3:
        pos1 = input('Укажите столбец который необходимо изменить: name, surname, mail: ')
        while pos1 not in ['name', 'surname', 'mail']:
            pos1 = input('Укажите столбец который необходимо изменить: name, surname, mail: ')
        value1 = input('Укажите новое значение: ')
        pos2 = input('Укажите столбец который необходимо изменить: name, surname, mail: ')
        while pos2 not in ['name', 'surname', 'mail']:
            pos2 = input('Укажите столбец который необходимо изменить: name, surname, mail: ')
        value2 = input('Укажите новое значение: ')
        pos3 = input('Укажите столбец который необходимо изменить: name, surname, mail: ')
        while pos3 not in ['name', 'surname', 'mail']:
            pos3 = input('Укажите столбец который необходимо изменить: name, surname, mail: ')
        value3 = input('Укажите новое значение: ')
        cur.execute(f"""
        UPDATE clients SET {pos1}='{value1}', {pos2}='{value2}', {pos3}='{value3}' WHERE client_id={cl_id};
        """)
    cur.execute(f"""
    SELECT client_id, name, surname, mail from clients
    WHERE client_id={cl_id};
    """)
    print('Данные изменены')
    return fetch(cur.fetchone())


# Функция, позволяющая удалить телефон для существующего клиента
def del_phone():
    phone = input('Введите номер телефона: ')
    cur.execute("""
    SELECT c.client_id, name, surname, mail, p.phone as client_phone FROM clients c
    LEFT JOIN phones p ON p.client_id = c.client_id
    WHERE phone=%s; 
    """, (phone,))
    print('DELETING')
    fetch(cur.fetchone())
    cur.execute("""
            DELETE FROM phones WHERE phone=%s;
            """, (phone,))
    conn.commit()
    return print('Phone deleted')


# Функция, позволяющая удалить существующего клиента
def del_client():
    client_id = int(input('Введите client_id: '))
    cur.execute("""
    SELECT c.client_id, name, surname, mail, p.phone as client_phone FROM clients c
    LEFT JOIN phones p ON p.client_id = c.client_id
    WHERE c.client_id=%s; 
    """, (client_id,))
    print('DELETING')
    fetch(cur.fetchall())
    cur.execute("""
            DELETE FROM clients WHERE client_id=%s;
            """, (client_id,))
    conn.commit()
    return print('Client deleted')


# Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
def find_client():
    print("Укажите кол-во параметров по которым осуществляется поиск. Кол-во параметров от 1 до 3")
    f = int(input('Введите значение: '))
    if f == 1:
        pos = input('Укажите столбец который необходимо изменить: name, surname, mail, phone: ')
        while pos not in ['name', 'surname', 'mail', 'phone']:
            pos = input('Укажите столбец который необходимо изменить: name, surname, mail, phone: ')
        value = input('Укажите значение для поиска: ')
        cur.execute(f"""
        SELECT c.client_id, name, surname, mail, p.phone as client_phone FROM clients c
        LEFT JOIN phones p ON p.client_id = c.client_id
        WHERE {pos}='{value}'; 
        """)
    if f == 2:
        pos1 = input('Укажите столбец который необходимо изменить: name, surname, mail, phone: ')
        while pos1 not in ['name', 'surname', 'mail', 'phone']:
            pos1 = input('Укажите столбец который необходимо изменить: name, surname, mail, phone: ')
        value1 = input('Укажите значение для поиска: ')
        pos2 = input('Укажите столбец который необходимо изменить: name, surname, mail, phone: ')
        while pos2 not in ['name', 'surname', 'mail', 'phone']:
            pos2 = input('Укажите столбец который необходимо изменить: name, surname, mail, phone: ')
        value2 = input('Укажите значение для поиска: ')
        cur.execute(f"""
        SELECT c.client_id, name, surname, mail, p.phone as client_phone FROM clients c
        LEFT JOIN phones p ON p.client_id = c.client_id
        WHERE {pos1}='{value1}' AND {pos2}='{value2}'; 
        """)
    if f == 3:
        pos1 = input('Укажите столбец который необходимо изменить: name, surname, mail, phone: ')
        while pos1 not in ['name', 'surname', 'mail', 'phone']:
            pos1 = input('Укажите столбец который необходимо изменить: name, surname, mail, phone: ')
        value1 = input('Укажите значение для поиска: ')
        pos2 = input('Укажите столбец который необходимо изменить: name, surname, mail, phone: ')
        while pos2 not in ['name', 'surname', 'mail', 'phone']:
            pos2 = input('Укажите столбец который необходимо изменить: name, surname, mail, phone: ')
        value2 = input('Укажите значение для поиска: ')
        pos3 = input('Укажите столбец который необходимо изменить: name, surname, mail, phone')
        while pos3 not in ['name', 'surname', 'mail', 'phone']:
            pos3 = input('Укажите столбец который необходимо изменить: name, surname, mail, phone: ')
        value3 = input('Укажите значение для поиска: ')
        cur.execute(f"""
        SELECT c.client_id, name, surname, mail, p.phone as client_phone FROM clients c
        LEFT JOIN phones p ON p.client_id = c.client_id
        WHERE {pos1}='{value1}' AND {pos2}='{value2}' AND {pos3}='{value3}'; 
        """)

    return fetch(cur.fetchall())


# Вызов функций
def functions(func):
    if func == 'create_databases':
        create_databases()
    if func == 'add_client':
        add_client()
    if func == 'add_phone':
        add_phone()
    if func == 'change_client':
        change_client()
    if func == 'del_phone':
        del_phone()
    if func == 'del_client':
        del_client()
    if func == 'find_client':
        find_client()
    if func == 'exit':
        return exit()


if __name__ == "__main__":
    while True:
        with psycopg2.connect(database="hw5_phonebook", user=sql_login, password=sql_pass) as conn:
            with conn.cursor() as cur:
                print("""
                Доступные функции:
                    create_databases - Функция, создающая структуру БД (таблицы)
                    add_client - Функция, позволяющая добавить нового клиента
                    add_phone - Функция, позволяющая добавить телефон для существующего клиента
                    change_client - Функция, позволяющая изменить данные о клиенте
                    del_phone - Функция, позволяющая удалить телефон для существующего клиента
                    del_client - Функция, позволяющая удалить существующего клиента
                    find_client - Функция, позволяющая найти клиента по его данным(имени, фамилии, email-у или телефону)
                    exit - выход
                    """)
                functions(input('Введите действие: '))
        conn.close()
