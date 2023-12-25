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