## Мониторинг

Цель мониторинга

![monitoring](https://static.tildacdn.com/tild3063-6263-4531-a233-633939643433/__2023-10-13__143032.png)

дашборды grafana(./grafana_dashboard) [link](http://5eca9364-3899-4021-b861-fd4f64e48c6d.mts-gslb.ru/dashboards/f/M4CESrGSz/kulishov-konstantin)

rule правила для promethrues для 4 золотых сигнала(./alertmanager/4_gold_signal)

посмотреть можно [здесь](http://91.185.85.240:9090/classic/alerts) 

1. описание алертов по насыщению(capability  ./alertmanager/4_gold_signal/capability.yaml)   

| Имя алерта        | Описание        | Runbook           |
|-------------------|:---------------:|------------------:|
| HostHighCpuLoad   | CPU > 80% на VM |                   |
| HostOutOfMemory   | на vm осталось  менее 10% памяти  |                   | 
| HostOutOfDiskSpace| место на диске менее 10%   |                   |                       

2. описание алертов по error (error  ./alertmanager/4_gold_signal/error.yaml)   

| Имя алерта                 | Описание                     | Runbook           |
|----------------------------|:----------------------------:|------------------:|
| PostgresqlDeadLock         | блокировки Postgresql        |                   |
| HostNetworkReceiveErrors   | Ошибки приема хост-сети      |                   |
| HostNetworkTransmitErrors  | Ошибки передачи в сети хоста |                   |
| BlackboxProbeFailed        | Проверка blackbox не удалась |                   |
| BlackboxProbeHttpFailure   | Проверка blackbox не удалась |                   |


3. описание алертов по latency (latency ./alertmanager/4_gold_signal/latency.yaml) 

| Имя алерта                       | Описание                             | Runbook           |
|----------------------------------|:------------------------------------:|------------------:|
| BlackboxSlowProbe                | Медленный запрос с blackbox          |                   |
| Longest_Transaction_Postgresql   | Медленный транзакции к БД            |                   |
| UnusualDiskReadLatency           | время на четение к диску             |                   |
| UnusualDiskWriteLatency          | время на запись к диску              |                   |
| BlackboxProbeSlowHttp            | Медленный запрос с http от blackbox  |                   |
| HostUnusualDiskIo                | Время на IO к диску                  |                   |

4. описание алертов по traffic (traffic ./alertmanager/4_gold_signal/traffic.yaml) 

| Имя алерта                       | Описание                             | Runbook           |
|----------------------------------|:------------------------------------:|------------------:|
| PostgresqlTooManyConnections     | кол-во запросов к БД > 80%           |                   |
| HostUnusualNetworkThroughputIn   | Входящий траффик сет. на vm более MB/s            |                   |
| HostUnusualNetworkThroughputOut  | Исходящий траффик сет. на vm более MB/s           |                   |


Примичание!!!
  1. не стал покрывать etcd и haproxy, посчитал доп. оверхедом. основ. примеры показаны. Хотя в жизни покрылбы и их.   

ошибки со стороны ingress-nginx не могу натсроить так к прометею не могу обратиться из свой подсети 
latency со стороны ingress-nginx не могу натсроить так к прометею не могу обратиться из свой подсети 
traffic (rps) со стороны ingress-nginx не могу натсроить так к прометею не могу обратиться из свой подсети  
capability не могу  со стороны prometheus получить метрики по container(cpu/mem/iops)
error  ситуация аналогичная 

[примеры алертинга](https://samber.github.io/awesome-prometheus-alerts/)

