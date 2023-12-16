## 

[chaosblade](https://chaosblade.io/en/docs/getting-started/installation-and-deployment/tool-chaosblade-install-and-uninstall/)


Загрузка ЦПУ градиентно на 70-90-100%
```
blade create cpu load --cpu-percent 70 --timeout 300
```
Загрузка RAM градиентно на 95-100%
```
blade create mem load --mode ram --mem-percent 95 --timeout 300
```
Потеря пакетов на 7%
```
./blade create network loss --percent 7 --interface ens160 --local-port 5432
tc qdisc add dev <NET_INTERFACES> root netem loss 7%
```
Короткая задержка пакетов
```
tc qdisc add dev <NET_INTERFACES> root netem delay 100ms 250ms 25%
```
Закончилось место на диске с логами
```
blade create disk fill --path /logs/WAS --reserve 0 --timeout 600
```
Интенсивная чтение/запись на диск
```
blade create disk burn --read --write --path /logs/WAS --timeout 600
```
Атаки на JVM
```
blade c jvm oom --area HEAP --wild-mode true --pid\$JAVA_PID 
```

[Примеры](https://github.com/dastergon/awesome-chaos-engineering)


## Результат эксперемента

1. Описание эксперемента.

Цель 

![SRE_schema](https://thumb.tildacdn.com/tild6264-3134-4564-a431-333637333964/-/resize/760x/-/format/webp/image.png)


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

Описание нагрузочного тестировнаие [здесь](https://github.com/KKulishov/mts_sre/tree/main/Stress_testing)

1. сэмулровать избыточную нагрузку cpu на postgresql при нагрузочном тестировании
2. сэмулровать избыточную нагрузку mem на postgresql при нагрузочном тестировании
3. сэмулровать потерю пакетов на postgresql
4. Короткая задержка пакетов на postgresql

Примечание !!! Закончилось место на диске с логами такое не делал так как логи в отдном разделе что и сама БД , а при заканчивании места на БД , сама БД может вовердится. 


Узнаем master postgresql  вот так  , на одном из узле patroni
```
patronictl list -f json | jq -r '.[] | select(.Role == "Leader") | .Member'
db1
```

заходим на db1 и на него ставим chaosblade
```
# 1. download tar
wget https://github.com/chaosblade-io/chaosblade/releases/download/v1.7.2/chaosblade-1.7.2-linux-amd64.tar.gz
# 2. unzip and entry chaosblade directory
tar -xvf chaosblade-1.7.2-linux-amd64.tar.gz && cd chaosblade-1.7.2/
```

паралельно поднимаем наргузочное тестирование как описано здесь [здесь](https://github.com/KKulishov/mts_sre/tree/main/Stress_testing)

1. на db1 

```
blade create cpu load --cpu-percent 70 --timeout 300
```

приводит к увелению обработки запросов от сервиса что влечет за собой увеличиный latency

[latency_locust](https://drive.google.com/file/d/1gR4STOr3TTSKgTqaI9R9VTDrZOd-Fzd-/view?usp=drive_link)
[latency_blackbox](https://drive.google.com/file/d/1-CsJnqR6Hx5qnv4ybDQOGy6IfIbn7Kes/view?usp=drive_link)


2. на db1 нагрузка по памяти 95%

```
./blade create mem load --mode ram --mem-percent 95 --timeout 300
```
Влечет за собой высокий LA на сервере, что влечет за собой увелечения latency

в логах приложения, пример
```
[11:33:30 INF] Executed action SreCourseApi.Controllers.WeatherForecastController.Get (SreCourseApi) in 32918.441ms
```
при дальнешей нагрузи появлятя 500. 

[url_500](http://5eca9364-3899-4021-b861-fd4f64e48c6d.mts-gslb.ru/d/7GKkdrGIz/4-golden-signal?orgId=1)


3. на db1 потеря пакетов в 7% для порта postgresql

```
./blade create network loss --percent 7 --interface ens160 --local-port 5432
```

приводит к появлению 500 со стороны сервиса 
[500](https://drive.google.com/file/d/1LmAwFSnV7uqFGdAPZREW5-YJwBq02EKR/view)



4. Короткая задержка сетевых пакетов на postgresql
```
./blade create network delay --time 300 --offset 1000 --interface ens160 --local-port 5432
```

при задержке пакетов видим резкое уведечения lantency ответа
[latency_locust_1](https://drive.google.com/file/d/1galTJ9f1igSyZGzu0yXJ9HO8fj42kFj1/view?usp=drive_link) 
[latency_ingress](http://5eca9364-3899-4021-b861-fd4f64e48c6d.mts-gslb.ru/d/7GKkdrGIz/4-golden-signal?orgId=1) 


Посмотреть статусы зап. задач
```
./blade status --type create
```


Итоги вывода. 

1. Нужно следить за LA БД и доступности ОЗУ и процессорного времени. 
2. Так же следит за стабильностью работы сети. 
3. Нагрузку по cpu и mem не делал так как при нагрузочном тестировании и так описал что приложение в кубере упирается в cpu  ипроисходит тротлинг cpu что влечет к появлению 5xx а при исчерпании памяти идет рестарт (OOM приходит). 



