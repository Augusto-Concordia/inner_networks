import socket

# connection settings
HOST = '127.0.0.1'
PORT = 9999

# starts the client process


def init():
    # connects to the server
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_socket.connect((HOST, PORT))

    while True:
        choice_display()
        choice = input(' ')

        # exits the client
        if choice == '8':
            print('See you later... Alligator.')
            break

        success = process_choice(choice, c_socket)

        # if the form entry was a success, send it to the server;
        # otherwise, wait for more input
        if success:
            result = c_socket.recv(1024)

            process_result(choice, result.decode())
        else:
            print("\nInvalid operation: Please try again.", end="\n\n")

        input('Press ENTER to continue...')

    c_socket.close()


# displays the main choices menu
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


# processes the server's find_customer response
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


# processes the server's add_customer response
def process_add_customer(raw_result: str):
    if raw_result == 'None':
        print('Customer already exists.')
    else:
        print('Successfully added customer.')


# processes the server's delete_customer response
def process_delete_customer(raw_result: str):
    if raw_result == 'None':
        print('Customer does not exist.')
    else:
        print('Successfully deleted customer.')


# processes the server's update_customer response
def process_update_customer(raw_result: str):
    if raw_result == 'None':
        print('Customer does not exist.')
    else:
        print('Successfully updated customer.')


# processes the server's print_report response
def process_print_report(raw_result: str):
    print('Customer DB Report\n------------------\n' + raw_result)


# processes the server's response choice
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


# processes the user's find_customer response, returns true if the formed succeeded
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

        if name == '':
            return False

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

        if field_to_update == '':
            return False

        connection.send((choice + '|' + name + ',' + field_to_update).encode())

        return True
    if choice == '7':
        connection.send((choice + '|').encode())
        return True
    if True:
        return False


if __name__ == '__main__':
    init()
