# API для базы фильмов, музыки, книг и других произведений  
Собирает отзывы, оценки и комментарии к отзывам пользователей на различные произведения через API.  

## Стек технологий  
Python, Django, Django REST framework, django-filter, Simple JWT, SQLite  

## Как развернуть API для Блога  

Создать окружение  
```  
python -m venv venv  
```  

Активировать окружение, обновить pip и установить зависимости  
```  
source venv/Scripts/activate  
python -m pip install --upgrade pip  
pip install -r requirements.txt  
```  

Применить миграции, по необходимости загрузить начальные данные и запустить сервер  
```  
python api_yamdb/manage.py migrate  
python api_yamdb/manage.py load_data  
python api_yamdb/manage.py runserver  
```  

По окончании использования деактивировать окружение  
```  
deactivate  
```  

## Разработчики по алфавиту
[Леонов Никита](https://github.com/KnowName90)  
[Мишустин Василий](https://github.com/vvvas), v@vvvas.ru, в том числе выполнял роль тим-лида  
[Селиверстов Михаил](https://github.com/MikhailDeveloper)
