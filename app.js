/**
 * @author Bradley Allen
 * @fileOverview An Express.js application for bradleypallen.org
 * @param int port the port for listening for HTTP requests
 * @param str dbhost the MongoDB server hostname
 * @param int dbport the MongoDB server port
 * @param str dbuser the MongoDB server user account name
 * @param str dbpassword the MongoDB server user account password
 * @see http://bradleypallen.org/colophon
 */

var express = require('express');

var requestHandlers = require('./requestHandlers');

var argv = require('optimist').argv;

var app = module.exports = express.createServer();

// Configuration

app.configure(function(){
  app.set('views', __dirname + '/views');
  app.set('view engine', 'jade');
  app.use(express.bodyParser());
  app.use(express.methodOverride());
  app.use(express.compiler({ src: __dirname + '/public', enable: ['sass'] }));
  app.use(app.router);
  app.use(express.static(__dirname + '/public'));
});

app.configure('development', function(){
  app.use(express.errorHandler({ dumpExceptions: true, showStack: true })); 
});

app.configure('production', function(){
  app.use(express.errorHandler()); 
});

// Routes

var db = 'pageback';
var coll = 'statuses';
var limit = 30;
var sort = [['date', 'desc']];

app.get('/', function(req, res){
  requestHandlers.results_page(req, res, 'index', { host: argv.dbhost, 
        port: argv.dbport,
  	database: db,
  	collection: coll,
  	user: argv.dbuser,
  	password: argv.dbpassword,
  	query: {},
        limit: 15,
  	sort: sort,
  	title: 'Bradley P. Allen',
  	subtitle: 'Recent status updates'
  });
});

app.get('/cv.xhtml', function(req, res){
  res.render('about', { title: 'Bradley P. Allen', subtitle: 'About'  });
});

app.get('/about', function(req, res){
  res.render('about', { title: 'Bradley P. Allen', subtitle: 'About'  });
});

app.get('/colophon', function(req, res){
  res.render('colophon', { title: 'Bradley P. Allen', subtitle: 'Colophon'  });
});

app.listen(argv.port, function(){
  console.log("Express server listening on port %d in %s mode", app.address().port, app.settings.env);
});