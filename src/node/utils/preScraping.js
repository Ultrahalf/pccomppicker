var MongoClient = require('mongodb').MongoClient;
var dbUrl = "mongodb://localhost:27017/";


MongoClient.connect(dbUrl, function(err, db) {
  if (err) throw err;
  var dbo = db.db("pccomppicker");
  dbo.collection("products").find().toArray(function(err, result) {
    if (err) throw err;
    for(j = 0;  j < result.length; j++) {
      let id = result[j]._id;
      var query = { _id: id };
      var value = { $set: { task: "remove" } };
      dbo.collection("products").updateOne(query, value, function(err) {
        if (err) throw err;
        db.close();
      });
    }
    db.close();
});
});

