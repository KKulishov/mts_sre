### Нагрузочное тестирование 

Цель 
```
http://sre-app.rndhelp.ru/Cities
http://sre-app.rndhelp.ru/Forecast
http://sre-app.rndhelp.ru/WeatherForecast
```

Описание api [проекта](http://sre-app.rndhelp.ru/swagger/index.html)

### Инструмент Locust 

docs [Locust](https://docs.locust.io/en/stable/quickstart.html)

установка (зависимость python3)
```sh
pip3 install locust
```

до материалы (https://www.blazemeter.com/blog/locust-python , https://github.com/locustio/locust/issues/1896, https://www.youtube.com/watch?v=_Z62E46bDmY&t=2458s, https://github.com/NikolaiMaximov/heisenbug_2022/blob/main/demo_code/http_max_perf.py) 


параметры запуска, где  -H указываем на какой хост вести запросы , -u кол-во пользв. , -r кол-во запросов от польз.  , параметр autostart означает, что сразу запускаем тест. 
```sh
locust -f sre.py -H http://sre-app.rndhelp.ru -u 2160 -r 20 --autostart
```


в данный скрипт доб. точка прирывани при условии если проверяемый роут престал отдавать 200 код ответа. Вообще в коде в функции handle_response в коментах я указал что прерывать можно разными спосабами. 

Так же можно запускать мульти задачу или оформить все тесты в одной единой. 

В моем примеры оформил как мульти задачей с разным интервалом запуска задач.

Идет рандом id проверка по списку общему из /Cities и по нему же идет рандом. изменение через PUT данныз по темерауре (примерчение PUT делается не так чвасто так как в реалиях температура не так чатсо меняется. Все отразил в итог. скрипте)

Применил self.user.stop() так как self.interrupt() останавливается на вермя но потом после того как сервис начинает работать заанова запускает тестирование. каждый метод интересен при разных условиях тестирования при ручном или автоматическом. 

### Dashboard метрик 
[общий](http://5eca9364-3899-4021-b861-fd4f64e48c6d.mts-gslb.ru/dashboards/f/M4CESrGSz/kulishov-konstantin)

[4GoldenSignal](http://5eca9364-3899-4021-b861-fd4f64e48c6d.mts-gslb.ru/d/7GKkdrGIz/4-golden-signal?orgId=1&from=now-3h&to=now)

[PostgeSql](http://5eca9364-3899-4021-b861-fd4f64e48c6d.mts-gslb.ru/d/5474745/postgresql-overview-postgres_exporter?orgId=1&refresh=5m)

[Ingress](http://5eca9364-3899-4021-b861-fd4f64e48c6d.mts-gslb.ru/d/nginxvdvsdv/nginx-ingress-controller?orgId=1&refresh=5s)

[etcd](http://5eca9364-3899-4021-b861-fd4f64e48c6d.mts-gslb.ru/d/dsvsdvsbrjrwew/etcd?orgId=1)

[NodeExporter](http://5eca9364-3899-4021-b861-fd4f64e48c6d.mts-gslb.ru/d/rYdddlPWksdvsdvsd/node-exporter-full?orgId=1)

[KuberDeployment](http://5eca9364-3899-4021-b861-fd4f64e48c6d.mts-gslb.ru/d/k8s_views_pods/kubernetes-views-pods?orgId=1&var-datasource=Prometheus&var-namespace=sre-cource-student-53&var-pod=app-f8cf557fb-g56sn&var-resolution=30s&from=1701084617407&to=1701085489616)

### Итог тестирования 

После проведенния нагрузочного тестирования было при ~ 560 rps/s (примерно 2160 пользователей ) было зафиксировано след., что приложение упирается в лимиты по ЦПУ в kubernetes (идет treshold cpu),  для того чтобы преодалеть узкое горлышко  нужно увеличить кол-во реплик приложения и/или поднять лимиты по ЦПУ для приложения. 


Вот скриншот по ingress
[ingress_traffic](https://drive.google.com/file/d/1R9b0qePLF06HfiqYzsozvmcEIEDM4hha/view?usp=drive_link)

Вот скриншот по db 
[traffic_db](https://drive.google.com/file/d/1ns2XJ4gpi4_fbDGDGCwsoM_bO8ogNtSG/view?usp=drive_link)
[connect_db](https://drive.google.com/file/d/1joGdcR9QN7_9MHP6lD7CIjg6M_ez6iig/view?usp=drive_link)

Вот скриншот по статистики от самого locust
[static_locust](https://drive.google.com/file/d/15g5fI0IOaBjetODk5we90E_PgnVFeoIJ/view?usp=drive_link)
[static_locust_2](https://drive.google.com/file/d/1r4nZP_0NDsrRm9ArJHBeD1tywVtGuO0t/view?usp=drive_link)

Вот скриншот по появлению 
[5xx](https://drive.google.com/file/d/1YjqzVfMKYomo92KFQVzNm6gU3jeTiBkz/view?usp=drive_link)

Рост кол-во latency при нагрузочном тестировании
[latency](https://drive.google.com/file/d/1x_paZppLy0u600bev9fM3ZZd9PETV64k/view?usp=drive_link)

А вот как раз скрин когда упираюсь в лимиты  
[cpu_limits](https://drive.google.com/file/d/1LFaWCb0iLKcHRyNjBPBP5Obhce0uf7b4/view?usp=drive_link)


