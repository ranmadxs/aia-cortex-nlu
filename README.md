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

#run
docker run --rm --add-host=aiadb:172.17.0.2 --net=bridge --name aia_cortex_nlu --env-file .env aia/aia-cortext-nlu:0.1.0
```
