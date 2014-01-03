exports.index = function(req, res) {
    res.render('about', { title: 'Bradley P. Allen', subtitle: ''  });
};

exports.colophon = function(req, res) {
    res.render('colophon', { title: 'Bradley P. Allen', subtitle: 'Colophon'  });
};

