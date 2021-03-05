### Run mongo

 `docker run --name mongo -p 27017:27017 -d --rm mongo`

### 1) Створіть декілька товарів з різним набором властивостей 

```shell
#db.items.drop();
db.items.insertMany([
  {category: "Phone", model: "iPhone 6",producer: "Apple",price: 600, screen_resolution: 720 },
  {category: "Phone", model: "iPhone 7",producer: "Apple",price: 700, screen_resolution: 720 },
  {category: "TV", model: "smart tv 1212",producer: "Sumsung",price: 400, screen_resolution: 1080, smart_tv: "yes" },
  {category: "TV", model: "smart tv 100",producer : "LG","price" : 350, "sscreen resolution": 4000, smart_tv: "No" },
  {category: "Laptop", model: "thinkpad",producer : "Lenovo","price" : 1250, screen_resolution: 1080, specs: {"processor": "Intel Core i7", "RAM": 16, "SSD": "512 GB"} },
  {category: "Laptop", model: "latitude 5400",producer : "Dell","price" : 1350, screen_resolution: 1080, specs: {"processor": "Intel Core i7", "RAM": 16, "SSD": "1 TB", "OS":"linux"} },
  {category: "Smart watch", model: "Marq Captain American Magic Edition",producer: "Garmin",price: 1800, screen_resolution: 240, batary_life: "21 day" },
  {category: "Smart watch", model: "Apple Watch Series 6 40mm Blue Aluminum",producer: "Apple",price: 500, screen_resolution: 240, batary_life: "2 days" },
  {category: "Smart watch", model: "Vantage V",producer: "Polar",price: 420, screen_resolution: 240, batary_life: "20 days" },
  {category: "Earbuds", model: "AirPods Pro",producer: "Apple",price: 250, screen_resolution: 240, batary_life: "5h" },
])
```

### 2) Напишіть запит, який виводіть усі товари (відображення у JSON)

```shell
db.getCollection("items").find({}).pretty();
```

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
database = client["online-shop"]
collection = database["items"]

query = {}

cursor = collection.find(query)
try:
    for doc in cursor:
        print(doc)
finally:
    client.close()

```
![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Mongo-practice/screenshots/1.png?raw=true)

### 3) Підрахуйте скільки товарів у певної категорії

```shell
#Grop by category and count
  db.items.aggregate([
      {"$group" : {_id:"$category", count:{$sum:1}}}
  ]);

#Count all items in Phone category
db.items.find( { category: "Phone"}).count()

```
![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Mongo-practice/screenshots/3.png?raw=true)

### 4) Підрахуйте скільки є різних категорій товарів

```shell
db.items.distinct('category').length;
```

### 5) Виведіть список всіх виробників товарів без повторів

```shell
db.items.distinct('producer');
```

### 6) Напишіть запити, які вибирають товари за різними критеріям і їх сукупності: 
#### a) категорія та ціна (в проміжку) - конструкція $and, 
```shell
db.items.find({ $and: [ { price: { $gt: 600 } }, { price: { $lt: 800 }}, { category: "Phone"} ] }).pretty();
```
#### b) модель чи одна чи інша - конструкція $or,
```shell
db.items.find( { $or: [ {model: "iPhone 6"}, {model: "iPhone 7"} ] } ).pretty();
```
#### c) виробники з переліку - конструкція $in
```shell
db.items.find( { producer: { $in: [ "Apple", "LG" ] } } ).pretty();
```

### 7) Оновить певні товари, змінивши існуючі значення і додайте нові властивості (характеристики) усім товарам за певним критерієм
```shell
db.items.update(
    {$and: [ { model: "iPhone 6"} , { producer: "Apple"} ] },
    {
         $set:  {price: 610} //update price
    },
    { upsert: true } 
);

db.items.update(
{producer: "Apple"},
{
     $set: {is_original: true} //new property 
},
{ upsert: false,
  multi: true
} 
);
```

### 8) Знайдіть товари у яких є (присутнє поле) певні властивості

```shell
db.items.find( {is_original: { $exists: true } }).pretty();
```

### 9) Для знайдених товарів збільшіть їх вартість на певну суму
```shell
db.items.update(
   {is_original: { $exists: true }},
   { $inc: { price: 1 } },
   { 
       upsert: false,
       multi: true
   } 
)

```

## Товари ви додаєте в замовлення - orders, яке містити вартість, ім'я замовника, і адресу доставки.
## Товари (items) в замовленні (order) повинні бути представлені у вигляді references, а замовник (customer) у вигляді embed

### 1) Створіть кілька замовлень з різними наборами товарів, але так щоб один з товарів був у декількох замовленнях

```shell
var iphone_6 = db.items.find( { $and: [ { model: "iPhone 6"} , { producer: "Apple"} ] } ).next();
var watch = db.items.find( { $and: [ { model: "Apple Watch Series 6 40mm Blue Aluminum"} , { producer: "Apple"} ] } ).next(); //common item
var tv_sumsung = db.items.find( { $and: [ { model: "smart tv 1212"} , { producer: "Sumsung"} ] } ).next();
var iphone_7 = db.items.find( { $and: [ { model: "iPhone 7"} , { producer: "Apple"} ] } ).next();

db.order.drop()

db.order.insertOne(
{    
  "order_number" : 201513,
  "date" : ISODate("2015-04-14"),
  "total_sum" : iphone_6.price + watch.price,
  "customer" : {
      "name" : "Andrii",
      "surname" : "Rodinov",
      "phones" : [ 9876543, 1234567],
      "address" : "PTI, Peremohy 37, Kyiv, UA"
  },
  "payment" : {
      "card_owner" : "Andrii Rodionov",
      "cardId" : 12345678
  },
  "order_items_id" : [
      {
          "$ref" : "items",
          "$id" : watch._id
      },
      {
          "$ref" : "items",
          "$id" : iphone_6._id
      }
  ]
}
);

db.order.insertOne(
{    
  "order_number" : 201514,
  "date" : ISODate("2015-04-15"),
  "total_sum" : watch.price + tv_sumsung.price,
  "customer" : {
      "name" : "John",
      "surname" : "Dou",
      "phones" : [ 1111111, 222222],
      "address" : "Bandery 37, Lviv, UA"
  },
  "payment" : {
      "card_owner" : "John Dou",
      "cardId" : 22345678
  },
  "order_items_id" : [
      {
          "$ref" : "items",
          "$id" : watch._id
      },
      {
          "$ref" : "items",
          "$id" : tv_sumsung._id
      }
  ]
}

);

db.order.insertOne(
{    
  "order_number" : 201515,
  "date" : ISODate("2015-04-16"),
  "total_sum" : iphone_7.price + watch.price,
  "customer" : {
      "name" : "James",
      "surname" : "Bond",
      "phones" : [ 3333333, 4444444],
      "address" : "10 Main str, London, UK"
  },
  "payment" : {
      "card_owner" : "James Bond",
      "cardId" : 22345678
  },
  "order_items_id" : [
      {
          "$ref" : "items",
          "$id" : watch._id
      },
      {
          "$ref" : "items",
          "$id" : iphone_7._id
      }
  ]
}

);

db.order.insertOne(
{    
  "order_number" : 201516,
  "date" : ISODate("2015-04-16"),
  "total_sum" : iphone_6.price + tv_sumsung.price,
  "customer" : {
      "name" : "James",
      "surname" : "Bond",
      "phones" : [ 3333333, 4444444],
      "address" : "10 Main str, London, UK"
  },
  "payment" : {
      "card_owner" : "James Bond",
      "cardId" : 22345678
  },
  "order_items_id" : [
      {
          "$ref" : "items",
          "$id" : tv_sumsung._id
      },
      {
          "$ref" : "items",
          "$id" : iphone_6._id
      }
  ]
}

);


```

### 2) Виведіть всі замовлення
```shell

db.getCollection("order").find({}).pretty()

```

### 3) Виведіть замовлення з вартістю більше певного значення
```shell
db.getCollection("order").find(
{ total_sum: { $gt: 1000 } }
).pretty()

```

### 4) Знайдіть замовлення зроблені одним замовником

```shell
db.getCollection("order").find(
{ "customer.name": "James" }
).pretty()
```

### 5) Знайдіть всі замовлення з певним товаром (товарами) (шукати можна по ObjectId)

```shell
var watch = db.items.find( { $and: [ { model: "Apple Watch Series 6 40mm Blue Aluminum"} , { producer: "Apple"} ] } ).next(); 
db.getCollection("order").find(
    {"order_items_id.$id": watch._id}
).pretty()
```

### 6) Додайте в усі замовлення з певним товаром ще один товар і збільште існуючу вартість замовлення на деяке значення Х

```shell
#// This query will add AirPods Pro for all who have bought iPhone 6
var apple_phone = db.items.find( { $and: [ { model: "iPhone 6" }, { producer: "Apple"} ] } ).next(); 
var air_pods = db.items.find( { $and: [ { model: "AirPods Pro"} , { producer: "Apple"} ] } ).next();

db.order.updateMany(
{ "order_items_id.$id": apple_phone._id },
{
     $push: { order_items_id:{"$ref" : "items",  "$id" : air_pods._id} },
     $inc: {total_sum: air_pods.price}
},
{
     upsert: true,
     multi: true,
}
)
```

### 7) Виведіть кількість товарів в певному замовленні

```shell
db.order.aggregate([
    { $match: {order_number: 201513}},
   {
      $project: {
          
         order_number: 1,
         numberOfitems: { 
             $cond: { if: { $isArray: "$order_items_id" }, then: { $size: "$order_items_id" }, else: "NA"} }
         
      }
   }

])
```

### 8) Виведіть тільки інформацію про кастомера і номери кредитної карт, для замовлень вартість яких перевищує певну суму

```shell
db.order.aggregate(
{ $match: { total_sum: { $gt: 1200 }  } },
  { $project : {
       "customer.name" : 1,
        "payment.cardId" : 1,
        total_sum : 1
  } }
).pretty();
```

### 9) Видаліть товар з замовлень, зроблених за певний період дат

```shell
db.order.update(
     {date: { $gt: ISODate("2015-04-15")}},
     {$set:{order_items_id:[]}},
     { multi: true }
 )

OR

db.order.update(
 {date: { $gt: ISODate("2015-04-15")}}, 
 { $pop: { order_items_id: 1 } }, 
 { multi: true } 
)
```

### 10) Перейменуйте у всіх замовлення ім'я (прізвище) замовника

```shell
db.order.update(
   {  },
   { $set: { "customer.surname" : "surname" } },
   {
     multi: true,
   }
)
```

### 11) (+2 бали)* Знайдіть замовлення зроблені одним замовником, і виведіть тільки інформацію про кастомера та товари
у замовлені підставивши замість ObjectId("***") назви товарів та їх вартість (аналог join-а між таблицями orders та items).

```shell
db.order.aggregate([
  {
    "$project": {
      "customer.name": 1,
      "customer.surname": 1,
      "order_number": 1,
      "date": 1,
      "order_items_id": 1
    }
  },
  {
    "$unwind": {
      "path": "$order_items_id",
      "preserveNullAndEmptyArrays": true
    }
  },
  {
    "$project": {
      "customer.name": 1,
      "customer.surname": 1,
      "order_number": 1,
      "date": 1,
      "order_items_id": {
        $arrayElemAt: [
          {
            $objectToArray: "$order_items_id"
          },
          1
        ]
      },
      
    }
  },
  {
    "$project": {
      "customer_name": "$customer.name",
      "customer_surname": "$customer.surname",
      "order_number": 1,
      "date": 1,
      "item_id": "$order_items_id.v",
      
    }
  },
  {
    "$lookup": {
      "from": "items",
      "localField": "item_id",
      "foreignField": "_id",
      "as": "order_items"
    }
  },
  {
    "$unwind": "$order_items"
  },
  {
    "$project": {
      "customer_name": 1,
      "customer_surname": 1,
      "order_number": 1,
      "date": 1,
      "producer": "$order_items.producer",
      "model": "$order_items.model",
      "prie": "$order_items.price"
    }
  },
  
]).pretty();
```


### Створіть Сapped collection яка б містила 5 останніх відгуків на наш інтернет-магазин. Структуру запису визначіть самостійно.
### 1) Перевірте що при досягненні обмеження старі відгуки будуть затиратись

```shell
db.createCollection("feedback", { capped : true, size : 4096, max : 5 } );
db.feedback.insertOne({"comment": "comment 1"});
db.feedback.insertOne({"comment": "comment 2"});
db.feedback.insertOne({"comment": "comment 3"});
db.feedback.insertOne({"comment": "comment 4"});
db.feedback.insertOne({"comment": "comment 5"});


db.getCollection("feedback").find({}).pretty();;

db.feedback.insertOne({"comment": "comment 6"});

db.getCollection("feedback").find({}).pretty();
```
