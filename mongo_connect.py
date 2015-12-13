def mongo_connect(username, password):
  connection = MongoClient("ds027385.mongolab.com", 27385)

  db = connection["antirec"]

  db.authenticate(username, password)

  return db