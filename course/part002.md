# Part 2
## Combining container resources into systems with docker-compose

Complex systems can be built on top of containers, assuming some orchestration of those containers is present. One popular tool for orchestrating contains into robust systems is docker-compose. This tool is particularly suited to local workstation development VS production deployment.  Docker-compose orchestrates multiple containers to present a developer with a "stack" that represents their eventual production environment.

For educational purposes, we'll build a contrived system involving both a client and database container. Similar to how `Dockerfiles` define how containers are built, a `docker-compose.yaml` file defines how multiple containers run and interact.

## Starting template for docker-compose.yaml

```
version: "3.9"
services:
  api:
    networks:
      - backplane
    build:
      context: client/
    volumes:
      - ./client:/client
      - "38080:8080"
    entrypoint: ["/client/serve_api.sh"]
  database:
    networks:
      - backplane
    image: mariadb:10.8
    environment:
      MARIADB_ROOT_PASSWORD: root
    volumes:
      - ./client:/client
    ports:
      - "33306:3306"

networks:
  backplane:
    name: backplane
```

## Explanation of docker-compose.yaml

```
version: "3.9"                                  # docker-compose.yaml syntax version
services:                                       # `services` contains an array of containers to run 

  api:                                          # `api` is the name of a container
    networks:                                   # optional list of networks this container is attached to
      - backplane                               # `backplane` is the network mariadb is located on
    build:                                      # a `build` key indicates this container is built locally
      context: client/                          # `context` is the path `docker build` should operate in
    volumes:                                    # optional list of volumes and mount points
      - ./client:/client                        # binds the `client` directory to `/client` inside the container
    ports:                                      # optional list of port forwarding from host->container
      - "38080:8080"                            # forward port 38080 on local machine to 8080 within container
    entrypoint: ["/client/serve_api.sh"]        # specific script to "launch" the container

  database:                                     # `database` is the name of a container
    networks:
      - backplane                               # container is attached to `backplane` network
    image: mariadb:10.8                         # container to fetch from docker hub: mariadb, tag 10.8
    environment:                                # optional list of environment variables to set within container
      MARIADB_ROOT_PASSWORD: root               # defines an environment variable `MARIADB_ROOT_PASSWORD` with value `root`
    volumes:
      - ./client:/client                        # binds the `client` directory to `/client` inside the container
    ports:
      - "33306:3306"                            # forward port 33306 on local machine to 3306 within container

networks:                                       # optional list of networks to create
  backplane:                                    # defines a network
    name: backplane                             # names the network `backplane`
```

## Starting the stack

To start a docker-compose system, run the command `docker-compose up` in the directory where `docker-compose.yaml` is located.

Let's bring up the system. The first time, this will take a short while... the containers have to be built, downloaded, and finally run.

```bash
$ docker-compose up
Starting client_database_database_1 ... done
Starting client_database_api_1      ... done
Attaching to client_database_database_1, client_database_api_1
...
... [misc start-up messages]
...
api_1       |  * Serving Flask app 'api.py' (lazy loading)
api_1       |  * Environment: development
api_1       |  * Debug mode: on
api_1       |  * Running on all addresses (0.0.0.0)
api_1       |    WARNING: This is a development server. Do not use it in a production deployment.
api_1       |  * Running on http://127.0.0.1:8080
api_1       |  * Running on http://172.26.0.3:8080 (Press CTRL+C to quit)
api_1       |  * Restarting with stat
api_1       |  * Debugger is active!
api_1       |  * Debugger PIN: 930-644-492
```

## Interacting with our stack

The stack includes a toy HTTP API and backend database. Here is a list of endpoints the API supports.

- `/` : Returns JSON `{"Hello": "mars"}`
- `/names` : Returns JSON array of the names of characters in the database
- `/absurd` Returns JSON array with the most absurd character in the database

## Problems interacting with the stack

If you attempt to access these endpoints above, you'll encounter an error. This is because our database is not populated yet, it only contains the stock `mysql` database included with MariaDB. When the API attempts to access these resources, it will raise an exception - this is normal behavior.

## Fixing(populating) our database container

Within `containercourse/resources/part002/client_database/client` there is a file named `characters.sql`. Running this SQL will create our database, table, and rows. There are two ways to execute this file against our database.

## Two methods to populate our database container

1. Connect to host port 33306 with an SQL client. This will connect to our database _container_ port of 3306.
2. Shell directly into the database container and use the included `mysql` CLI client.

For this course, we'll be using the second option.

## Shelling into our database container

While the stack is _up_, run this command in another terminal to access a shell within the database container.

```bash
docker-compose exec database /bin/bash
```

Once you are shelled into the container, run the following command to load `characters.sql`.

```bash
mysql -u root -proot mysql < /client/characters.sql
```

Now leave the shell, either by pressing Control+D or the `exit` command.

## Interacting with our API

#TODO