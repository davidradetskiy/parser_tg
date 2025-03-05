# Получение идентификатора и хеша API Telegram

Прежде чем работать с API Telegram, необходимо получить собственный идентификатор и хеш API:

Необходимо войти в свою учетную запись Telegram, указав номер телефона учетной записи разработчика. Страница [https://my.telegram.org](https://my.telegram.org) "Delete Account or Manage Apps". Далее нужно нажать "Инструменты разработки API": появится окно "Создать новое приложение". Заполните данные нового приложения. Нет необходимости вводить какой-либо URL-адрес, позже можно изменить только первые два поля (название приложения и краткое имя). В конце нажмите "Создать заявку".

Далее в файл `.env` добавьте `API_ID` и `API_HASH`.

# Запуск

Запустить скрипт можно командой:
```bash
./start.sh
```
Установятся зависимости, после чего попросит ввести номер телефона и код подтверждения. После этой процедуры создастся файл `anon.session`, который будет использоваться для работы с API Telegram, и больше не нужно запускать этот скрипт.

После этого можно запускать парсер командой:
```bash
docker-compose up --build
```

Логи парсера можно посмотреть в файле `parser.log`.

Времени было мало, поэтому пришлось собирать по-быстрому, не судите строго)))