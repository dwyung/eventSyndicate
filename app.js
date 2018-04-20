var express = require("express"),
    app     = express(),
    sqlite  = require("sqlite3").verbose(),
    path = require("path"),
    bodyParser = require("body-parser");

app.set("view engine", "ejs");
app.use(bodyParser.urlencoded({extended: true}));

var dbPath = path.resolve(__dirname, 'events.sqlite');

var db = new sqlite.Database(dbPath);


db.serialize(function () {
    // name, description, organizer, start date, start time, end date, end time, time zone, location, price, currency, synicated

  db.run('CREATE TABLE IF NOT EXISTS product (name TEXT, description TEXT, merchant TEXT, startdate TEXT, starttime TEXT, enddate TEXT, endtime TEXT, timezone TEXT, location TEXT, price TEXT, currency TEXT, s INTEGER)');

});


// CREATE
app.post("/events", function(req, res){
    var event = req.body.event;
    db.run("BEGIN TRANSACTION");
    db.run('INSERT INTO product VALUES (?,?,?,?,?,?,?,?,?,?,?,?)' , [event.name, event.description, event.merchant, event.startdate, event.starttime, event.enddate, event.endtime, event.timezone, event.location, event.price, event.currency, 0]);
    db.run("END");
    // db.each('SELECT rowid AS id, * FROM product', function (err, row) {
    //     console.log(row.id + ': ' + row.name + ", " + row.starttime + ", " + row.location + ", " + row.description + ", " + row.price + ", " +row.s)
    // });

    res.send("You have submitted an event.");

});

// NEW
app.get("/events/new", function(req, res){
    res.render("new");
});

// ALL
app.get("*", function(req, res){
    res.redirect("/events/new");

});


// app.listen(process.env.PORT, process.env.IP, function(){
//     console.log("server has started!");
// });

app.listen(3000, function(){
    console.log("server has started!");
});
