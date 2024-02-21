c = get_config() #noqa

c.ServerProxy.servers = {
    'mercury': {
        'command': ['mercury', 'run', '0.0.0.0:8080', '--verbose'],
        'timeout': 2 * 60,
        'absolute_url': False,
        'port': '10000'
        'new_browser_window': False,
        'launcher_entry':{
            'enabled': True,
            'title': 'mercury server'
        }
    }
}