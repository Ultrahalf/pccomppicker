var MongoClient = require('mongodb').MongoClient;
var dbUrl = "mongodb://localhost:27017/";


MongoClient.connect(dbUrl, function(err, db) {
  if (err) throw err;
  var dbo = db.db("pccomppicker");
      var query = { task: "remove" };
      dbo.collection("products").deleteMany(query, function(err) {
        if (err) throw err;
        db.close();
      });
    db.close();
});

