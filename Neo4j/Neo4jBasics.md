CREATE (john:Customer {name: 'John'}),
(joe:Customer {name: 'Joe'}),
(steve:Customer {name: 'Steve'}),
(sara:Customer {name: 'Sara'}),
(maria:Customer {name: 'Maria'})
RETURN john, joe, steve, sara, maria;



CREATE
(item1: Item {category: 'Phone', model: 'iPhone 6',producer: 'Apple',price: 600, screen_resolution: 720 }),
(item2: Item {category: 'Phone', model: 'iPhone 7',producer: 'Apple',price: 700, screen_resolution: 720 }),
(item3: Item {category: 'TV', model: 'smart tv 1212',producer: 'Sumsung',price: 400, screen_resolution: 1080, smart_tv: 'yes' }),
(item4: Item {category: 'TV', model: 'smart tv 100',producer : 'LG', price : 350, screen_resolution : 4000, smart_tv: 'No' }),
(item5: Item {category: 'Laptop', model: 'thinkpad',producer : 'Lenovo', price : 1250, screen_resolution: 1080 }),
(item6: Item {category: 'Laptop', model: 'latitude 5400',producer : 'Dell',price : 1350, screen_resolution: 1080 }),
(item7: Item {category: 'Smart watch', model: 'Marq Captain American Magic Edition',producer: 'Garmin',price: 1800, screen_resolution: 240, batary_life: '21 day' }),
(item8: Item {category: 'Smart watch', model: 'Apple Watch Series 6 40mm Blue Aluminum',producer: 'Apple',price: 500, screen_resolution: 240, batary_life: '2 days' })
RETURN item1, item2, item3, item4, item5, item6, item7, item8;


```shell
	MATCH (c:Customer), (i1:Item)
	WHERE c.name = "John" and i1.producer = "Apple" and i1.model = "Apple Watch Series 6 40mm Blue Aluminum"
	CREATE (o: Order {id:1, customer: c.name, ts: timestamp(), amount: i1.price})
	CREATE (c)-[v1:VIEWED]->(i1), (c)-[r:MADE]->(o), (i1)-[in1:INCLUDED]->(o)
	RETURN c,o, i1, in1;
```


	MATCH (c:Customer), (i1:Item), (i2:Item), (i3:Item) 
	WHERE c.name = "John" and i1.producer = "Apple" and i1.model = "iPhone 6" and i2.producer = "Sumsung" and i2.model = "smart tv 1212" and i3.producer = "Garmin" and i3.model = "Marq Captain American Magic Edition"
	CREATE (o: Order {id:1, customer: c.name, ts: timestamp(), amount: i1.price + i2.price + i3.price})
	CREATE (c)-[v1:VIEWED]->(i1), (c)-[v2:VIEWED]->(i2),(c)-[v3:VIEWED]->(i3), (c)-[r:MADE]->(o), (i1)-[in1:INCLUDED]->(o), (i2)-[in2:INCLUDED]->(o), (i3)-[in3:INCLUDED]->(o)
	RETURN c,o, i1,i2, in1, in2, in3;

	MATCH (c:Customer), (i1:Item), (i2:Item), (i3:Item)
	WHERE c.name = "Joe" and i1.producer = "Garmin" and i1.model = "Marq Captain American Magic Edition" and i2.producer = "Lenovo" and i2.model = "thinkpad" and i3.producer = "Dell" and i3.model = "latitude 5400"
	CREATE (o: Order {id:2, customer: c.name, ts: timestamp(), amount: i1.price + i2.price})
	CREATE (c)-[v1:VIEWED]->(i1), (c)-[v2:VIEWED]->(i2),(c)-[v3:VIEWED]->(i3), (c)-[r:MADE]->(o), (i1)-[in1:INCLUDED]->(o), (i2)-[in2:INCLUDED]->(o)
	RETURN c,o, i1,i2, i3, in1, in2;


	MATCH (c:Customer), (i1:Item), (i2:Item), (i3:Item)
	WHERE c.name = "Steve" and i1.producer = "Garmin" and i1.model = "Marq Captain American Magic Edition" and i2.producer = "Lenovo" and i2.model = "thinkpad" and i3.producer = "Dell" and i3.model = "latitude 5400"
	CREATE (c)-[v1:VIEWED]->(i1), (c)-[v2:VIEWED]->(i2),(c)-[v3:VIEWED]->(i3)
	RETURN c, i1,i2;



	MATCH (c:Customer)-[m:MADE]-(o:Order)-[r:INCLUDED]-(i:Item) RETURN c,m,o,r,i


MATCH (o:Oreder {id: 1})-[:INCLUDED]->(i:Item) return i
Match (o:Order {id: 1}) -[:INCLUDED]->(i:Item) return i
RETURN o

	MATCH (n)
DETACH DELETE n

call db.schema.visualization()

### Знайти Items які входять в конкретний Order

```shell
Match (o:Order {id: 1}) -[:INCLUDED]-(i:Item) return o,i
```

### Підрахувати вартість конкретного Order

```shell
Match (o:Order {id: 1}) -[:INCLUDED]-(i:Item) return  sum(i.price)
```

### Знайти всі Orders конкретного Customer

```shell
Match (c:Customer {name: "John"}) -[:MADE]-(o:Order) return c,o
```

### Знайти всі Items куплені конкретним Customer (через Order)

```shell
MATCH (c:Customer {name: "John"})-[m:MADE]-(o:Order)-[r:INCLUDED]-(i:Item) RETURN i
```

### Знайти кількість Items куплені конкретним Customer (через Order)

```shell
MATCH (c:Customer {name: "John"})-[m:MADE]-(o:Order)-[r:INCLUDED]-(i:Item) RETURN count(i)
```

### Знайти для Customer на яку суму він придбав товарів (через Order)

```shell
MATCH (c:Customer {name: "John"})-[m:MADE]-(o:Order)-[r:INCLUDED]-(i:Item) RETURN sum(i.price)
```

### Знайті скільки разів кожен товар був придбаний, відсортувати за цим значенням

```shell
MATCH (i:Item)-[r:INCLUDED]->(o:Order)
RETURN i.producer, i.model, count(r) as count
ORDER BY COUNT(r) DESC;
```

### Знайти всі Items переглянуті (view) конкретним Customer

```shell 
MATCH (c:Customer {name: "John"})-[r:VIEWED]-(i:Item) RETURN c, i
```

### Знайти інші Items що купувались разом з конкретним Item (тобто всі Items що входять до Order-s разом з даними Item)

```shell
MATCH (apple:Item {producer: "Apple", model:"iPhone 6"})-[:INCLUDED]->(:Order)<-[:INCLUDED]-(i:Item) return i.producer, i.model
```


### Знайти Customers які купили даний конкретний Item

```shell
MATCH (c:Customer)-[m:MADE]-(o:Order)-[r:INCLUDED]-(i:Item{producer:"Garmin", model: "Marq Captain American Magic Edition"}) RETURN c.name
```

### Знайти для певного Customer(а) товари, які він переглядав, але не купив

```shell
MATCH (c:Customer {name: "Joe"})-[r:VIEWED]-(i:Item)
WHERE NOT (i)-[:INCLUDED]-(:Order)
RETURN i
```