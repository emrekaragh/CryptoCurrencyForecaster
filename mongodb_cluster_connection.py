from pymongo import MongoClient

uri = "mongodb+srv://crypto-forecaster.bikyg.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='emre_X509-cert-7315245080984398576.pem')

db = client['testDB']
collection = db['testCol']
doc_count = collection.count_documents({})
print(doc_count)
