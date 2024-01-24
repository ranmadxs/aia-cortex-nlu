---
runme:
  id: 01HJQ7F9RYFAQG4NCAYG2PW00T
  version: v2.2
---

# aia-cortex-nlu

Natural Languague Understanding

```sh {"id":"01HJQ7F9RXZBJJ4YEQA7Q49GYF"}
poetry run daemon

poetry cache clear pypi --all

git ls-remote --get-url origin 
git remote set-url origin git@github_ranmadxs:ranmadxs/aia-cortex-nlu.git

#tags
git push --tags
```

## Docker

```sh {"id":"01HJV2GKHFHRCW2MAYBX6DWF7V"}
#set var entorno
export AIA_TAG_NLU=0.3.3
```

```sh {"id":"01HJQ7F9RXZBJJ4YEQAAH1BXHZ"}
#build
docker build . --platform linux/arm64/v8 -t keitarodxs/aia-cortext-nlu:$AIA_TAG_NLU

#push
docker push keitarodxs/aia-cortext-nlu:$AIA_TAG_NLU

#go into docker container
docker exec -ti aia_cortex_nlu bash

#run
docker run -d --restart=always -e TZ=America/Santiago -v /home/ranmadxs/aia/aia-device/resources/images:/wh40k_images -v /home/ranmadxs/aia/aia-cortex-nlu/target:/app/target --net=bridge --name aia_cortex_nlu --env-file .env keitarodxs/aia-cortext-nlu:$AIA_TAG_NLU
```

### Install Img

```sh {"id":"01HJQ7F9RXZBJJ4YEQAAX4XA1Y"}
docker save -o aia-cortex-nlu_$AIA_TAG_NLU.tar keitarodxs/aia-cortext-nlu:$AIA_TAG_NLU

docker pull keitarodxs/aia-cortext-nlu:$AIA_TAG_NLU

docker load -i aia-cortex-nlu_$AIA_TAG_NLU.tar
```
