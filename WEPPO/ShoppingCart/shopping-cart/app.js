const createError = require("http-errors");
const express = require("express");
const path = require("path");
const cookieParser = require("cookie-parser");
const logger = require("morgan");
const Handlebars = require("handlebars");
const expressHbs = require("express-handlebars");
const mongoose = require("mongoose");
const session = require("express-session");
const passport = require("passport");
const flash = require("connect-flash");
const MongoStore = require("connect-mongo");

// Byly problemy z ładowaniem zdjęć, najprostsze rozwiązanie:
const { allowInsecurePrototypeAccess } = require("@handlebars/allow-prototype-access");

const app = express();
mongoose.connect("mongodb://localhost:27017/shopping");

require("./config/passport");

// view engine setup
app.set("views", path.join(__dirname, "views"));

app.engine(
  ".hbs",
  expressHbs.engine({
    defaultLayout: "layout",
    extname: ".hbs",
    handlebars: allowInsecurePrototypeAccess(Handlebars),
  })
);
app.set("view engine", ".hbs");

app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, "public")));
app.use(
  session({
    secret: "2137",
    resave: false,
    saveUninitialized: false,
    store: MongoStore.create({ mongoUrl: "mongodb://localhost:27017/shopping" }),
    cookie: { maxAge: 180 * 60 * 1000 },
  })
);
app.use(flash());
app.use(passport.initialize());
app.use(passport.session());

const indexRoutes = require("./routes/index");
const userRoutes = require("./routes/user");

app.use((req, res, next) => {
  res.locals.login = req.isAuthenticated();
  res.locals.session = req.session;
  next();
});

app.use("/user", userRoutes);
app.use("/", indexRoutes);

// catch 404 and forward to error handler
app.use((req, res, next) => {
  next(createError(404));
});

// error handler
app.use((err, req, res, next) => {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get("env") === "development" ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render("error");
});

module.exports = app;
