# Запросы к web-приложению (API).
import requests
# Преобразование.
import json
# Использования файла конфигурации.
from configparser import ConfigParser 


# Переменная для работы 'ConfigParser'.
config = ConfigParser() 
# Прочесть файла конфигурации.
config.read('config.ini')

# Переменная для хранения Токена телеграмм (прочитан с файла).
telegramAccessToken = config.get('TELEGRAM', 'telegramAccessToken')
# Переменная для хранения ссылки запросов (прочитана с файла).
telegramUrl = config.get('TELEGRAM', 'telegramUrl')

# ====================== Функции ======================
def main():
    '''
        Основная функция для работы скрипта, производит запуск остальных ф-ций.
    '''

    # Переменная для хранения 'id_update'(необходим для отправки на сервер при long-Pooling).
    # (на оснеовании 'id_update' сервер понимает, какой последний update мы получили).
    offset = None

    while True:
        print(f'[Отладочное сообщение] цикл WHile начался')
        # Обрабатываем отправку запроса GET (получаем последние события).
        try:
            # Параметры запроса
            params = {
                       'timeout': 30,       # Сервер держит соединения 30 секунд (Long-Pooling), при появлении ответа сразу его высылает.
                        'offset': offset    # 'id_update', следующий после последнего полученного.
                     }
            # Запрос (get) на получения последнего события.
            r = requests.get(
                                f"{telegramUrl}{telegramAccessToken}/getUpdates",
                                data = params
                            )
            # Переменная для хранения ответа от  сервера в json.
            data = r.json()
            print(f'[Отладочное сообщение] запрос GET-выполнен успешно (Long-Pooling)')
        # В случае неудачного запроса (при ошибке).
        except: 
            print(f'[Отладочное сообщение] запрос GET-выполнен не выполнен')
            # Возвращаемся в начало цикла While.
            continue

        # Условие выполняется только в том случае, если в ответе на GET запрос ['result]: пустой.
        if  not data['result']: 
            print(f'[Отладочное сообщение] новых событий не произошло')
            # Возвращаемся в начало цикла While.
            continue
        
        # Условие выполняется только в том случае, если внутри ответа на GET запрос есть ключ 'text'.
        if 'text' in data['result'][0]['message']:
            print(f'[Отладочное сообщение] внутри запроса GET- найден текст сообщения')
            # Переменная для хранения имени пользователя.
            userName = data['result'][0]['message']['from']['username']
            # Переменная для хранения сообщении пользователя.
            userMessage = data['result'][0]['message']['text']
            # Переменная для хранения даты отправки сообщения пользователем.
            userMessageDate = data['result'][0]['message']['date']
            # Переменная для хранения ID-чата с пользователем.
            userChatId = data['result'][0]['message']['chat']['id']

            # Обрабатываем отправку запроса POST (отправляем пользователю ответ на сообщение).
            try:
                # Параметры запроса.
                params = {
                            "chat_id": userChatId,     
                                "text": userMessage   
                            }
                # # Запрос (post) на отправку сообщения пользователю.
                r = requests.post(
                                    f"{telegramUrl}{telegramAccessToken}/sendMessage",
                                    data = params
                                ).json()
                print(f'[Отладочное сообщение] Запрос POST-отправлен успешно')
            # В случае неудачного запроса (при ошибке)
            except: 
                print(f'[Отладочное сообщение] Запрос POST-отправлен не отправлен')
                pass

            # Переменная для хранения 'id_update'(необходим для отправки на сервер при long-Pooling),
            # (на оснеовании 'id_update' сервер понимает, какой последний update мы получили),
            # увеличиваем 'id_update' на 1 от последнего полученного.
            offset = data['result'][0]['update_id'] + 1
            
# Условие: файл запускается самостоятельно (не импортирован в виде модуля).
if __name__ == '__main__':
    # Обработка исключений
    try:
        # Запускаем выполнения основной ф-ции.
        main()
    # исключение на 'ctrl+c'
    except KeyboardInterrupt:
        exit()

        

            
