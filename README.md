# NashSGO - телеграм бот для взаимодействия с "Сетевым Городом"

## Техническое задание

### Цель
* Целью проекта является реализация бота на python с использованием aiogram для работы с telegram, неофициального API для Сетевого Города - netschooloapi. База данных - sqlite, взаимодействие с ней через sqlalchemy

### Возможности бота
* Авторизация школьника в системе СГО
* Просмотр расписания
* Просмотр предстоящих домашних заданий
* Просмотр оценок за день
* Создание отчетов об успеваемости

### Запуск на своей машине

* Клонируем [репозиторий](https://github.com/erytw/NashSGO)
```shell
git clone https://github.com/erytw/NashSGO.git
```

* Переходим в каталог репозитория и устанавливаем зависимости
```shell
cd NashSGO
pip install -r requirements.txt
```

* Переименовываем ```config_``` в ```config```
  - Для linux
  ```shell
  mv congig_ config
  ```
  - Для Win
  ```shell
  ren congig_ config
  ```
* Переходим в ```/config``` и в файле ```config.yaml``` вставляем свой BotToken, полученный у @BotFather и id чата для для ошибок
* Применяем миграции
```shell
  alembic upgrade head
  ```
* Запускаем бота
```shell
python3 -m app
```
