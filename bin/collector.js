#!/usr/bin/env node

var options = require("/etc/cube/collector-config"),
    cube = require("cube"),
    server = cube.server(options);

server.register = function(db, endpoints) {
  cube.collector.register(db, endpoints);
};

server.start();
