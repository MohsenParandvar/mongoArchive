import yaml
import argparse
from time import sleep
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.write_concern import WriteConcern

# Get the yml file path with args or default
parser = argparse.ArgumentParser(description='MongoDB archive data')
parser.add_argument('--config', default='config.yml', help='Config file path')
parser.add_argument('-y', action='store_true', help='Accept delete without interactive mode')
args = parser.parse_args()


# Get the config file
try:
    with open(args.config, 'r') as stream:
        config = yaml.safe_load(stream)
except Exception as e:
    print(e)
    exit()

# Connect to MongoDB by config
client = MongoClient(config['db_uri'])

# Check if the client is connected
if client is None:
    print("MongoDB Cant be connected!")
    exit()

# Check if the database exists
if client[config['database']] is None:
    print(f"Database {config['database']} not found!")
    exit()

# Get the database
db = client[config['database']]

# Check if -y argument is set
if args.y:
    pass
else:
    # Ask for confirmation
    confirm = input(f"Are you sure you want to delete older data? (y/n): ")
    if confirm.lower() == 'y':
        pass
    else:
        print ("Exiting...")
        exit()

for collection in config['collections']:
    # Check if collection exists
    if db[collection] is None:
        print(f"Collection {collection} not found!")
        continue

    print(f"Archiving {collection} older than {config['archive_days']} days data...")

    # Get the date of archive
    date = datetime.now() - timedelta(days=config['archive_days'])
    
    # Convert date to string by `date_format` field in config
    date = date.strftime(config['date_format'])

    # Get the collection
    target_collection = db[collection]

    # Archive older data to new collection by `affix_collection` field in config
    new_collection = db[f"{collection}{config['affix_collection']}"]

    # Insert data to new collection if fails exit
    try:
        if config['queuing']:
            # Insert data to new collection with queue while data exists
            while target_collection.count_documents({'date': {'$lt': date}}) > 0:
                try:
                    # find data and insert to new collection
                    stage_rows = target_collection.find({'date': {'$lt': date}}).limit(config['queue_size'])
                    stage_list = list(stage_rows)

                    if stage_list:
                        new_collection.with_options(write_concern=WriteConcern(w=0)).insert_many(stage_list)
                        print(f"{config['queue_size']} items inserted to {collection}{config['affix_collection']}...")

                        # Get ids to delete
                        ids_to_delete = [row['_id'] for row in stage_list]

                        # Delete stage data from main collection
                        target_collection.delete_many({'_id': {'$in': ids_to_delete}})
                        print(f"{config['queue_size']} items Deleted from {collection}...")

                except Exception as e:
                    print(e)
                sleep(1)
        else:
            # Insert data to new collection without queue
            new_collection.with_options(write_concern=WriteConcern(w=0)).insert_many(target_collection.find({'date': {'$lt': date}}))

        # Delete data from main collection limit by `queue_size` field in config
        print(f"Deleting {collection} older than {config['archive_days']} days data...")

        target_collection.delete_many({'date': {'$lt': date}})

        print(f"{collection} older than {config['archive_days']} days data deleted successfully!")

        print(f"{collection} archived successfully!")
    except Exception as e:
        print(e)
        exit()

    
