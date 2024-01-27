// admin.js
const express = require("express");
const router = express.Router();
const Product = require("../models/product");
const Order = require("../models/order");
const User = require("../models/user");

const isLoggedIn = (req, res, next) => {
  if (req.isAuthenticated() && req.user.admin) {
    return next();
  }
  res.redirect('/');
};

router.post('/add_product', async (req, res) => {
  try {
    console.log(req.body)
    const newProduct = new Product({
      title: req.body.title,
      imagePath: req.body.filepath,
      description: req.body.description,
      price: req.body.price,
    });
    await newProduct.save();

    res.redirect('admin');
  } catch (error) {
    res.status(500).send('Internal Server Error');
  }
});

router.post('/delete_product', async (req, res) => {
  try {
    const title = req.body.deleteTitle;
    console.log(title);
    await Product.findOneAndDelete({ title: title });
    res.redirect('admin');
  } catch (error) {
    console.error('Error Delete:', error);
    res.status(500).send('Internal Server Error');
  }
});

router.post('/edit_product', async (req, res) => {
  try {
    const product_to_edit = await Product.findOne({ title: req.body.editTitle});
    console.log(product_to_edit);
    console.log(req.body.new_title);

    const updateObject = {};

    if (req.body.new_title != "") {
      updateObject.title = req.body.new_title;
    }
    if (req.body.description != "") {
      updateObject.description = req.body.description;
    }
    if (req.body.filepath != "") {
      updateObject.imagePath = req.body.filepath;
    }
    if (req.body.price != "") {
      updateObject.price = req.body.price;
    }

    if (Object.keys(updateObject).length > 0) {
      await Product.updateOne(
        { _id: product_to_edit._id},  
        { $set: updateObject }
      );
    }

    res.redirect('/admin');
  } catch (error) {
    console.error(error);
    res.status(500).send('Internal Server Error');
  }
});




router.get('/admin', isLoggedIn, async (req, res, next)  => {
  try {
    const order = await Order.find();
    const users = await User.find();
    const products = await Product.find();
    res.render('admin', { order: order, users: users, products: products });
  } catch (error) {
    console.error('Error fetching products:', error);
  }
});

module.exports = router;
