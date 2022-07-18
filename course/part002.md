# Part 2
## Combining container resources into systems with docker-compose

Complex systems can be built on top of containers, assuming some orchestration of those containers is present. One popular tool for orchestrating contains into robust sytems is docker-compose. This tool is particularly suited to local workstation development VS production deployment.  Docker-compose orchestrates multiple containers to present a developer with a "stack" that represents their eventual production environment.

For educational purposes, we'll build a contrived system involving both a client and database container. Similar to how `Dockerfiles` define how containers are built, a `docker-compose.yaml` file defines how multiple containers run and interact.

## Starting template for docker-compose.yaml

```
version: "3.9"
services:
  client:
    networks:
      - backplane
    build:
      context: .
      dockerfile: client/Dockerfile
    volumes:
      - ./client:/client
    entrypoint: ["/client/run_forever.sh"]
  database:
    networks:
      - backplane
    image: mariadb:10.8
    environment:
      MARIADB_ROOT_PASSWORD: root
    ports:
      - "33306:3306"

networks:
  backplane:
    name: backplane
```

## Explanation of docker-compose.yaml

#TODO