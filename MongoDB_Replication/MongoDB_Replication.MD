### Налаштувати реплікацію в конфігурації: Primary with Two Secondary Members (всі ноди можуть бути запущені як окремі процеси або у Docker контейнерах)

```shell
docker network create mongo-cluster

docker run -p 30001:27017 --name mongo1 --net mongo-cluster -d mongo mongod --replSet my-mongo-set
docker run -p 30002:27017 --name mongo2 --net mongo-cluster -d mongo mongod --replSet my-mongo-set
docker run -p 30003:27017 --name mongo3 --net mongo-cluster -d mongo mongod --replSet my-mongo-set

docker exec -it mongo1 mongo

db = (new Mongo('localhost:27017')).getDB('test')
config = {"_id" : "my-mongo-set", "members" : [{"_id" : 0,"host" : "mongo1:27017"},{"_id" : 1,"host" : "mongo2:27017"},{"_id" : 2,"host" : "mongo3:27017"}]}

rs.initiate(config)
```

### Продемонструвати запис даних на primary node з різними Write Concern Levels

* Unacknowledged - Requests no acknowledgment of the write operation. However, w: 0 may return information about socket exceptions and networking errors to the application. Data can be rolled back if the primary steps down before the write operations have replicated to any of the secondaries.

```shell
db.products.insert(
   {category: "Phone", model: "iPhone 6",producer: "Apple",price: 600, screen_resolution: 720 },
   { writeConcern: { w: 0 , wtimeout: 5000 } }
)
```

* Acknowledged - Requests acknowledgment that the write operation has propagated to the standalone mongod or the primary in a replica set. w: 1 is the default write concern for MongoDB. Data can be rolled back if the primary steps down before the write operations have replicated to any of the secondaries.

```shell
db.products.insert(
   {category: "Phone", model: "iPhone 7",producer: "Apple",price: 700, screen_resolution: 720 },	
   { writeConcern: { w: 1 , wtimeout: 5000 } }
)
```

* Journaled - The j option requests acknowledgment from MongoDB that the write operation has been written to the on-disk journal. To provide durability in the event of a failure, MongoDB uses write ahead logging to on-disk journal files.


```shell
db.products.insert(
   {category: "TV", model: "smart tv 1212",producer: "Samsung",price: 400, screen_resolution: 1080, smart_tv: "yes" },
   { writeConcern: { w: 1 , j: true, wtimeout: 5000} }
)
```

* AcknowledgedReplica - Any data-bearing voting member of the replica set can contribute to write acknowledgment of "majority" write operations. j=true Acknowledgment requires writing operation to on-disk journal.
```shell
db.products.insert(
   {category: "TV", model: "smart tv 100",producer : "LG","price" : 350, "screen resolution": 4000, smart_tv: "No" },
   { writeConcern: { w: "majority" , wtimeout: 5000} }
)
```

```shell
db.getCollection("products").find({}).pretty();
```

### Продемонструвати Read Preference Modes: читання з primary і secondary node (http://docs.mongodb.org/manual/core/read-preference/)
#### Primary is set by default 
```shell
db.getMongo().setReadPref('secondary')
```

```shell
Read Preference Mode: primary, primaryPreferred, secondary, secondaryPreferred, nearest
```

### Спробувати зробити запис з однією відключеною нодою та write concern рівнім 3 та нескінченім таймаутом. Спробувати під час таймаута включити відключену ноду 
### By not specifying the wtimeout the timeout will be infinitive 
```shell
docker stop mongo2
```

```shell
db.products.insert(
  {category: "Laptop", model: "thinkpad",producer : "Lenovo","price" : 1250, screen_resolution: 1080, specs: {"processor": "Intel Core i7", "RAM": 16, "SSD": "512 GB"} },
  { writeConcern: { w: 3} }
)
```

### Аналогічно попередньому пункту, але задати скінченний таймаут та дочекатись його закінчення. Перевірити чи данні записались і чи доступні на чиіання з рівнем readConcern: “majority”
```shell
docker stop mongo2
```
```shell
db.products.insert(
{category: "Laptop", model: "latitude 5400",producer : "Dell","price" : 1350, screen_resolution: 1080, specs: {"processor": "Intel Core i7", "RAM": 16, "SSD": "1 TB", "OS":"linux"} },
{ writeConcern: { w: 3 , wtimeout: 5000} }
 )
```

```shell
db.products.find({ $and: [ { category: "Laptop"}, { producer: "Dell"}, { model: "latitude 5400"} ] }).readConcern("majority").pretty();
```
```shell
Дані доступні
```

### Продемонстрував перевибори primary node в відключивши поточний primary (Replica Set Elections) - 

```shell
docker stop mongo1
```

```shell
docker exec -it mongo2 mongo

db.products.insert(
{category: "Smart watch", model: "Marq Captain American Magic Edition",producer: "Garmin",price: 1800, screen_resolution: 240, batary_life: "21 day" },
{ writeConcern: { w: 0 , wtimeout: 5000} }
 )
```

```shell
docker start mongo1
docker exec -it mongo1 mongo
db.getMongo().setReadPref('nearest')

db.products.find({ $and: [ { category: "Smart watch"}, { model: "Marq Captain American Magic Edition"}, { producer: "Garmin"} ] }).pretty();

```

### Привести кластер до неконсистентного стану користуючись моментом часу коли primary node не відразу помічає відсутність secondary node 


```shell
db.products.insert(
{category: "Earbuds", model: "AirPods Pro",producer: "Apple",price: 250, screen_resolution: 240, batary_life: "5h" },
  { writeConcern: { w: 1} }
)
```

```shell
docker stop mongo3
```

```shell
db.products.find({}).readConcern("majority").pretty();
db.products.find({}).readConcern("local").pretty();
db.products.find({}).readConcern("linearizable").pretty();
```


### Земулювати eventual consistency за допомогою установки затримки реплікації для репліки 

```shell
# set delay on mongo2 
cfg = rs.conf()
cfg.members[1].priority = 0
cfg.members[1].hidden = true
cfg.members[1].slaveDelay = 30
rs.reconfig(cfg)

db.getMongo().setReadPref('nearest')

db.products.insert(
 {category: "Smart watch", model: "Vantage V",producer: "Polar",price: 420, screen_resolution: 240, batary_life: "20 days" },
 )
   
db.products.find({})
```


### Лишити primary та secondary для якої налаштована затримка реплікації. Записати декілька значень. Спробувати прочитати значення з readConcern: {level: "linearizable"}
### Має бути затримка поки значення не реплікуються на більшість нод

```shell
docker stop mongo3
db.products.find({}).readConcern("linearizable").pretty();
```
