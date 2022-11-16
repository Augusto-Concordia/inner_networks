import socket

HOST = '127.0.0.1'
PORT = 9999


def choice_display():
    print('''
Python DB Menu - Deluxe

    1. Find Customer
    2. Add Customer
    3. Delete customer
    4. Update customer age
    5. Update customer address
    6. Update customer phone
    7. Print report
    8. Exit
    
Select:''', end='')


def process_find_customer(raw_result: str):
    if raw_result == 'None':
        print('Not found.')
    else:
        name, age, address, phone = raw_result.split('|')

        print(f'''
Found Entry
-----------
Name: {name}
Age: {age}
Address: {address}
Phone #: {phone}
''')


def process_add_customer(raw_result: str):
    if raw_result == 'None':
        print('Customer already exists.')
    else:
        print('Successfully added customer.')


def process_delete_customer(raw_result: str):
    if raw_result == 'None':
        print('Customer does not exist.')
    else:
        print('Successfully deleted customer.')


def process_update_customer(raw_result: str):
    if raw_result == 'None':
        print('Customer does not exist.')
    else:
        print('Successfully updated customer.')


def process_print_report(raw_result: str):
    print('Customer DB Report\n------------------\n' + raw_result)


def process_result(choice: str, result: str):
    if choice == '1':
        process_find_customer(result)
    elif choice == '2':
        process_add_customer(result)
    elif choice == '3':
        process_delete_customer(result)
    elif choice == '4' or choice == '5' or choice == '6':
        process_update_customer(result)
    elif choice == '7':
        process_print_report(result)


def process_choice(choice: str, connection: socket.socket) -> bool:
    if choice == '1':
        name = input('Name? (case-sensitive) ')
        connection.send((choice + '|' + name).encode())
        return True
    if choice == '2':
        print('\nNew Customer')
        print('------------')

        name = input('Name? ')
        age = input('Age? ')
        address = input('Address? ')
        phone = input('Phone #? ')

        connection.send(
            (choice + '|' + f"{name},{age},{address},{phone}").encode())

        return True
    if choice == '3':
        name = input('Name to delete? (case-sensitive) ')
        connection.send((choice + '|' + name).encode())
        return True
    if choice == '4' or choice == '5' or choice == '6':
        print('\nUpdate Customer')
        print('------------')

        name = input('Name (case-sensitive)? ')

        field_to_update = ''

        if choice == '4':
            field_to_update = input('Age? ')
        elif choice == '5':
            field_to_update = input('Address? ')
        elif choice == '6':
            field_to_update = input('Phone #? ')
        else:
            return False

        connection.send((choice + '|' + name + ',' + field_to_update).encode())

        return True
    if choice == '7':
        connection.send((choice + '|').encode())
        return True
    if True:
        print("\nInvalid operation: Please try again.", end="\n\n")
        return False


def init():
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_socket.connect((HOST, PORT))

    while True:
        choice_display()
        choice = input(' ')

        if choice == '8':
            print('See you later... Alligator.')
            break

        success = process_choice(choice, c_socket)

        if success:
            result = c_socket.recv(1024)

            process_result(choice, result.decode())

        input('Press ENTER to continue...')

    c_socket.close()


if __name__ == '__main__':
    init()
