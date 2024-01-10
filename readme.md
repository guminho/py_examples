# Python Examples

## setup
```bash
python3 -m venv venv
. venv/bin/activate
```

## usage
```bash
cd jwt2
bash genkey.sh

# run
python main.py
```

```bash
cd h2
bash gencert.sh

# server
hypercorn server:app -c hyper.toml

# client
curl https://localhost:8000/ -i -k
```

```bash
cd sse

# server
uvicorn server:app --log-config=log-config.yml

# client
curl localhost:8000?name=world -X POST
python client.py
```