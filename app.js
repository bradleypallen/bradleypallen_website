/**
 * @author Bradley Allen
 * @fileOverview An Express.js application for bradleypallen.org
 * @see http://bradleypallen.org/colophon
 */

var express = require('express')
    , routes = require('./routes')
    , http = require('http');

var app = express();

app.configure(function(){
    app.set('port', 8081);
    app.set('views', __dirname + '/views');
    app.set('view engine', 'jade');
    app.use(express.logger('dev'));
    app.use(express.bodyParser());
    app.use(express.methodOverride());
    app.use(app.router);
    app.use(express.static(__dirname + '/public'));
});

app.get('/', routes.index);

app.get('/index.html', routes.index);

app.get('/cv.xhtml', routes.index);

app.get('/about', routes.index);

app.get('/colophon', routes.colophon);

http.createServer(app).listen(app.get('port'), function(){
    console.log("Express server listening on port " + app.get('port'));
});
