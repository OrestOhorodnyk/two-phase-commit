### Run cassandra
```shell
 docker network create cassandra-network

 docker run --name cassandra-n1 -d --network cassandra-network cassandra:4.0
 docker run --name cassandra-n2 -d --network cassandra-network -e CASSANDRA_SEEDS=cassandra-n1 cassandra:4.0
 docker run --name cassandra-n3 -d --network cassandra-network -e CASSANDRA_SEEDS=cassandra-n1 cassandra:4.0
```

### Run cqlsh
```shell
docker exec -it cassandra-n1 cqlsh
```

### Create key space
```shell
CREATE KEYSPACE IF NOT EXISTS ishop
WITH replication = {
  'class' : 'SimpleStrategy',
  'replication_factor' : 1
};
```
### Create table items
```shell
USE ishop;

CREATE TABLE ishop.items(
   item_id int,
   category text,
   model text,
   producer text,
   price varint,
   screen_resolution text,
   properties map<text,text>,
   PRIMARY KEY (category, price, producer, item_id)
   )
WITH CLUSTERING ORDER BY (price DESC);
```

### Create an index on map field

```shell
CREATE INDEX IF NOT EXISTS properties_idx
ON ishop.items (ENTRIES(properties));

CREATE INDEX properties_key_idx ON items(KEYS(properties));
```

### Populate table items

```shell
INSERT INTO ishop.items (item_id, category, model, producer, price, screen_resolution, properties) VALUES (1, 'Phone', 'iPhone 6','Apple', 600, '720', {});
INSERT INTO ishop.items (item_id, category, model, producer, price, screen_resolution, properties) VALUES (2, 'Phone', 'iPhone 7','Apple', 700, '720', {});
INSERT INTO ishop.items (item_id, category, model, producer, price, screen_resolution, properties) VALUES (3, 'TV', 'smart tv 1212', 'Sumsung', 400, '4k', {'smart_tv': 'yes'});
INSERT INTO ishop.items (item_id, category, model, producer, price, screen_resolution, properties) VALUES (4, 'TV', 'smart tv 100',  'LG', 350, '4k',{'smart_tv': 'yes'});
INSERT INTO ishop.items (item_id, category, model, producer, price, screen_resolution, properties) VALUES (5, 'Laptop', 'thinkpad', 'Lenovo', 1250, '1080', {'processor': 'Intel Core i7', 'RAM': '16', 'SSD': '512 GB'});
INSERT INTO ishop.items (item_id, category, model, producer, price, screen_resolution, properties) VALUES (6, 'Laptop', 'latitude 5400', 'Dell', 1350, '1080',{'processor': 'Intel Core i7', 'RAM': '16', 'SSD': '1 TB', 'OS':'linux'});
INSERT INTO ishop.items (item_id, category, model, producer, price, screen_resolution, properties) VALUES (7, 'Smart watch', 'Marq Captain American Magic Edition','Garmin', 1100, '240', {'batary_life': '21 day'});
INSERT INTO ishop.items (item_id, category, model, producer, price, screen_resolution, properties) VALUES (8, 'Smart watch', 'Apple Watch Series 6 40mm Blue Aluminum','Apple', 500, '360', { 'batary_life': '2 days'});
INSERT INTO ishop.items (item_id, category, model, producer, price, screen_resolution, properties) VALUES (9, 'Smart watch', 'Vantage V', 'Polar', 420, '128', {'batary_life': '20 days'});
INSERT INTO ishop.items (item_id, category, model, producer, price, screen_resolution, properties) VALUES (10, 'Earbuds', 'AirPods Pro','Apple', 250, 'N/A', {'batary_life': '5h' });
```

### Напишіть запит, який показує структуру створеної таблиці (команда DESCRIBE)
```shell
DESCRIBE TABLE ishop.items;
```
![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Cassandra/screenshots/1.png?raw=true)

### Напишіть запит, який виводить усі товари в певній категорії відсортовані за ціною

```shell
select * from items where category = 'Smart watch';
```
![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Cassandra/screenshots/2.png?raw=true)

### Напишіть запити, які вибирають товари за різними критеріями в межах певної категорії:
### - назва, 
### - ціна (в проміжку), 
### - ціна та виробник 

```shell
select * from items where category = 'Smart watch';
select * from items where category = 'Phone' and price > 600 and price < 1000;
select * from items where category = 'Phone' and price = 600 and producer = 'Apple';
```

![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Cassandra/screenshots/3.png?raw=true)

### Напишіть запити, які вибирають товари за:
### - наявність певних характеристик
### - певна характеристика та її значення

```shell
SELECT * FROM items WHERE properties CONTAINS KEY 'OS';
SELECT JSON * FROM items WHERE properties['processor']='Intel Core i7';
```

![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Cassandra/screenshots/4.png?raw=true)


### Оновити опис товару:
### змінить існуючі значення певної характеристики 
### додайте нові властивості (характеристики) товару
### видалить характеристику товару
