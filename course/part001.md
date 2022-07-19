# Part 1

## Building and running containers with Docker
This portion of the course will explain the anatomy of a `Dockerfile`, and how that file is used to generate containers.

## Creating a simple container
To begin, create a new file named `Dockerfile` in an empty directory. Paste the contents below into `Dockerfile`.

```docker
FROM nginx:latest
```

## Building your container

Within the directory where you created `Dockerfile`, run the following command:

```bash
docker build -t mycontainer:001 .
```

Assuming all goes well, you should see the following similar output:

```
$ docker build -t mycontainer:001 .
Sending build context to Docker daemon  2.048kB
Step 1/1 : FROM nginx:latest
latest: Pulling from library/nginx
461246efe0a7: Pull complete 
a96aaf9a9ec3: Pull complete 
650d8b758441: Pull complete 
b138da793ac8: Pull complete 
bb1705539683: Pull complete 
b9ed43dcc388: Pull complete 
Digest: sha256:db345982a2f2a4257c6f699a499feb1d79451a1305e8022f16456ddc3ad6b94c
Status: Downloaded newer image for nginx:latest
 ---> 41b0e86104ba
Successfully built 41b0e86104ba
Successfully tagged mycontainer:001
```

## What happened?

We have effectively created a clone of the official `nginx:latest` container. A `Dockerfile` is a series of steps describing how to build a container, or how to _extend_ an existing container with your customizations.

Let's break down the effects of our `docker build` command, and the `FROM nginx:latest` contents of our `Dockerfile`.

### Explaining `docker build -t mycontainer:001 .`

This command tells Docker you want to build a new container, name it `mycontainer`, with a tag of `001`, and it should expect to find `Dockerfile` in the current directory. The last argument to the `docker build` command is a `.` character. That argument tells Docker where to look for `Dockerfile`. The `.` character is a UNIX concept that translates to the current directory you are in.

### Explaining our `Dockerfile` contents: `FROM nginx:latest`

The first line in a `Dockerfile` specifies which _existing_ container we intend to modify. Subsequent lines detail those modifications...but we don't specify any of those. Therefore we end up with a perfect clone of the `nginx:latest` container. By default, if a container does not exist on your local computer, Docker will attempt to look it up on [Docker Hub](https://hub.docker.com). You can view the `nginx` container we are using on Docker Hub with [this link](https://hub.docker.com/_/nginx).

## Running our container

Start your container with the following command:

```bash
docker run -p 38080:80 mycontainer:001
```

That command does more than start the container, it also tells Docker to forward traffic to your localhost on port 38080 _inside_ the container to port 80. This particular container happens to be a web server that listens on port 80. Forwarding port 38080 means that we can use our local computers web browser and visit [http://localhost:38080](http://localhost:38080), which would send our web request to the container.

If you have `curl` available, try it out to see the response from nginx:

```bash
curl 'http://localhost:38080/'
```

You should see output resembling:

```
$ curl 'http://localhost:38080/'
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

## Customizing our container

Let's modify our nginx container to send back different output. If you're familiar with nginx, you probably know that by default, it serves web traffic from `/usr/share/nginx/html`. We can add content to that directory and our container will serve it back to us. Let's extend our `Dockerfile` with the example below:

```docker
FROM nginx:latest
RUN echo "Hello World!" > /usr/share/nginx/html/index.html
```

## Rebuilding our container

Build the container again with the command we used earlier...but this time let's increment the tag to from `001` to `002`.

```bash
docker build -t mycontainer:002 .
```

Now run the new container we just built, which is tagged `mycontainer:002`.

```bash
docker run -p 38080:80 mycontainer:002
```

Now `curl` the container and see the response has changed to reflect us writing `index.html` to the correct path within the container.

```
$ curl 'http://localhost:38080/'
Hello World!
```

## Adding custom files to our container

In the previous example, we edited `index.html` by using the `echo` command during the build process. This works, but there is a more efficient and elegant way to add files to a container. Next, we'll add a more polished website template named _Dashmin_.

For this example, you'll need to clone this git repository, and navigate to `containercourse/resources/part001/dashmin`.

Open the `Dockerfile` in that directory.

```docker
FROM nginx:latest
ADD dashmin_files/ /usr/share/nginx/html/
```

Notice how the `echo` command has been swapped for `ADD`. This command recursively copies all the files within the `dashmin_files` directory to `/usr/share/nginx/html/` within the container.

Let's build the new container and see the output. Use the command below to build - notice how we've incremented our tag from `002` to `003`.

```bash
docker build -t mycontainer:003 .
```

Now run the container with the same command we've used previously, referencing the new tag.

```bash
docker run -p 38080:80 mycontainer:003
```

Once the container is running, visit [http://localhost:38080](http://localhost:38080) to see the website.

The _Dashmin_ website is a free and open source template. For more information about it visit it's official website at [https://htmlcodex.com/bootstrap-admin-template-free](https://htmlcodex.com/bootstrap-admin-template-free).

## More information on commands available within a `Dockerfile`

A complete listing of all syntax and documentation for the `Dockerfile` format is available on the official Docker website, at [https://docs.docker.com/engine/reference/builder/](https://docs.docker.com/engine/reference/builder/).
