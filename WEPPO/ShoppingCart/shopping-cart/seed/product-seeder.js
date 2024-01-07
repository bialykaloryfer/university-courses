var Product = require('../models/product');
var mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/shopping');

var products = [
    new Product({
        imagePath: "https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/Witcher_3_cover_art.jpg/220px-Witcher_3_cover_art.jpg",
        title: "Witcher 3",
        description: "Best game ever!",
        price: 10
    }),
    new Product({
        imagePath:"https://upload.wikimedia.org/wikipedia/en/5/5e/Gothiccover.png",
        title: "Gothic 1",
        description: "Very old, very cool!",
        price: 5
    }),
    new Product({
        imagePath:"https://cdn-bgp.bluestacks.com/BGP/us/gametiles_com.mojang.minecraftpe.jpg",
        title: "Minecraft",
        description: "Build you own world!",
        price: 15
    }),
    new Product({
        imagePath:"https://m.media-amazon.com/images/M/MV5BNzU2YTY2OTgtZGZjZi00MTAyLThlYjUtMWM5ZmYzOGEyOWJhXkEyXkFqcGdeQXVyNTgyNTA4MjM@._V1_FMjpg_UX1000_.jpg",
        title: "Fortnite",
        description: "Quite good!",
        price: 0
    }),
    new Product({
        imagePath:"https://static.muve.pl/uploads/product-cover/0041/7939/cover.jpg",
        title: "Tom Clancy's Rainbow Six Siege",
        description: "One of most popular AAA shooters!",
        price: 20
    }),
    new Product({
        imagePath:"https://image.api.playstation.com/vulcan/ap/rnd/202009/2818/FuG72QFUf4aRYbSBAMNH2xwm.png",
        title: "The Elder Scrolls V: Skyrim",
        description: "Definetely recommend!",
        price: 10
    })
];

async function seedProducts() {
    try {
        for (let i = 0; i < products.length; i++) {
            await products[i].save();
        }
        console.log('All products saved successfully');
    } catch (err) {
        console.error('Error saving products:', err);
    } finally {
        mongoose.disconnect();
    }
}

seedProducts();