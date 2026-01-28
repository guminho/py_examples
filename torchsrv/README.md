# TorchServe Examples

## ref

- https://github.com/pytorch/serve/tree/master/examples/image_classifier/resnet_18
- https://github.com/pytorch/serve/tree/master/model-archiver
- https://docs.pytorch.org/serve/configuration.html
- https://docs.pytorch.org/serve/custom_service.html

## run

```bash
cd torchsrv

wget https://download.pytorch.org/models/resnet18-f37072fd.pth
bash archive_resnet18.sh
bash archive_greeter.sh
mkdir model-store
mv resnet-18.mar model-store/
mv greeter.mar model-store/

docker compose up -d

curl localhost:8081/models/resnet-18
curl localhost:8080/predictions/resnet-18 -T ./image_classifier/kitten.jpg
curl localhost:8080/predictions/grt -d 'body={"foo":"bar1"}'
```
