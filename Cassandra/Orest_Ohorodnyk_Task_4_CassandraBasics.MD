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

```shell
UPDATE items SET properties['OS'] = 'Windows' WHERE item_id=6 and category='Laptop' and price = 1350 and producer = 'Dell';
UPDATE items SET properties = properties + {'battery_life': '21' } WHERE item_id=6 and category='Laptop' and price = 1350 and producer = 'Dell';
UPDATE items SET properties = properties - {'battery_life'} WHERE item_id=6 and category='Laptop' and price = 1350 and producer = 'Dell';
```

![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Cassandra/screenshots/5.png?raw=true)

### ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
### ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


### Створіть таблицю orders в якій міститься ім'я замовника і інформація про замовлення: 
### перелік id-товарів у замовленні, вартість замовлення, дата замовлення, .... Для кожного замовника повинна бути
### можливість швидко шукати його замовлення і виконувати по них запити.

### Create table

```shell
  CREATE TABLE ishop.orders(
   customer_name text,
   order_date timestamp,
   items_id list<int>,
   total_amount float,
   PRIMARY KEY ((customer_name),order_date))
 WITH CLUSTERING ORDER BY (order_date DESC);

CREATE INDEX items_id_idx ON ishop.orders(items_id);
```

### Insert data

```shell
 INSERT INTO ishop.orders (customer_name,order_date, items_id, total_amount ) VALUES (
  'Thomas', '2021-03-05 00:00:00+0000', [10,9], 670);
 INSERT INTO ishop.orders (customer_name,order_date, items_id, total_amount ) VALUES (
  'Thomas', '2021-03-01 00:00:00+0000', [3], 400);
 INSERT INTO ishop.orders (customer_name,order_date, items_id, total_amount ) VALUES (
  'Thomas', '2021-03-04 00:00:00+0000', [7],  1100);
 INSERT INTO ishop.orders (customer_name,order_date, items_id, total_amount ) VALUES (
  'Thomas', '2021-03-03 00:00:00+0000', [7, 3], 1500);


 INSERT INTO ishop.orders (customer_name,order_date, items_id, total_amount ) VALUES (
  'Mary', '2021-03-17 00:00:00+0000', [3], 400);
 INSERT INTO ishop.orders (customer_name,order_date, items_id, total_amount ) VALUES (
  'Mary', '2021-03-16 00:00:00+0000', [1,2], 1300);
 INSERT INTO ishop.orders (customer_name,order_date, items_id, total_amount ) VALUES (
  'Mary', '2021-03-16 12:00:00+0000', [3], 1100);
```

### Напишіть запит, який показує структуру створеної таблиці (команда DESCRIBE)

![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Cassandra/screenshots/6.png?raw=true)


### Для замовника виведіть всі його замовлення відсортовані за часом коли вони були зроблені
```shell
select * from ishop.orders where customer_name='Thomas';
```

![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Cassandra/screenshots/7.png?raw=true)

### Для замовника знайдіть замовлення з певним товаром

```shell
select * from ishop.orders where customer_name = 'Thomas' and items_id contains 3;
```

![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Cassandra/screenshots/8.png?raw=true)

### Для замовника знайдіть замовлення за певний період часу і їх кількість

```shell
select customer_name, count(*) from ishop.orders where customer_name = 'Thomas' and order_date > '2021-03-01 00:00:00.000000+0000' and order_date < '2021-03-05 00:00:00.000000+0000';
```

![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Cassandra/screenshots/9.png?raw=true)

### Для кожного замовників визначте середню вартість замовлення

```shell
select customer_name, avg(total_amount) from ishop.orders group by customer_name;
```

![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Cassandra/screenshots/10.png?raw=true)

### Для кожного замовників визначте суму на яку були зроблені усі його замовлення

```shell
select customer_name, sum(total_amount) from ishop.orders group by customer_name;
```
![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Cassandra/screenshots/11.png?raw=true)

### Для кожного замовників визначте замовлення з максимальною вартістю

```shell
select customer_name, order_date, items_id, max(total_amount) from ishop.orders group by customer_name;
```
![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Cassandra/screenshots/12.png?raw=true)

### Модифікуйте певне замовлення додавши / видаливши один або кілька товарів при цьому також змінюючи вартість замовлення

```shell
select * from ishop.orders where customer_name = 'Mary' and order_date = '2021-03-17 00:00:00.000000+0000';
UPDATE ishop.orders SET items_id = items_id - [3], total_amount = 799 where customer_name = 'Mary' and order_date = '2021-03-17 00:00:00.000000+0000';
```
![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Cassandra/screenshots/13.png?raw=true)

### Для кожного замовлення виведіть час коли його ціна були занесена в базу (SELECT WRITETIME)

```shell
select WRITETIME(total_amount), customer_name, order_date from ishop.orders;
```

![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Cassandra/screenshots/14.png?raw=true)

### Створіть замовлення з певним часом життя (TTL), після якого воно видалиться 

```shell
 INSERT INTO ishop.orders (customer_name,order_date, items_id, total_amount ) VALUES (
  'Mary', '2021-03-16 12:00:00+0000', [1,4,5,7], 4100) USING TTL 86400;
```

![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Cassandra/screenshots/15.png?raw=true)

### Поверніть замовлення у форматі JSON

```shell
select json * from ishop.orders;
```

![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Cassandra/screenshots/16.png?raw=true)

### Додайте замовлення у форматі JSON

```shell
INSERT INTO ishop.orders JSON '{"customer_name": "Mary", "order_date": "2021-03-01 13:01:00.000Z", "items_id": [2,4,9], "total_amount": 2799.0}';
```

![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Cassandra/screenshots/17.png?raw=true)