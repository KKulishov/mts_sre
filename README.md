### SRE

Цель построения 

![SRE_schema](https://thumb.tildacdn.com/tild6264-3134-4564-a431-333637333964/-/resize/760x/-/format/webp/image.png)


Построить postgesql + patroni  [пример](https://github.com/vitabaks/postgresql_cluster)

Накатить приложение в кубер 

### Приложение в kubernetes 
Написать helm chart для разворачивания api в выделенном неймспейсе. Docker image лежит в публичном registry, разворачивать стоит актуальную версию ghcr.io/ldest/sre-course/api
[пример образа](https://github.com/ldest/SreCourseApi/pkgs/container/sre-course%2Fapi)


нюансы по app 
```
- DOTNET_ENVIRONMENT переменную выставляете в Development и вперед
- /app/Migrations/init.sql
```

описание сети в hub.cloud.mts.ru

подсеть network -- sre -- 192.168.10.0/24 

```
haproxy -- (haproxy) точка входа через внешку 91.185.85.240
db1 -- (patroni + postgresql + haproxy) 192.168.10.3
db2 -- (patroni + postgresql + haproxy) 192.168.10.4
etcd1 -- (etcd)  192.168.10.5
etcd2 -- (etcd)  192.168.10.6
etcd3 -- (etcd)  192.168.10.7
```

### деплой postgresql

```sh
git clone https://github.com/vitabaks/postgresql_cluster.git
```

Заменить postgresql_cluster_my/inventory и postgresql_cluster_my/vars/main.yml  на свои 


!!! скорректировать значения postgresql_cluster_my/inventory под своей проект !!!
!!! перед этим в vars/main.yml заменить пароли с "xxx" на свои !!!

```sh
cp postgresql_cluster_my/inventory postgresql_cluster/inventory
cp postgresql_cluster_my/vars/main.yml postgresql_cluster/vars/main.yml
```

### деплой приложения через helm

!!! скорректировать значения в sre_app/.kube/app/values.yaml в поле ConnectionStrings__PgConnection под свои значения которые были указанны ранее в postgresql_cluster !!!

само приложение описано в helm шаблоне в каталоге sre_app/.kube/app


установка в кубере 
```sh
./helm upgrade --install -n sre-cource-student-53 --namespace sre-cource-student-53 app sre_app/.kube/app/
```


### Проверка работы сайта

Описание [swagger](http://sre-app.rndhelp.ru/swagger/index.html)

Проверка подключения к БД [check_city](http://sre-app.rndhelp.ru/cities)