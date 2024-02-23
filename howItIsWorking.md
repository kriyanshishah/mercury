# This is a version of mercury that supports mercury inside the jupyterhub pod
Here this version that works with jupyter server proxy.

prerequsites:
- working setup of jupyterhub with any kind of spawner. This version is tested and working with `Kubespawner`. You can contribute by checking if this works with other spawner.

### Here this version works with jupyter server proxy.

Before starting you need to set environment varibales `MERCURY_APP_PREFIX` and `MECURY_SERVER_URL`. 

`MERCURY_APP_PREFIX` is a subpath where the requests will be made and frontend will be served.

for example for jupyterhub user with name  'username' `MERCURY_APP_PREFIX` will be '/user/username/mercury'.

and `MECURY_SERVER_URL` will be '127.0.0.1:8080'.


### Setup required to run this version on jupyterhub:
- jupyter-server-proxy installed and activated with this command:
```
jupyter serverextension enable --sys-prefix jupyter_server_proxy
```
- setting up jupyter_server_config.py at on of `jupyter --paths`. You can check documentation of `jupyter-server-proxy` [here](https://jupyter-server-proxy.readthedocs.io/en/latest/)  

    the `jupyter_server_config.py` will look like this:
```
c = get_config() #noqa

c.ServerProxy.servers = {
    'mercury': {
        'command': ['mercury', 'run', '0.0.0.0:8080', '--verbose'],
        'timeout': 2 * 60,
        'absolute_url': False,
        'port': '8080',
        'new_browser_window': False,
        'launcher_entry':{
            'enabled': True,
            'title': 'mercury server'
        }
    }
}
```

- in `jupyterhub_config.py` you need to set environement variables `MERCURY_APP_PREFIX` and `MECURY_SERVER_URL`,
- you need to make custom front end with subpath '/user/username/mercury' for each user as per shown here[https://runmercury.com/docs/docker-compose/#deploy-on-subpath] by changing `package.json` and `Routes.tsx`. create wheel using this [script](scripts/build_wheel_custom_frontend.sh) and this use user specific wheel in each user environment.
