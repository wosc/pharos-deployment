var express = require('express');
var http = require('http');
var pkg = require('./package.json');
var ExpressPeerServer = require('./lib').ExpressPeerServer;


// copy&paste to add listen host, removed ssl stuff
function PeerServer(options, callback) {
  options = options || {};
  var path = options.path || '/';
  var port = options.port || 80;
  var host = options.host || '0.0.0.0';
  delete options.path;

  if (path[0] !== '/') {
    path = '/' + path;
  }
  if (path[path.length - 1] !== '/') {
    path += '/';
  }

  var app = express();
  var server = http.createServer(app);
  var peerjs = ExpressPeerServer(server, options);
  app.use(path, peerjs);

  server.listen(port, host, function() {
    callback(server);
  });

  return peerjs;
};

var server = PeerServer(
    {host: '127.0.0.1', port: 7077, path: '/', proxied: true}, function(server) {
  var host = server.address().address;
  var port = server.address().port;

  console.log(
    'Started PeerServer on %s, port: %s, path: %s (v. %s)',
    host, port, '/', pkg.version
  );
});
