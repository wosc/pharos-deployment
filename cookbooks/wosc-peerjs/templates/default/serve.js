var pkg = require('./package.json');
var PeerServer = require('./lib').PeerServer;
var server = PeerServer(
    {port: 7077, path: '/', proxied: true}, function(server) {
  var host = server.address().address;
  var port = server.address().port;

  console.log(
    'Started PeerServer on %s, port: %s, path: %s (v. %s)',
    host, port, '/', pkg.version
  );
});
