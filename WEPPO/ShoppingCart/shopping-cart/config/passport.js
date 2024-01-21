const passport = require('passport');
const User = require('../models/user');
const LocalStrategy = require('passport-local').Strategy;
const bcrypt = require('bcrypt');

passport.serializeUser((user, done) => {
    done(null, user.id);
});

passport.deserializeUser(async (id, done) => {
    try {
        const user = await User.findById(id);
        done(null, user);
    } catch (err) {
        done(err, null);
    }
});

const validateEmail = email => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
const validatePassword = password => password.length >= 6;

passport.use('local.signup', new LocalStrategy({
    usernameField: 'email',
    passwordField: 'password',
    passReqToCallback: true
}, async (req, email, password, done) => {
    console.log('Starting local.signup strategy');
    if (!validateEmail(email)) {
        return done(null, false, { message: 'Invalid email' });
    }

    if (!validatePassword(password)) {
        return done(null, false, { message: 'Password must be at least 6 characters long' });
    }

    try {
        const user = await User.findOne({ email });

        if (user) {
            console.log('User already exists:', user);
            return done(null, false, { message: 'E-mail is already in use' });
        }

        const hashedPassword = await bcrypt.hash(password, 10);
        const newUser = new User({
            email,
            password: hashedPassword
        });

        const result = await newUser.save();

        console.log('User saved successfully:', result);
        return done(null, newUser);
    } catch (err) {
        console.error('Error during user signup:', err);
        return done(err);
    }
}));

passport.use('local.signin', new LocalStrategy({
    usernameField: 'email',
    passwordField: 'password',
    passReqToCallback: true
}, async (req, email, password, done) => {
    if (!validateEmail(email)) {
        return done(null, false, { message: 'Invalid email' });
    }

    try {
        const user = await User.findOne({ email });

        if (!user) {
            return done(null, false, { message: 'No user found' });
        }

        const isPasswordValid = await bcrypt.compare(password, user.password);

        if (!isPasswordValid) {
            return done(null, false, { message: 'Wrong password' });
        }

        return done(null, user);
    } catch (err) {
        console.error('Error during user login:', err);
        return done(err);
    }
}));

module.exports = passport;
