
### docker run command 
```
docker run --name postgresdb -p 5432:5432 -e POSTGRES_PASSWORD=pass -d --rm postgres --max_prepared_transactions=100
docker exec -it postgresdb bash
psql -U postgres
```


### SQL to create databases and schemas

~~~sql
CREATE DATABASE db1;
CREATE DATABASE db2;
CREATE DATABASE db3;



\c db1;
CREATE TABLE public.fly_booking (
	booking_id serial NOT NULL,
	client_name varchar NULL,
	fly_number varchar NULL,
	origin varchar NULL,
	destination varchar NULL,
	departure_date date NULL,
	CONSTRAINT fly_booking_pkey PRIMARY KEY (booking_id)
);



\c db2;
CREATE TABLE public.hotel_booking (
	booking_id serial NOT NULL,
	client_name varchar NULL,
	hotel_name varchar NULL,
	arrival_date date NULL,
	departure_date date NULL,
	CONSTRAINT hotel_booking_pkey PRIMARY KEY (booking_id)
);


\c db3;
CREATE TABLE public.account (
	account_id serial NOT NULL,
	client_name varchar NULL,
	amount numeric NOT NULL,
	CONSTRAINT account_amount_check CHECK ((amount > (0)::numeric)),
	CONSTRAINT account_pkey PRIMARY KEY (account_id)
);
~~~

### Swagger UI ``http://0.0.0.0:8000/docs``

### Add account via Swagger UI or curl

```shell
curl -X POST "http://localhost:8000/account" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"client_name\":\"John\",\"amount\":500.67}"
```


### Add booking via Swagger UI or curl

```shell
curl -X POST "http://localhost:8000/booking" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"client_name\":\"John\",\"hotel_name\":\"Hilton\",\"arrival_to_hotel_date\":\"2021-02-22\",\"departure_from_hotel_date\":\"2021-02-28\",\"fly_number\":\"UCU2021\",\"origin\":\"Lviv\",\"destination\":\"Rome\",\"departure_date\":\"2021-02-21\",\"price\":500}"
```
