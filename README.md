[[_TOC_]]

# Описание проекта

Скелет базового django-проекта.
Позволяет быстро создавать новые django-проекты не заботясь о предварительной настройке проекта.
Может использоваться как совместно с `virtualenv` так и быть собран в Docker-образ.


## Структура проекта

- `src/` -каталог, в котором ведется вся разработка
- `src/apps/` - каталог с django-приложениями, создаваемыми в новом проекте
- `src/settings/` - 
- `src/templates/` - 
- `src/static/` - 
- `pip/` - каталог, куда должны быть скопированы, либо подключены pip-пакеты, являющиеся внутренней разработкой и не доступные из публичного pip, либо модифицированные (с исправленными ошибками) версии публично доступных библиотек
- `requirements.txt` - файл, с описанием зависимостей
- `data/` - данные, с которыми работает приложение
- `data/private/` - каталог с приватными данными, доступ к которым должен быть только у приложения
- `data/static/` - каталог, куда будет выполняться `collectstatic`. Можно шарить веб-серверу, бэкендом для которого служит данное приложение.
- `data/media/` - каталог, куда будут по умолчанию сохраняться файлы приложением. Можно шарить веб-серверу, бэкендом для которого служит данное приложение.


# Способ использования

## Создание полной копии данного пректа

```sh
mkdir new_project
cd new_project
git init
git remote add djangoskel git@github.com:mavriq/djangoskel.git
git checkout djangoskel/master .
git status
git commit -m "Initialized by djangoskel"
```


## Создание копии для запуска проекта в virtualenv

### Создание копии проекта

```sh
mkdir new_project
cd new_project
git init
git remote add djangoskel git@github.com:mavriq/djangoskel.git
git checkout djangoskel/master \
    --recurse-submodules \
    .gitignore \
    src \
    data \
    pip \
    requirements.txt
git status
git commit -m "Initialized by djangoskel"
```

### Предварительная настройка virtualenv

Данный пример описывает настройку virtualenv для использования `python2.7`

```sh
virtualenv \
    --python=python2.7 \
    .
. ./bin/activate
pip install -r requirements.txt
```

## Создание копии проекта для использования в составе docker-контейнера

### Создание копии проекта

```sh
mkdir new_project
cd new_project
git init
git remote add djangoskel git@github.com:mavriq/djangoskel.git
git checkout djangoskel/master .
```

### Сборка контейнера и запуск локальной разработки

