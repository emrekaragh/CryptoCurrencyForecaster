from pymongo import MongoClient

uri = "mongodb+srv://crypto-forecaster.bikyg.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority" #DO NOT TOUCH HERE
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='<PEM_FILE_PATH>') #ADD YOUR PEM FILE PATH HERE AS STRING AND REMOVE <> SYMBOLS

db = client['sample_airbnb'] #SAMPLE DATABASE
collection = db['listingsAndReviews'] #SAMPLE COLLECTION
doc_count = collection.count_documents({}) #COUNTS DOCUMENTATION
print(doc_count) #PRINTS DOCUMENTS COUNT
