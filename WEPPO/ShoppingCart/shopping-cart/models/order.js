const mongoose = require('mongoose');
const { Schema } = mongoose;

const orderSchema = new Schema({
  user: { type: Schema.Types.ObjectId, ref: 'User' },
  cart: { type: Object, required: true },
  address: { type: String, required: true },
  name: { type: String, required: true },
  cardNumber: { type: String, required: true },
  cardExpiry: { type: String, required: true },
  cvv: { type: String, required: true },
});

module.exports = mongoose.model('Order', orderSchema);
