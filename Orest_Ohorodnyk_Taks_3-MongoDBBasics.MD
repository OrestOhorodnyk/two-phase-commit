### Run mongo

 `docker run --name mongo -p 27017:27017 -d --rm mongo`

### 1) Створіть декілька товарів з різним набором властивостей 

```shell
db.items.insertMany([
  {category: "Phone", model: "iPhone 6",producer: "Apple",price: 600, screen_resolution: 720 },
  {category: "Phone", model: "iPhone 7",producer: "Apple",price: 700, screen_resolution: 720 },
  {category: "TV", model: "smart tv 1212",producer: "Sumsung",price: 400, screen_resolution: 1080, smart_tv: "yes" },
  {category: "TV", model: "smart tv 100",producer : "LG","price" : 350, "sscreen resolution": 4000, smart_tv: "No" },
  {category: "Laptop", model: "thinkpad",producer : "Lenovo","price" : 1250, screen_resolution: 1080, pecs: {"processor": "Intel Core i7", "RAM": 16, "SSD": "512 GB"} },
  {category: "Laptop", model: "latitude 5400",producer : "Dell","price" : 1350, screen_resolution: 1080, pecs: {"processor": "Intel Core i7", "RAM": 16, "SSD": "1 TB", "OS":"linux"} },
  {category: "Smart watch", model: "Marq Captain American Magic Edition",producer: "Garmin",price: 1800, screen_resolution: 240, batary_life: "21 day" },
  {category: "Smart watch", model: "Apple Watch Series 6 40mm Blue Aluminum",producer: "Apple",price: 500, screen_resolution: 240, batary_life: "2 days" },
])

```

### 2) Напишіть запит, який виводіть усі товари (відображення у JSON)

```shell
db.getCollection("items").find({}).pretty()
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

### 3) Підрахуйте скільки товарів у певної категорії

```shell
#Grop by category and count
db.items.aggregate([
    {"$group" : {_id:"$category", count:{$sum:1}}}
]);

#Count all items in Phone category
db.items.find( { category: "Phone"}).count()

```

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
db.items.find( { $and: [ { price: { $gt: 600 } }, { price: { $lt: 700 }}, { category: "Phone"} ] } )
```
#### b) модель чи одна чи інша - конструкція $or,
```shell
db.items.find( { $or: [ {model: "iPhone 6"}, {model: "iPhone 7"} ] } )
```
#### c) виробники з переліку - конструкція $in
```shell
db.items.find( { producer: { $in: [ "Apple", "LG" ] } } )
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
// find items with missing is_original property
db.items.find( {is_original: { $exists: false } });
```

### 9) Для знайдених товарів збільшіть їх вартість на певну суму
```shell
db.items.update(
   {is_original: { $exists: false }},
   { $inc: { price: 1 } },
   { 
       upsert: false,
       multi: true
   } 
)

```

## Товари ви додаєте в замовлення - orders, яке містити вартість, ім'я замовника, і адресу доставки.
## Товари (items) в замовленні (order) повинні бути представлені у вигляді references, а замовник (customer) у вигляді embed

### Створіть кілька замовлень з різними наборами товарів, але так щоб один з товарів був у декількох замовленнях

```shell
var iphone_6 = db.products.find( { $and: [ { model: "iPhone 7"} , { producer: "Apple"} ] } ).next();
var watch = db.products.find( { $and: [ { model: "Apple Watch Series 6 40mm Blue Aluminum"} , { producer: "Apple"} ] } ).next();

iphone_6._id
watch._id


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


)

```