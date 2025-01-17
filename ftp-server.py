import os
import socket
import shutil

# Устанавливаем рабочую директорию для сервера
WORKING_DIR = "server_workspace"

# Если директория не существует, создаем ее
if not os.path.exists(WORKING_DIR):
    os.makedirs(WORKING_DIR)

# Функция для обработки запросов клиента
def handle_client_request(client_socket):
    try:
        while True:
            # Получаем запрос от клиента
            request = client_socket.recv(1024).decode('utf-8')
            if not request:  # Если запрос пустой, завершаем обработку
                break

            # Разделяем запрос на команды и параметры
            parts = request.split(' ')
            command = parts[0].lower()  # Основная команда
            response = ""  # Ответ сервера

            # Обработка команды "list" (список файлов и папок)
            if command == "list":
                response = "\n".join(os.listdir(WORKING_DIR))
            # Создание папки
            elif command == "create_folder":
                folder_name = parts[1]
                os.makedirs(os.path.join(WORKING_DIR, folder_name), exist_ok=True)
                response = f"Folder '{folder_name}' created."
            # Удаление папки
            elif command == "delete_folder":
                folder_name = parts[1]
                shutil.rmtree(os.path.join(WORKING_DIR, folder_name), ignore_errors=True)
                response = f"Folder '{folder_name}' deleted."
            # Создание файла
            elif command == "create_file":
                file_name = parts[1]
                open(os.path.join(WORKING_DIR, file_name), 'w').close()
                response = f"File '{file_name}' created."
            # Удаление файла
            elif command == "delete_file":
                file_name = parts[1]
                os.remove(os.path.join(WORKING_DIR, file_name))
                response = f"File '{file_name}' deleted."
            # Переименование файла или папки
            elif command == "rename":
                old_name = parts[1]
                new_name = parts[2]
                os.rename(os.path.join(WORKING_DIR, old_name), os.path.join(WORKING_DIR, new_name))
                response = f"Renamed '{old_name}' to '{new_name}'."
            # Запись содержимого в файл
            elif command == "write_file":
                file_name = parts[1]
                content = " ".join(parts[2:])
                with open(os.path.join(WORKING_DIR, file_name), 'w') as file:
                    file.write(content)
                response = f"Content written to '{file_name}'."
            # Чтение содержимого файла
            elif command == "read_file":
                file_name = parts[1]
                with open(os.path.join(WORKING_DIR, file_name), 'r') as file:
                    response = file.read()
            # Обработка неизвестных команд
            else:
                response = "Invalid command."

            # Отправляем ответ клиенту
            client_socket.send(response.encode('utf-8'))
    except Exception as e:
        # Отправляем сообщение об ошибке
        client_socket.send(f"Error: {str(e)}".encode('utf-8'))
    finally:
        # Закрываем соединение с клиентом
        client_socket.close()

# Основная функция запуска сервера
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создаем сокет
    server_socket.bind(('127.0.0.1', 9090))  # Привязываем сокет к адресу и порту
    server_socket.listen(5)  # Начинаем прослушивание подключений
    print("Server is running on port 9090...")
    while True:
        client_socket, addr = server_socket.accept()  # Принимаем соединение
        print(f"Connection established with {addr}")
        handle_client_request(client_socket)  # Обрабатываем запрос клиента

if __name__ == "__main__":
    start_server()