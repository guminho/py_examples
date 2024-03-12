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
python main.py
```

```bash
cd h2
bash gencert.sh
hypercorn server:app -c hyper.toml

# client
curl https://localhost:8000/ -i -k
```

```bash
cd sse
uvicorn server:app --log-config=log-config.yml

# client
curl localhost:8000?name=world -i -X POST
python client.py
```

```bash
cd sched
python blocking.py
python thread.py
```