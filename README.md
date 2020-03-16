# Car Rental

## Prerequisites

1. Install and use python 3.6.9

    For this step it we prefer to use pyenv as our python version management. see [here](https://github.com/pyenv/pyenv#installation) on how to install pyenv.

    Install python 3.6.9 and set is as your current python version

    ```shell
    pyenv install 3.6.9
    pyenv local 3.6.9
    ```

2. Install [Poetry](https://poetry.eustace.io/docs/#installation)


## Installing

   
1. Using [poetry](https://poetry.eustace.io/docs/#installation)

    ```shell script
    poetry install
    poetry shell
    ```

    If you use VS Code, add this setting to your folder setting
    
    ```shell script
    poetry env info -p
    ```
    
2. .env
    
    Copy car_rental.env.example
    
    ```shell script
    cp env.example .env
    source car_rental.env.example 
    ```
    
3. Docker DB & Redis
    
    Build docker db and redis
    
    ```shell script
    docker-compose up -d 
    ```
    

## Tests

### Running Test

```shell
make test
```

### Coding Style

We follow flake8 standard. Use black as code formater and isort as import sorter.

### Running Dev Server

```shell
flask run
```

### Running Shell

```shell
flask shell
```

### Running Car CLI

```shell
flask car
```

### Running Rent CLI

```shell
flask rent
```

