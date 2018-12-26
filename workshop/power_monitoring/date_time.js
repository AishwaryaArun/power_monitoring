var http = require('http');

http.createServer(function (req, res) {
var currentTime = new Date().toISOString().
  replace(/T/, ' ').
  replace(/\..+/, '');
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end(currentTime);
}).listen(80, '192.168.43.254');
console.log('Server running at http://192.168.43.254:80/');


