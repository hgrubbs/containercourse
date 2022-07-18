# Docker

Welcome to this course! The goal is to get you up and running with Docker containers to enable development to be more repeatable and 
reliable, to scale more easily, and deploy seamlessly.

## What is it?

Docker is a technology ecosystem that standardized a unit for app development, shipment, and deployment.

It can look a little different from different perspectives, but the staandard approach helps it work seamless across them.

For developers it lets them define the run-time (and often build-time!)
environment with all their dependenencies, common configuration, and run time environment setup as code, making a robust repeatable processes,
and prventing issues arising from variations across development and deployment environments.

For QA it can be a way to specify exactly what versions of components were tested, and create and manage test environments more easily.

For operations, containers offer a consistent "unit of deployment" that let's each application be 
treated in a similar way, and allowing robust and scalable reliable deployments, as well as some useful tools for addressing issues.

Docker provides a common abstraction, in a standard reliable 'container' that defines your application. This includes a shared, secure, repeatable definition 
of how to build your container (in the Dockerfile), the code and immediate dependnecies that your application needs to run, and some 
well defined shared touchpoints like environment-variable based configuration, and well defined network interfaces. Docker can publish versioned 
images of your applications for rapid and high integrity re-use and deployment.

## Why?

Dependencies cause a lot of problems. "DLL Hell", issues with non-specific package versions, required installs on your computer. A lot of solutions to
these issues have been built over time, including many of the technologies that underpin containers.

It takes a bit of effort, but a Docker real captures, in an high integrity, stanadrd, re-runable way how to set up your application. It's esentially same thing as the
"steps to set up and run this project" that you find in your readme.md files, with some pre-req installs, configuration notes, and things like what ports it runs on.
The mian difference is that it is in a command executable form, and clever layering and hashing makes it easy to build relaibly and quickly.

The point is standardization so that we can treat applications in the same way, and have shared expectations. This is why the "container" metaphor is used.
Shipping containers standardize how goods are packged and manged, increasing throughput and scaling our global shipping systems. The ships are set to cary them, the 
cranes are ready to load and unload them. The trains and trucks can hault them to the destitation. And the end user just has to open the doors and all the stuff is ready
to load, unload and use.

Likewise, when you standardize your application in a container, all the things it needs to run are there. Instructions for how to build it are there. The CI pipeline builds them,
and we can run them anywhere, from local machines for an all-services-local environment, which makes development and QA easier, to running in the cloud, or on a 
Kubernetes cluster. If an app has an issue, we can check that it has network connectivity, and restart it without worrying about what's inside.

Standardized containers help smooth out the processes across different languages, development flows, dependnecy complexities and other "unique" needs.

# What this course will cover

We'll be working hands on with containers to demonstrate how they are used and what you can do with them. We'll start withe the docker basics, how to create the
Dockerfile, and how that is used to build your container. From there we'll learn how to combine multiple containers with everything you need for a full environment using
Docker-compose.
After these local basics, we'll talk about how those whole systems "go live" onto Kubernetes ("K8s") clusters as running maintainable systems, and cover more details on how
the deployment process and troubleshooting.

# Outside links

* [Docker - What is a container?](https://www.docker.com/resources/what-container/)
* [What is Kubernetes?](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Scott Hanselman - Docker 101](https://www.youtube.com/watch?v=0oEsMwSxBsk)
* [Scott Hanselman - Kubernetes 101](https://www.youtube.com/watch?v=3RTvoI-A7UQ)

