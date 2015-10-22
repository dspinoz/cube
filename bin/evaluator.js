#!/usr/bin/env node

var options = require("/etc/cube/evaluator-config"),
    cube = require("cube"),
    server = cube.server(options);

server.register = function(db, endpoints) {
  cube.evaluator.register(db, endpoints);
};

server.start();
