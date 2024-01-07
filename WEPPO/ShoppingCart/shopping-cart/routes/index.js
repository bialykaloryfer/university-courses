var express = require('express');
var router = express.Router();
var Product = require('../models/product');

router.get('/', async function (req, res, next) {
  try {
    const docs = await Product.find();
    var productChunks = [];
    var chunkSize = 3;
    for (var i = 0; i < docs.length; i += chunkSize) {
      productChunks.push(docs.slice(i, i + chunkSize));
    }
    res.render('shop/index', { title: 'Shopping Cart', products: productChunks });
  } catch (err) {
    console.error('Error fetching products:', err);
    res.status(500).send('Internal Server Error');
  }
});

router.get('/user/signup', function(req, res, next) {
  res.render('user/signup')
})

router.post('/user/signup', function(req, res, next) {
  res.redirect('/')
})

module.exports = router;
