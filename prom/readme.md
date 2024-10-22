# PYTHON PROMETHEUS EXAMPLES

## PREREQUISITES
```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```


## BACKEND SETUP
```bash
docker-compose up -d prom
```
visit [localhost:9090](http://localhost:9090) to view Prometheus WebUI


## CLIENT SIMPLE-PROM-PULL
```bash
python simple_prom.py
```
visit [localhost:9464](http://localhost:9464) to view the metrics


## CLIENT FASTAPI-PROM-PULL
```bash
uvicorn fast_prom:app --port=9464
```
visit [localhost:9464](http://localhost:9464/metrics) to view the metrics


## CLIENT FASTAPI-OTEL-PULL
```bash
export OTEL_SERVICE_NAME='fast_otel' 
export OTEL_TRACES_EXPORTER=''
OTEL_METRICS_EXPORTER='prometheus' \
opentelemetry-instrument uvicorn fast_otel:app
```
visit [localhost:9464](http://localhost:9464/metrics) to view the metrics


## CLIENT FASTAPI-OTEL-PUSH
```bash
export OTEL_SERVICE_NAME='fast_otel'
export OTEL_TRACES_EXPORTER='' 
export OTEL_METRIC_EXPORT_INTERVAL=15000
OTEL_EXPORTER_OTLP_METRICS_PROTOCOL='http/protobuf' OTEL_EXPORTER_OTLP_METRICS_ENDPOINT='http://localhost:9090/api/v1/otlp/v1/metrics' \
opentelemetry-instrument uvicorn fast_otel:app
```


## REFERENCE
- [prometheus.github.io/client_python/](http://prometheus.github.io/client_python/)
- [pypi.org/project/prometheus-fastapi-instrumentator/](https://pypi.org/project/prometheus-fastapi-instrumentator/)
- [opentelemetry.io/docs/languages/python/](http://opentelemetry.io/docs/languages/python/)
- [prometheus.io/docs/guides/opentelemetry/](http://prometheus.io/docs/guides/opentelemetry/)