import select
import socket
import sqlite3

SERVER_ADDRESS = ('localhost', 8686)
MAX_CONNECTIONS = 10
INPUTS = list()
OUTPUTS = list()


def get_non_blocking_server_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    server.bind(SERVER_ADDRESS)
    server.listen(MAX_CONNECTIONS)
    return server


def handle_readables(readables, server):
    for resource in readables:
        if resource is server:
            connection, client_address = resource.accept()
            connection.setblocking(0)
            INPUTS.append(connection)
            print(f"Новое подключение от {client_address}")
            continue

        try:
            data = resource.recv(1024).decode('utf-8')
            if not data:
                clear_resource(resource)
                continue

            print(f"Получен запрос: {data}")

            # Обработка тестового запроса
            if data.strip() == "PING":
                resource.sendall(b"PONG")  # Явная отправка
                print("Отправлен PONG")
                continue

            # Обработка SQL-запросов
            conn = None
            try:
                conn = sqlite3.connect("users.sqlite")
                cursor = conn.cursor()

                if "|||" in data:
                    query, params_str = data.split("|||", 1)
                    params = eval(params_str)
                    cursor.execute(query, params)
                else:
                    cursor.execute(data)

                result = cursor.fetchall()
                conn.commit()
                response = str(result).encode('utf-8')
                resource.sendall(response)  # Явная отправка
                print(f"Отправлен ответ: {response}")

            except Exception as e:
                error_msg = f"Error: {str(e)}".encode('utf-8')
                resource.sendall(error_msg)
                print(f"Отправлена ошибка: {error_msg}")

        except ConnectionResetError:
            print("Клиент разорвал соединение")
        except Exception as e:
            print(f"Ошибка обработки: {e}")
            # Не закрываем соединение явно!
        if conn:
            conn.close()






def clear_resource(resource):
    if resource in OUTPUTS:
        OUTPUTS.remove(resource)
    if resource in INPUTS:
        INPUTS.remove(resource)
    resource.close()
    print(f"Closing connection {resource}")


def handle_writables(writables):
    for resource in writables:
        try:
            resource.send(bytes('Hello from server!', encoding='UTF-8'))
        except OSError:
            clear_resource(resource)


if __name__ == '__main__':
    server_socket = get_non_blocking_server_socket()
    INPUTS.append(server_socket)
    print("Server is running, press Ctrl+C to stop")
    try:
        while INPUTS:
            readables, writables, exceptional = select.select(INPUTS, OUTPUTS, INPUTS)
            handle_readables(readables, server_socket)
            handle_writables(writables)
    except KeyboardInterrupt:
        clear_resource(server_socket)
        print("Server stopped!")