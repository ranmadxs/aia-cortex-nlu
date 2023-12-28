# aia-cortex-nlu
Natural Languague Understanding
```console
poetry run daemon

git ls-remote --get-url origin 
git remote set-url origin git@github_ranmadxs:ranmadxs/aia-cortex-nlu.git
```


## Docker

```console
#build
docker build . -t aia/aia-cortext-nlu:0.1.0 --platform linux/amd64

#go into docker container
sudo docker exec -ti aia_cortex_nlu bash

#run
docker run --rm -v /home/ranmadxs/aia/aia-cortex-nlu/logs:/app/target/logs --net=bridge --name aia_cortex_nlu --env-file .env aia/aia-cortext-nlu:0.1.0
```
