const express = require("express");
const router = express.Router();
const Product = require("../models/product");
const Cart = require("../models/cart");
const Order = require("../models/order");

router.get("/", async (req, res, next) => {
  try {
    const docs = await Product.find();
    const chunkSize = 3;
    const productChunks = Array.from({ length: Math.ceil(docs.length / chunkSize) }, (v, i) =>
      docs.slice(i * chunkSize, i * chunkSize + chunkSize)
    );

    const messages = req.flash('success');
    res.render("shop/index", {
      title: "Shopping Cart",
      products: productChunks,
      messages,
    });
  } catch (err) {
    console.error("Error fetching products:", err);
    res.status(500).send("Internal Server Error");
  }
});

router.get("/add-to-cart/:id", async (req, res, next) => {
  try {
    const { id } = req.params;
    const cart = new Cart(req.session.cart || {});

    const product = await Product.findById(id).exec();

    if (!product) {
      return res.redirect('/');
    }

    cart.add(product, product.id);
    req.session.cart = cart;
    console.log(cart);
    res.redirect('/');
  } catch (err) {
    console.error(err);
    res.redirect('/');
  }
});

router.get('/basket', (req, res, next) => {
  const { cart } = req.session;

  if (!cart) {
    return res.render("shop/basket", { products: null });
  }

  const cartInstance = new Cart(cart);
  res.render('shop/basket', { products: cartInstance.generateArray(), totalPrice: cartInstance.totalPrice });
});

router.get('/checkout', isLoggedIn, (req, res, next) => {
  const { cart } = req.session;

  if (!cart) {
    return res.redirect("shop/basket");
  }

  const cartInstance = new Cart(cart);
  res.render('shop/checkout', { total: cartInstance.totalPrice });
});

router.post('/checkout', isLoggedIn, async (req, res, next) => {
  try {
    const { cart } = req.session;

    if (!cart) {
      return res.redirect("shop/basket");
    }

    const cartInstance = new Cart(cart);

    const order = new Order({
      user: req.user,
      cart: cartInstance,
      address: req.body.address,
      name: req.body.name,
      cardNumber: req.body.cardNumber,
      cardExpiry: req.body.cardExpiry,
      cvv: req.body.cvv
    });

    await order.save();

    req.flash('success', "Successfully bought products!");
    req.session.cart = null;
    res.redirect('/');
  } catch (err) {
    console.error(err);
    res.redirect('/');
  }
});

module.exports = router;

function isLoggedIn(req, res, next) {
  if (req.isAuthenticated()) {
    return next();
  }
  req.session.oldUrl = req.url;
  res.redirect('/user/signin');
}
