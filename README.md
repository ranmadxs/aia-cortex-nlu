---
runme:
  id: 01HJQ7F9RYFAQG4NCAYG2PW00T
  version: v2.0
---

# aia-cortex-nlu

Natural Languague Understanding

```console {"id":"01HJQ7F9RXZBJJ4YEQA7Q49GYF"}
poetry run daemon

git ls-remote --get-url origin 
git remote set-url origin git@github_ranmadxs:ranmadxs/aia-cortex-nlu.git
```

## Docker

```console {"id":"01HJQ7F9RXZBJJ4YEQAAH1BXHZ"}
#build
docker docker build . --platform linux/arm64/v8 -t aia/aia-cortext-nlu:0.2.0

#go into docker container
sudo docker exec -ti aia_cortex_nlu bash

#run
docker run -d --rm -e TZ=America/Santiago -v /home/ranmadxs/aia/aia-cortex-nlu/target:/app/target --net=bridge --name aia_cortex_nlu --env-file .env aia/aia-cortext-nlu:0.2.0
```

### Install Img

```console {"id":"01HJQ7F9RXZBJJ4YEQAAX4XA1Y"}
docker save -o aia-cortex-nlu_0.2.0.tar aia/aia-cortext-nlu:0.2.0

docker load -i aia-cortex-nlu_0.2.0.tar
```
