### This is a version of mercury that supports mercury inside the jupyterhub pod
Here this version works with jupyter server proxy and custom node proxy.

Before staring you need to set environment varibales `MERCURY_APP_PREFIX` and `MECURY_SERVER_URL`. 

`MERCURY_APP_PREFIX` is a subpath where the requests will be made and front end will be served.

for example for jupyterhub `MERCURY_APP_PREFIX` will be '/user/username/mercury'.

and `MECURY_SERVER_URL` will be '127.0.0.1:8080'.

the custom proxy will listen at port `8080` and serve it at `10000` and jupyter-server-proxy will listen at `10000` port and serve it at subpath `/mercury`.

Setup required to run this version on jupyterhub:
- node installed in the environment 
- jupyter-server-proxy installed and activated with this command:
```
jupyter serverextension enable --sys-prefix jupyter_server_proxy
```
- in `jupyterhub_config.py` you need to set environement variables `MERCURY_APP_PREFIX` and `MECURY_SERVER_URL`,
- you need to make custom front end with subpath '/user/username/mercury' as per shown here[https://runmercury.com/docs/docker-compose/#deploy-on-subpath] by changing `package.json` and `Routes.tsx`


the start up script when starting mercury will be:
```
node proxy/proxy.js
mercury run 127.0.0.1:8080 --verbose
```
