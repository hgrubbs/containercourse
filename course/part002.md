# Part 2
## Combining container resources into systems with docker-compose

Complex systems can be built on top of containers, assuming some orchestration of those containers is present. One popular tool for orchestrating containers into robust systems is docker-compose. This tool is particularly suited to local workstation development VS production deployment.  Docker-compose orchestrates multiple containers to present a developer with a "stack" that represents their eventual production environment.

For educational purposes, we'll explain and run a contrived system involving both a client and database container. Similar to how `Dockerfiles` define how containers are built, a `docker-compose.yaml` file defines how multiple containers run and interact.

## Our docker-compose.yaml

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

## Annotated version of docker-compose.yaml

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

To start a docker-compose system, run the command `docker-compose up` in the directory where `docker-compose.yaml` is located. Change your directory to `containercourse/resources/part002/client_database` - this is the directory containing `docker-compose.yaml`.

Let's bring up the system. The first time, this will take a short while... the containers have to be downloaded, built, and finally started.

```bash
$ docker-compose up
Starting client_database_database_1 ... done
Starting client_database_api_1      ... done
Attaching to client_database_database_1, client_database_api_1
...
... [lots of start-up messages]
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

The database container has a volume mounted as `/client`, which maps to our `client` directory in the repo. This directory contains the SQL file we intend to load. While the stack is _up_, run this command in another terminal to access a shell within the database container.

```bash
docker-compose exec database /bin/bash
```

Once you are shelled into the container, run the following command to load `characters.sql`.

```bash
mysql -u root -proot mysql < /client/characters.sql
```

Now leave the shell, either by pressing Control+D or the `exit` command.

## Interacting with our API

With our database populated, let's test out the API endpoints. You can use any HTTP client you like, but this course will show examples from the `curl` client.

### Testing the `/` endpoint

```bash
$ curl 'http://localhost:38080/'
{
  "hello": "mars"
}
```

### Testing the `/names` endpoint

```bash
$ curl 'http://localhost:38080/names'
[
  {
    "firstname": "Zaphod",
    "lastname": "Beeblebrox"
  },
  {
    "firstname": "Harry",
    "lastname": "Tuttle"
  },
  {
    "firstname": "Samwell",
    "lastname": "Tarly"
  }
]
```

### Testing the `/absurd` endpoint

```bash
$ curl 'http://localhost:38080/absurd'
[
  {
    "firstname": "Zaphod",
    "lastname": "Beeblebrox"
  }
]
```

## Changing API code live

In our `docker-compose.yaml` file, we defined each container with a `/client` volume. This volume contains [among other things] our source code. This concept of mounting a volume between our host and container allows us to modify our code and see the output - without restarting our stack.

Open the `client/api.py` program, and change line `18` to see this concept in action.

```bash
    return {"hello": "mars"}  # CHANGE "mars" to "world"
```

Once you save your changes, you'll see a line of output from docker-compose, specifically from the `api` container.

```bash
api_1       |  * Detected change in '/client/api.py', reloading
```

This concept of live reloading is not unique to our program or the language it is written in. Many frameworks and languages include these feature, and concepts like volume mounts between hosts and containers allow you to easily take advantage of this. Sending a request to the `/` endpoint now returns a new message to reflect our edit.

```bash
$ curl 'http://localhost:38080/'
{
  "hello": "world"
}
```

## Don't forget to clean up!

Since we've modified code in the above exercise, let's reset it back to the state it was in before. Run the below command in your terminal to discard your changes and reset the file's state to match the repo.

```bash
git reset --hard
```

## Container reachability within docker-compose

When looking at the source code for `api.py`, you might have noticed we address the database container by the hostname `database`. In most scenarios, `database` is not a valid hostname. Within docker-compose, every container can reach every other container by it's name. This means that if you wanted to communicate from the `database` container with the `api` container, you could do it with the short `api` hostname. This concept carries over into other orchestration systems, specifically Kubernetes concept of services within a namespace.

To demonstrate this concept, let's access a shell in the `database` container, and attempt to reach the `api` container by name. Let's start by gaining a shell on the `database` container, and installing the `ping` utility with the below commands.

First, open a shell into the database container:
```bash
docker-compose exec database /bin/bash
```

Now, install the `ping` utility:
```bash
apt update && apt install -y inetutils-ping
```

Finally, attempt to ping the `api` container by name.

```bash
root@dec55cd00845:/# ping api
PING api (172.28.0.2): 56 data bytes
64 bytes from 172.28.0.2: icmp_seq=0 ttl=64 time=0.373 ms
64 bytes from 172.28.0.2: icmp_seq=1 ttl=64 time=0.177 ms
```

## Applying these concepts with your own scenarios

This example stack was minimal; a database and HTTP API container. Hopefully your understanding of `docker-compose.yaml` helps you feel comfortable modifying the example from this course, or crafting entirely new stacks. Some containers you could commonly see added to the API and Database stack are:

- Redis, as a caching layer
- gRPC daemon, an alternative to HTTP
- RabbitMQ, to introduce a message bus into your stack
- Prometheus, for persisting telemetry and metrics from your stack
- Grafana, for graphing and interacting with telemetry and metrics
- nginx, for terminating SSL or implementing path-based routing rules

## From docker-compose to production

If you are familiar with Kubernetes, you might have noticed some parallels between `docker-compose.yaml` and Kubernetes YAML. Any system defined with docker-compose can be cleanly translated to Kubernetes(or other orchestration tools, like Swarm). As you work with DevOps staff in the future, they will understand and be competent at translating your docker-compose systems to Kubernetes resources. This creates a scenario of your development environment closely mapping to the production environment, which is ideal for everyone involved.
