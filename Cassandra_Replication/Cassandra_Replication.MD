### Сконфігурувати кластер з 3-х нод

```shell
 
 docker network create cassandra-network

 docker run --name cassandra-n1 -d --network cassandra-network -d cassandra:4.0
 docker run --name cassandra-n2 -d --network cassandra-network -e CASSANDRA_SEEDS=cassandra-n1 cassandra:4.0
 docker run --name cassandra-n3 -d --network cassandra-network -e CASSANDRA_SEEDS=cassandra-n1 cassandra:4.0
```

### Перевірити правильність конфігурації за допомогою nodetool status

```shell
docker exec cassandra-n1 nodetool status 
```

### Викоритовуючи  cqlsh, створити три Keyspace з replication factor 1, 2, 3

```shell
docker exec -it cassandra-n1 cqlsh

CREATE KEYSPACE IF NOT EXISTS ishop_rf1
WITH replication = {
  'class' : 'SimpleStrategy',
  'replication_factor' : 1
};

CREATE KEYSPACE IF NOT EXISTS ishop_rf2
WITH replication = {
  'class' : 'SimpleStrategy',
  'replication_factor' : 2
};

CREATE KEYSPACE IF NOT EXISTS ishop_rf3
WITH replication = {
  'class' : 'SimpleStrategy',
  'replication_factor' : 3
};

DESCRIBE KEYSPACES;
```

### В кожному з кейспейсів створити таблиці 

```shell
CREATE TABLE ishop_rf1.items_1(
   item_id int,
   category text,
   model text,
   producer text,
   price varint,
   screen_resolution text,
   properties map<text,text>,
   PRIMARY KEY (item_id)
   );

CREATE TABLE ishop_rf2.items_2(
   item_id int,
   category text,
   model text,
   producer text,
   price varint,
   screen_resolution text,
   properties map<text,text>,
   PRIMARY KEY (item_id)
   );

CREATE TABLE ishop_rf3.items_3(
   item_id int,
   category text,
   model text,
   producer text,
   price varint,
   screen_resolution text,
   properties map<text,text>,
   PRIMARY KEY (item_id)
   );

```

### Спробуйте писати і читати на / та з різних нод.
```shell
docker exec -it cassandra-n1 cqlsh
 
 
INSERT INTO ishop_rf1.items_1 (item_id, category, model, producer, price, screen_resolution, properties) VALUES (1, 'Phone', 'iPhone 6','Apple', 600, '720', {});
INSERT INTO ishop_rf2.items_2 (item_id, category, model, producer, price, screen_resolution, properties) VALUES (2, 'Phone', 'iPhone 7','Apple', 700, '720', {});
INSERT INTO ishop_rf3.items_3 (item_id, category, model, producer, price, screen_resolution, properties) VALUES (3, 'TV', 'smart tv 1212', 'Sumsung', 400, '4k', {'smart_tv': 'yes'});

select * from ishop_rf1.items_1;
select * from ishop_rf2.items_2;
select * from ishop_rf3.items_3;
```

### Вставте дані в створені таблиці і подивіться на їх розподіл по вузлах кластера (для кожного з кейспесов - nodetool status)


```shell
nodetool getendpoints -- <keyspase> <table> <row key>

docker exec cassandra-n1 nodetool getendpoints -- ishop_rf1 items_1 1
docker exec cassandra-n1 nodetool getendpoints -- ishop_rf2 items_2 2
docker exec cassandra-n1 nodetool getendpoints -- ishop_rf3 items_3 3
```

### Відключиіть одну з нод. Для кожного з кейспейсів визначить з якими рівнями consistency можемо читати та писати, і які з них забезпечують strong consistency 

```shell
docker stop cassandra-n1

docker exec -it cassandra-n2 cqlsh


CONSISTENCY ALL;  - No results for select form any keyspase, no insert
CONSISTENCY EACH_QUORUM;  - No results for select form any keyspase, no insert
CONSISTENCY QUORUM; - No results for select form any keyspase, no insert
CONSISTENCY LOCAL_QUORUM; - No results for select form keyspase 1 and 2, no insert for 1 nd 2. Insert and update works for keyspace 3
CONSISTENCY ONE; select and insert works for ishop_rf2.items_2; and from ishop_rf3.items_3; not working for ishop_rf1.items_1;
CONSISTENCY TWO; read from and insert for 3, 1 and 2 not able to select or update
CONSISTENCY THREE;  not able to select and insert for any of keyspaces
CONSISTENCY LOCAL_ONE; cannot read from 1, works fine for 2 and 3
CONSISTENCY ANY; no read from 1,2 and 3. able to insert into all tables
CONSISTENCY SERIAL; able to read only from 3, no inserts available
CONSISTENCY LOCAL_SERIAL; SERIAL; able to read only from 3, no inserts available
```

### Зробить так щоб три ноди працювали, але не бачили одна одну по мережі (відключити зв'язок між ними)

```shell
docker network disconnect cassandra-network cassandra-n1 
docker network disconnect cassandra-network cassandra-n2 
docker network disconnect cassandra-network cassandra-n3 
CONSISTENCY ONE; 
INSERT INTO ishop_rf3.items_3 (item_id, category, model, producer, price, screen_resolution, properties) VALUES (10, 'TV', 'smart tv 1212', 'Sumsung', 100, '4k', {'smart_tv': 'yes'});
INSERT INTO ishop_rf3.items_3 (item_id, category, model, producer, price, screen_resolution, properties) VALUES (10, 'TV', 'smart tv 1212', 'Sumsung', 200, '4k', {'smart_tv': 'yes'});

docker network connect cassandra-network cassandra-n1 
docker network connect cassandra-network cassandra-n2 
docker network connect cassandra-network cassandra-n3 


select * from ishop_rf3.items_3;

```

### Перевірте поведінку lightweight transactions для попередніх пунктів у розділеному на три частини кластері 

```shell
docker network disconnect cassandra-network cassandra-n1 
docker network disconnect cassandra-network cassandra-n2 
docker network disconnect cassandra-network cassandra-n3 

INSERT INTO ishop_rf3.items_3 (item_id, category, model, producer, price, screen_resolution, properties) VALUES (2, 'TV', 'smart tv 1212', 'Sumsung', 400, '4k', {'smart_tv': 'yes'})  IF NOT EXISTS;
```
