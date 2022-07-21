# Part 3

## Required steps before we can begin

Before beginning this portion, you _must_ be logged into the `dev` Kubernetes cluster. This allows your `kubectl` tool to interact with the cluster.

## Translating systems from docker-compose to Kubernetes

In [Part 2](part002.md) of this course, we moved "up" from basic container usage to container orchestration with docker-compose. In this part, we'll move "up" again into more advanced container orchestration using Kubernetes.

Let's look at the `docker-compose.yaml` file from [Part 2](part002.md) below. Our goal is to identify which Kubernetes resources we will need to support the same system.

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
    ports:
      - "38080:8080"
    entrypoint: ["/bin/sh", "/client/serve_api.sh"]
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

## Breaking this down into required Kubernetes resources

We'll need some Kubernetes resources to represent the docker-compose resources. Here's a brief summary of how those are translated:

- `services` translate to `deployments`
    - 1 deployment for `api`
    - 1 deployment for `database`
- `ports` translate to `services`
    - 1 service for 8080/tcp to deployment `api`
    - 1 service for 3306/tcp to deployment `database`

### Kubernetes deployment YAML

Let's look at what the Kubernetes _deployment_ YAML looks like for this system.

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: lab-hgrubbs
  labels:
    app: api
spec:
  replicas: 1
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api
          image: q5idcontainers.azurecr.io/q5id/labs/chracter-api:001
          env:
            - name: DB_PASSWORD
              value: thuctive
          ports:
            - containerPort: 8080
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: database
  namespace: lab-hgrubbs
  labels:
    app: database
spec:
  replicas: 1
  selector:
    matchLabels:
      app: database
  template:
    metadata:
      labels:
        app: database
    spec:
      containers:
        - name: database
          image: mariadb:10.8
          env:
            - name: MARIADB_ROOT_PASSWORD
              value: thuctive
          ports:
            - containerPort: 3306

```

### Kubernetes _service_ YAML

Let's look at what the Kubernetes _service_ YAML looks like for this system.

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: api
  namespace: lab-hgrubbs
spec:
  selector:
    app: api
  ports:
  - port: 8080
    protocol: TCP
    targetPort: 8080
  type: NodePort
---
apiVersion: v1
kind: Service
metadata:
  name: database
  namespace: lab-hgrubbs
spec:
  selector:
    app: database
  ports:
  - port: 3306
    protocol: TCP
    targetPort: 3306
  type: NodePort

```

## Containing the _system_

Systems in Kubernetes are usually(_but not always!_) contained with a _namespace_ resource. A namespace is an organizational unit. Resources within a namespace can reach each other by their short name, eg `database` or `api`. 

### Caution!
When you delete a namespace, _all resources_ within it are deleted.

## Creating resources 

### Namespace creation

Before we can begin to create the resources defined in YAML above, we'll need to create the namespace. Above, all the YAML resources indicate they are meant to exist in namespace `lab-hgrubbs`.

Let's create our namespace with the below command, if it does not already exist.

```bash
kubectl create namespace lab-hgrubbs
```

You can see namespaces that exist with the following command.

```bash
$ kubectl get namespace
NAME                STATUS   AGE
cert-manager        Active   28d
default             Active   28d
devtest             Active   27d
gatekeeper-system   Active   27d
ingress-nginx       Active   28d
kube-node-lease     Active   28d
kube-public         Active   28d
kube-system         Active   28d
lab-hgrubbs         Active   6s    <----- Our new namespace
qa1                 Active   13d
qa2                 Active   13d
qa3                 Active   13d
```

### Deployment creation

Ensure your current directory is changed to `containercourse/resources/part003/kubernetes_files`. This path contains the Kubernetes YAML referenced above.

To deploy your deployment YAML, see the following the command and output:

```bash
$ kubectl create -f deployment/deployment.yaml 
deployment.apps/api created
deployment.apps/database created
```

You can see your deployments with the following command. Note the `-n <namespace>` argument used.

```bash
$ kubectl get deployment -n lab-hgrubbs
NAME       READY   UP-TO-DATE   AVAILABLE   AGE
api        1/1     1            1           35s
database   1/1     1            1           35s
```

### Service creation

To deploy your service YAML, see the following command and output:

```bash
$ kubectl create -f service/service.yaml 
service/api created
service/database created
```

You can see your services with the following command. Again, note the `-n <namespace>` argument used.

```bash
$ kubectl get service -n lab-hgrubbs
NAME       TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
api        NodePort   172.16.5.203   <none>        8080:32058/TCP   35s
database   NodePort   172.16.0.245   <none>        3306:32691/TCP   34s
```

## The state of things so far

At this point, we've created 2 deployments, both `database` and `api`. We've also created 2 services, one for the `database` port 3306/tcp, and another for the `api` port 8080/tcp.

Unfortunately, while it may run fine - we can't interact with them from outside the cluster(ie from the internet). For this to be usable by internet clients, we'll need to expose the `api` port 8080/tcp to the outside world.

## Bridging your _service_ resource to internet HTTP clients

To connect our service to the internet, we will use a new Kubernetes resource called an _ingress_. An _ingress_ resource accepts internet traffic destined for 1 or more hostnames, and routes that traffic to backend service[s] within a namespace.

### Ingress deployment YAML

Let's look at what the Kubernetes _ingress_ YAML looks like for this the `api` port 8080/tcp service.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api
  namespace: lab-hgrubbs
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
spec:
  ingressClassName: nginx

  defaultBackend:
    service:
      name: api
      port:
        number: 8080

  rules:
    - host: "character-api.dev-westus2.aks.q5id.com"
      http:
        paths:
          - pathType: Prefix
            path: "/"
            backend:
              service:
                name: api
                port:
                  number: 8080
```

### Ingress creation

To deploy your ingress YAML, see the following command and output:

```bash
$ kubectl create -f ingress/ingress.yaml 
ingress.networking.k8s.io/api created
```

You can see your ingress with the following command. Again, note the `-n <namespace>` argument used.

```bash
$ kubectl get ingress -n lab-hgrubbs
NAME   CLASS   HOSTS                                    ADDRESS   PORTS   AGE
api    nginx   character-api.dev-westus2.aks.q5id.com             80      22s
```

### Caution!

This ingress is not ready to use yet! Notice there is no value under `ADDRESS`. Ingress resources are not instant, they can take between 30 and 600 seconds to create - dependent on the type of ingress used. Our ingresses are of type `nginx`, and usually take 1 minute or less to become active.

If we wait a few moments and run the command again, we should see it have an address and ready to serve traffic.

```bash
$ kubectl get ingress -n lab-hgrubbs
NAME   CLASS   HOSTS                                    ADDRESS         PORTS   AGE
api    nginx   character-api.dev-westus2.aks.q5id.com   20.80.138.125   80      2m13s
```
Notice the `ADDRESS` field is now populated. The ingress is ready for use.

## Testing our service

Use curl (or your web browser) to access the `HOSTS` address listed: `character-api.dev-westus2.aks.q5id.com`

```bash
$ curl 'http://character-api.dev-westus2.aks.q5id.com'
{
  "hello": "mars"
}
```

### Testing the other endpoints

Here are the endpoints for the `characters` application - they are unchanged since [Part 2](part002.md).

- `/` : Returns JSON `{"Hello": "mars"}`
- `/names` : Returns JSON array of the names of characters in the database
- `/absurd` Returns JSON array with the most absurd character in the database

If you remember, we had to populate our database before `/names` or `/absurd` will work. This is still true.

## Populating our database

In _most_ scenarios, databases will be already populated by another mechanism. We will populate ours as an exercise in interacting with running containers. The steps will be similar, but not the same, as the steps we used when orchestrating this system via docker-compose.

### Gain a shell on the `database` container

First, we'll need to find out the name of the container currently holding the `database` container from the `database` deployment.

```bash
$ kubectl get pod -n lab-hgrubbs
NAME                       READY   STATUS    RESTARTS   AGE
api-5df599ff46-6sjct       1/1     Running   0          14m
database-8cb8d9f75-8f2j8   1/1     Running   0          14m
```

There are 2 containers running in our namespace. One for each of the deployments(`api` and `database`). We're interested in `database-8cb8d9f75-8f2j8`. Gain a shell on that container with the following command.

```bash
$ kubectl exec -i -t -n lab-hgrubbs database-8cb8d9f75-8f2j8 -- /bin/bash
root@database-8cb8d9f75-8f2j8:/#
```

Now we need to start the database CLI client to run `characters.sql`. Use the following command.

```
root@database-8cb8d9f75-8f2j8:/# mysql -u root -pthuctive
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 4
Server version: 10.8.3-MariaDB-1:10.8.3+maria~jammy mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> 
```

Now, copy the contents of `containercourse/resources/part003/character_api/characters.sql` to your clipboard. Paste it in the `mysql` CLI and press ENTER.

```
MariaDB [(none)]> DROP DATABASE IF EXISTS characters;
Query OK, 0 rows affected, 1 warning (0.000 sec)

MariaDB [(none)]> CREATE DATABASE characters;
Query OK, 1 row affected (0.000 sec)

MariaDB [(none)]> USE characters;
Database changed
MariaDB [characters]> CREATE TABLE users(id int primary key auto_increment not null, firstname text, lastname text);
Query OK, 0 rows affected (0.031 sec)

MariaDB [characters]> 
MariaDB [characters]> INSERT INTO users(firstname, lastname) VALUES("Zaphod", "Beeblebrox");
Query OK, 1 row affected (0.003 sec)

MariaDB [characters]> INSERT INTO users(firstname, lastname) VALUES("Harry", "Tuttle");
Query OK, 1 row affected (0.002 sec)

MariaDB [characters]> INSERT INTO users(firstname, lastname) VALUES("Samwell", "Tarly");
Query OK, 1 row affected (0.003 sec)

MariaDB [characters]> 
```

Now, type `exit` and press ENTER to leave the `mysql` CLI. Then, type `exit` and press ENTER to leave the container shell.

## Testing the other endpoints....for real this time

Using your web browser or `curl`, let's send requests to the other endpoints.

### Endpoint `/names`

```bash
$ curl 'http://character-api.dev-westus2.aks.q5id.com/names'
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

### Endpoint `/absurd`

```bash
$ curl 'http://character-api.dev-westus2.aks.q5id.com/absurd'
[
  {
    "firstname": "Zaphod", 
    "lastname": "Beeblebrox"
  }
]
```

## A brief introduction to accessing logs from your containers

If you were curious about what was happening on the backend, that's not immediately obvious with Kubernetes, unlike with docker-compose. The output from the containers is there, but we'll need to use a command to retrieve it.

### First, determine the container name you want logs from

Use the command below(again) to list the container names from your deployments. You can copy them to the clipboard and use them during the command to fetch logs.

```bash
$ kubectl get pod -n lab-hgrubbs
NAME                       READY   STATUS    RESTARTS   AGE
api-5df599ff46-6sjct       1/1     Running   0          27m
database-8cb8d9f75-8f2j8   1/1     Running   0          27m
```

### Accessing logs on the `api` container

```bash
$ kubectl logs -n lab-hgrubbs api-5df599ff46-6sjct
 * Serving Flask app 'api.py' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:8080
 * Running on http://10.244.9.134:8080 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 133-321-951
10.244.0.9 - - [21/Jul/2022 16:21:44] "GET / HTTP/1.1" 200 -
10.244.0.9 - - [21/Jul/2022 16:33:38] "GET /names HTTP/1.1" 200 -
10.244.0.9 - - [21/Jul/2022 16:34:20] "GET /absurd HTTP/1.1" 200 -
```

### Accessing logs on the `database` container

```bash
$ kubectl logs -n lab-hgrubbs database-8cb8d9f75-8f2j8
2022-07-21 16:10:18+00:00 [Note] [Entrypoint]: Entrypoint script for MariaDB Server 1:10.8.3+maria~jammy started.
2022-07-21 16:10:18+00:00 [Note] [Entrypoint]: Switching to dedicated user 'mysql'
2022-07-21 16:10:18+00:00 [Note] [Entrypoint]: Entrypoint script for MariaDB Server 1:10.8.3+maria~jammy started.
2022-07-21 16:10:19+00:00 [Note] [Entrypoint]: Initializing database files
...
... [tons of normal output]
...
```

### Fetching <N> number of logs

You can restrict how many lines are fetched with the `--tail=<N>` argument. See the below example to fetch only 1 line(the most recent) from the logs.

```bash
$ kubectl logs -n lab-hgrubbs api-5df599ff46-6sjct --tail=1
10.244.0.9 - - [21/Jul/2022 16:34:20] "GET /absurd HTTP/1.1" 200 -
```