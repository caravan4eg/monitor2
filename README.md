# TenderMonitor Service
## Для чего и что делает
ТендерМонитор разрабатывался как учебный проект, хотя задачи решает вполне реальные. 
Сервис собирает доступные публичные данные об объявленных тендерах в интернет, 
формирует и обновляет базу данных, выдает информацию из базы данных по простым и сложным запросам. 
Была попытка сделать подбор информации по отраслям экономики путем анализа ключевых понятий, характерных для соответсвующей области, 
но отвергнута как очень ресурсоемкая задача. 
В настоящее время  поиск реализован через фильтрацию по ключевым словам в соответствующих полях БД.
Наличие API позволяет "прикрутить" к сервису любой фронт или использовать его в мобильном приложении.

## Какие технологии задействованы
Для построения бэкэнда в проекте задействованы: 
* Django 
* Django Rest Framework 
* Python 
* В качестве базы данных используется
* PostgreSQL 
* Для формирования датасета и пополнения базы данных применен Scrapy 
* Задачи по обновлению БД запускаются в фоне по расписанию. Для решения этих задач использовались Redis и Celery.
* В качестве рабочего варианта сделан фронт с помощью Bootstrap.

## Адреса
1. Доступ к через browsable API: [https://tender-ms.herokuapp.com/api/v1/](https://tender-ms.herokuapp.com/api/v1/)
2. Доступ к обычному html: ["https://tender-ms.herokuapp.com"](https://tender-ms.herokuapp.com).
