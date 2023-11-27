### SRE

Цель построения 

![SRE_schema](https://thumb.tildacdn.com/tild6264-3134-4564-a431-333637333964/-/resize/760x/-/format/webp/image.png)


Построить postgesql + patroni  [пример](https://github.com/vitabaks/postgresql_cluster)

Накатить приложение в кубер 

### Приложение в kubernetes 
Написать helm chart для разворачивания api в выделенном неймспейсе. Docker image лежит в публичном registry, разворачивать стоит актуальную версию ghcr.io/ldest/sre-course/api
[пример образа](ghcr.io/ldest/sre-course/api)


нюансы по app 
```
- DOTNET_ENVIRONMENT переменную выставляете в Development и вперед
- /app/Migrations/init.sql
```

описание сети в hub.cloud.mts.ru

подсеть network -- sre -- 192.168.10.0/24 

```
haproxy -- (haproxy) точка входа через внешку 91.185.85.240  -- внутринний адрес 192.168.10.2
db1 -- (patroni + postgresql + haproxy) 192.168.10.3
db2 -- (patroni + postgresql + haproxy) 192.168.10.4
etcd1 -- (etcd)  192.168.10.5
etcd2 -- (etcd)  192.168.10.6
etcd3 -- (etcd)  192.168.10.7
```

```
namespace sre-cource-student-53
site name http://sre-app.rndhelp.ru
```

вывод списка городов http://sre-app.rndhelp.ru/cities , пока таблица пустая. 

### деплой postgresql

```sh
git clone https://github.com/vitabaks/postgresql_cluster.git
```

Заменить postgresql_cluster_my/inventory и postgresql_cluster_my/vars/main.yml  на свои 


!!! скорректировать значения postgresql_cluster_my/inventory под своей проект !!!
!!! перед этим в vars/main.yml заменить пароли с "xxx" на свои !!!

в моем случае изменить
```
patroni_superuser_password: "xxx" 
patroni_replication_password: "xxx" 
pgbouncer_auth_password: "xxx"
monitoring_password: "xxx"
user_password: "xxx"
```

```sh
cp postgresql_cluster_my/inventory postgresql_cluster/inventory
cp postgresql_cluster_my/vars/main.yml postgresql_cluster/vars/main.yml
```


Подключаемся к БД  (прошу обратить внимание что подкл. через gw в DMZ 192.168.10.0/24) но из внешки хост 91.185.85.240 
```sh
# тут указать пароль который указывали ранее
psql -U postgresql -h 192.168.10.3 -p 5000 -W
# Создаем БД sre
CREATE DATABASE sre; 
# выдаем права для mydb-user
GRANT ALL PRIVILEGES ON DATABASE sre TO "mydb-user";
```

после этого извлекаем из образа (https://github.com/ldest/SreCourseApi/pkgs/container/sre-course%2Fapi) проекта sql миграцию , расположениую в /app/Migrations/init.sql и накатываем в БД sre

```
psql -U mydb-user -h 192.168.10.3 -p 5000 -W -d sre

# создаем в БД  sre структуру 
create table if not exists public.cities
(
    id   bigserial,
    name varchar(255)
);

create table if not exists public.forecast
(
    id          bigserial,
    "cityId"    bigint,
    "dateTime"  bigint,
    temperature integer,
    summary     text
);
```


### деплой приложения через helm

!!! скорректировать значения в sre_app/.kube/app/values.yaml в поле secret под свои значения которые были указанны ранее в postgresql_cluster !!!

парметры подключения к БД уже открыто указаны в sre_app/.kube/app/values.yaml в secret кроме password, его зададим в ручную или через CI/CD 

само приложение описано в helm шаблоне в каталоге sre_app/.kube/app

установка в кубере (пример):
```sh
helm upgrade --install -n sre-cource-student-53 --namespace sre-cource-student-53 --set secret.app.password="xxx" app sre_app/.kube/app/
```

### Проверка работы сайта

Описание [swagger](http://sre-app.rndhelp.ru/swagger/index.html)

Проверка подключения к БД [check_city](http://sre-app.rndhelp.ru/cities)