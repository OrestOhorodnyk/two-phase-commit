
### Env setup
```shell
docker run --name redis -d -p 6379:6379 redis
docker exec -it redis  redis-cli 
```

### Create virtualenv with python 3.9
```shell
virtualenv -p python3.9 venv
source venv/bin/activate
```

### Ruin script

```shell
python main.py
```

###Results will be printed to the console
![alt text](https://github.com/OrestOhorodnyk/two-phase-commit/blob/master/Redis/redis.png)