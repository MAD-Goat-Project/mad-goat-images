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
docker build -t nginix:1.25.1 .
docker tag nginix:1.25.1 ghcr.io/mad-goat-project/nginix:1.25.1
docker push ghcr.io/mad-goat-project/nginix:1.25.1
```

### Install Python project dependencies

```bash
pip install -r requirements.txt
python app.py
```
