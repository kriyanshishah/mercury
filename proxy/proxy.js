var httpProxy = require('http-proxy')

let server_ip='127.0.0.1'
let server_port=8080, proxy_port=10000, 
var proxy = httpProxy.createProxyServer({target: "http://" +`${server_ip}:${server_port}`, ws:true}).listen(proxy_port);
var username = jhub_username
proxy.on('proxyReq', (proxyReq, req, res, options) => {
    let path = proxyReq.path;
    let tokens = path.split('/')
    if(path.includes("/static/media")){
        if(tokens[1] == 'user' && tokens[3] == 'mercury'){
            tokens.splice(1,3)
            path = tokens.join('/')
        }
    }else if(path.includes('/media/')){
        path = '/user/' + username + '/mercury' + path
    }else if(tokens[1]  == 'user' && tokens[3] == 'mercury'){
        tokens.splice(1,3)
        path = tokens.join('/')
    }

    if(path === ''){
        path = '/'
    }
    proxyReq = path
});

proxy.on('error', (err, req, res) => {
    if(err.errno == -111){
        res.end("waiting for mercury to get up")
    }else{
        res.end("Error occures" + err)
    }
});