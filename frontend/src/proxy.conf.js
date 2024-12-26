const PROXY_CONFIG = [
    {
        context: [
            "/api",
        ],
        "target": "http://localhost:9000/",
        "secure": false,
        onProxyReq: (proxyReq) => {
            proxyReq.setHeader('webpass-remote-user','TOTO_USER');
        },
    },
];

module.exports = PROXY_CONFIG;