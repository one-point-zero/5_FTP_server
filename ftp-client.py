import socket

# Функция для запуска клиента
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создаем сокет
    client_socket.connect(('127.0.0.1', 9090))  # Подключаемся к серверу

    print("Connected to the server.")
    print("Available commands:")
    print("  list                     - List files and folders")
    print("  create_folder <name>     - Create a folder")
    print("  delete_folder <name>     - Delete a folder")
    print("  create_file <name>       - Create a file")
    print("  delete_file <name>       - Delete a file")
    print("  rename <old> <new>       - Rename file or folder")
    print("  write_file <name> <text> - Write content to a file")
    print("  read_file <name>         - Read content of a file")
    print("  exit                     - Exit the client")

    try:
        while True:
            # Ввод команды от пользователя
            command = input("Enter command: ")
            if command.lower() == "exit":  # Завершаем работу клиента
                break

            client_socket.send(command.encode('utf-8'))  # Отправляем команду серверу
            response = client_socket.recv(1024).decode('utf-8')  # Получаем ответ
            print(response)  # Выводим ответ
    finally:
        client_socket.close()  # Закрываем соединение

if __name__ == "__main__":
    start_client()