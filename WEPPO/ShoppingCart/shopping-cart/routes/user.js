const express = require('express');
const router = express.Router();
const passport = require('passport');
const Order = require('../models/order');
const Cart = require('../models/cart');

const isLoggedIn = (req, res, next) => {
  if (req.isAuthenticated()) {
    return next();
  }
  res.redirect('/');
};

const notLoggedIn = (req, res, next) => {
  if (!req.isAuthenticated()) {
    return next();
  }
  res.redirect('/');
};

router.get('/profile', isLoggedIn, async (req, res, next) => {
  try {
    const orders = await Order.find({ user: req.user }).exec();

    for (const order of orders) {
      const cart = new Cart(order.cart);
      order.items = cart.generateArray();
    }

    res.render('user/profile', { orders });
  } catch (err) {
    console.error(err);
    next(err);
  }
});

router.get('/logout', isLoggedIn, (req, res, next) => {
  req.logout((err) => {
    if (err) {
      return next(err);
    }
    res.redirect('/');
  });
});

router.use('/', notLoggedIn, (req, res, next) => {
  next();
});

router.get('/signup', (req, res, next) => {
  const messages = req.flash('error');
  res.render('user/signup', { messages, hasErrors: messages.length > 0 });
});

router.post('/signup', passport.authenticate('local.signup', {
  failureRedirect: '/user/signup',
  failureFlash: true
}), (req, res, next) => {
  if (req.session.oldUrl) {
    const oldUrl = req.session.oldUrl;
    req.session.oldUrl = null;
    res.redirect(oldUrl);
  } else {
    res.redirect('/user/profile');
  }
});

router.get('/signin', (req, res, next) => {
  const messages = req.flash('error');
  res.render('user/signin', { messages, hasErrors: messages.length > 0 });
});

router.post('/signin', passport.authenticate('local.signin', {
  failureRedirect: '/user/signin',
  failureFlash: true
}), (req, res, next) => {
  if (req.session.oldUrl) {
    const oldUrl = req.session.oldUrl;
    req.session.oldUrl = null;
    res.redirect(oldUrl);
  } else {
    res.redirect('/user/profile');
  }
});

module.exports = router;
