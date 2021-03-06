// Much like db.collection, but caches the result for both events and metrics.
// Also, this is synchronous, since we are opening a collection unsafely.
var types = module.exports = function(db) {
  var collections = {};
  return function(type) {
    var collection = collections[type];
    if (!collection) {
      collection = collections[type] = {};
      db.collection(type + "_events", function(error, events) {
        collection.events = events;
      });
      db.collection(type + "_metrics", function(error, metrics) {
        collection.metrics = metrics;
      });
    }
    return collection;
  };
};

var eventRe = /_events$/;

types.getter = function(db) {
  return function(request, callback) {
    db.listCollections().toArray(function(error, names) {
      handle(error);
      callback(names
            .map(function(d) { 
				// TODO why split on '.' ?
				var tok = d.name.split("."); return tok[0]; 
			})
            .filter(function(d) { return eventRe.test(d); })
            .map(function(d) { return d.substring(0, d.length - 7); })
            .sort());
    });
  };
};

function handle(error) {
  if (error) throw error;
}
