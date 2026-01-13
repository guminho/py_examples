from tritonclient.grpc import InferenceServerClient as TritonClient
from tritonclient.grpc import InferenceServerException

cli = TritonClient("localhost:8001")

print("\n# Health")
for o in (
    cli.is_server_live(headers={"test": "1"}),
    cli.is_server_ready(),
    cli.is_model_ready("simple"),
):
    print(o)

print("\n# Meta")
for o in (
    cli.get_server_metadata(),
    cli.get_model_repository_index(),
    cli.get_inference_statistics(),
    cli.get_model_metadata("simple"),
    cli.get_model_config("simple"),
):
    print(o)

# incorrect model
try:
    cli.get_model_metadata("wrong")
except InferenceServerException as exc:
    print(exc)
