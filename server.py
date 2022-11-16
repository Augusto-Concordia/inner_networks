import socket
from typing import List

# connection settings
HOST = "127.0.0.1"
PORT = 9999

# entries for the database
entries: List[tuple[str, str, str, str]] = []

# starts the server process


def init():
    # reads the database file
    dbt = open("db.txt", "r")

    for line in dbt:
        name, age, address, phone = line.split("|")

        # formats the fields
        name = name.strip()
        age = age.strip()
        address = address.strip()
        phone = phone.strip()

        if name == '':
            continue

        entries.append((name, age, address, phone))

    # creates a connection to the first client that connects
    c_conn, c_address = create_connection()

    while True:
        data = c_conn.recv(1024)

        # if no data is coming, try the connection to see if it's alive
        if not data:
            c_conn, c_address = try_connection(c_conn, c_address)
            continue

        print("From connection: " + data.decode())

        result = process_data(data.decode())

        c_conn.send(result.encode())


# finds a customer with the specified name
def find_customer(name: str) -> tuple[str, str, str, str]:
    return next((e for e in entries if e[0] == name), None)


# determines if a customer exist with the specified name
def customer_exists(name: str) -> bool:
    return find_customer(name)


# gets the customer's name from a customer (used for sorting)
def get_customer_name(customer: tuple[str, str, str, str]) -> str:
    return customer[0]


# creates the add_customer response
def add_customer(raw_customer: str) -> str:
    name, age, address, phone = raw_customer.split(',')

    if customer_exists(name):
        return 'None'

    entries.append((name, age, address, phone))

    return 'Success'


# creates the delete_customer response
def delete_customer(name: str) -> str:
    customer_to_delete = find_customer(name)

    if not customer_to_delete:
        return 'None'

    entries.remove(customer_to_delete)

    return 'Success'


# creates the update_customer response
def update_customer(choice: str, raw_update: str) -> str:
    name, field_to_update = raw_update.split(',')

    customer_to_update = find_customer(name)

    if not customer_to_update:
        return 'None'

    if choice == '4':
        updated_customer = (
            customer_to_update[0], field_to_update, customer_to_update[2], customer_to_update[3])
    elif choice == '5':
        updated_customer = (
            customer_to_update[0], customer_to_update[1], field_to_update, customer_to_update[3])
    elif choice == "6":
        updated_customer = (
            customer_to_update[0], customer_to_update[1], customer_to_update[2], field_to_update)
    else:
        return 'None'

    entries.remove(customer_to_update)
    entries.append(updated_customer)

    return 'Success'


# creates the print_report response
def print_report() -> str:
    if len(entries) == 0:
        return 'Empty'

    report = ''

    entries.sort(key=get_customer_name)

    for e in entries:
        report += f'{e[0]}|{e[1]}|{e[2]}|{e[3]}\n'

    return report


# processes the client's request
def process_data(data: str) -> str:
    choice, param = data.split('|')

    if choice == '1':
        customer = find_customer(param)

        if not customer:
            return 'None'

        str_tuple = ''

        for d in customer[:-1]:
            str_tuple += d + '|'

        str_tuple += customer[-1]

        return str_tuple
    if choice == '2':
        return add_customer(param)
    if choice == '3':
        return delete_customer(param)
    if choice == '4' or choice == '5' or choice == '6':
        return update_customer(choice, param)
    if choice == '7':
        return print_report()


# creates connection and waits for the first client to connect
def create_connection():
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_socket.bind((HOST, PORT))
    s_socket.listen(1)

    conn, address = s_socket.accept()
    print(f"Connection on {address}")

    s_socket.close()

    return conn, address


# tries the connection to check connection validity
def try_connection(connection, address):
    try:
        connection.send(".")
    except:
        print(f"Disconnection from {address}")

        connection.close()

        return create_connection()


if __name__ == "__main__":
    init()
