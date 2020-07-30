# Парсер платежного поручения из PDF

## Описание
Полезность этого приложение в том, что оно позволяет из документа забирать номер платежного поручения не открывая файл. Вследствие экономит время сотрудников.

## Установка
Клонируем репозиторий на локальную машину:
```
$ git clone https://github.com/netshy/ParserPDFOrder.git
```
Создаем виртуальное окружение:
```
$ python -m venv venv
```
Устанавливаем зависимости:
```
$ pip isntall -r requirements.txt
```

## Запуск
```
$ python main.py
```

Запускаем скрипт первый раз для того, чтобы он создал 3 папки:
1. load - в нее нужно перемещать PDF файлы.
2. result - здесь хранятся переименованные файлы.
3. trash - сюда попадают файлы, которые не удалось переименовать.

<img src="https://i.ibb.co/yykhtF1/demo-min.gif"/>
