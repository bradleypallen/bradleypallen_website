/**
 * @author Bradley Allen
 */

var mongodb = require('mongodb');

function results_page(req, res, view, options) {
    var client = new mongodb.Db(options.database, new mongodb.Server(options.host, options.port, {}), {});
    var n = 0;
    client.open(function(err, db) {
        client.authenticate(options.user, options.password, function(err, replies) {
            client.collection(options.collection, function(err, collection) {
                if (!req.query.p || !req.query.p.match(/^\d+$/)) {
                    page = 0
                } else {
                    page = parseInt(req.query.p)
                }
                collection.find(options.query, { limit: options.limit, sort: options.sort, skip: page*options.limit }, function(err, cursor) {
                    cursor.count(function(err, count) {
                        n = count
                    });
                    cursor.toArray(function(err, records) {
                        if (records !== null) {
                            res.render(view, {
				title: options.title,
				subtitle: options.subtitle,
                                results: records,
				query: options.query,
                                page: page,
                                count: n,
                                limit: options.limit
                            });
                        }
                        db.close();
                    });
                });
            });
        });
    });
}

exports.results_page = results_page;
