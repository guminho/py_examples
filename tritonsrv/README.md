# Triton Inference Server Examples

## ref

- https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tritonserver
- https://github.com/triton-inference-server/server/tree/main/docs/examples
- https://github.com/triton-inference-server/client/tree/main/src/python/examples
- https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/getting_started/quickstart.html

## run

```bash
cd tritonsrv
# clone model_repository from triton-server-examples
docker compose up -d

python simple_int.py
```
