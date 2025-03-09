# MongoArchive

**MongoArchive** is a simple, customizable, and lightweight Python tool designed to archive MongoDB collections efficiently. With minimal dependencies (just `pymongo`), it provides a fast and flexible solution for managing your MongoDB data archiving needs.

---

## Key Features

- **Customizable**: Tailor the archiving process to fit your specific requirements.
- **Fast**: Optimized for quick and efficient data archiving.
- **Lightweight**: Minimal resource usage with only one dependency (`pymongo`).
- **Low Dependency**: No bloated libraries—just the essentials.

---

## Usage

Run the script from the command line with the following options:

```bash
usage: mongo-archive.py [-h] [--config CONFIG] [-y]

MongoDB Archive Tool

options:
  -h, --help       Show this help message and exit
  --config CONFIG  Path to the configuration file (default: config.yaml)
  -y               Skip interactive mode and automatically confirm deletions
```
You can automate the archiving process by setting up a cronjob to run the script at regular intervals.

## Configuration
The tool uses a YAML configuration file to define archiving rules. Below is the default configuration template, which you can customize to suit your needs:

```yaml
# Database configuration
db_uri: "mongodb://{USER}:{PASS}@{ADDRESSES}/?authSource={}"
database: "{DB_NAME}"
collections:
  - COLLECTION_1
  - COLLECTION_2

# Archive settings
archive_days: 90  # Archive documents older than this number of days
date_format: "%Y.%m.%d"  # Date format for archived collections
affix_collection: "_archive"  # Suffix for archived collection names
queuing: true  # Enable queuing for batch processing
queue_size: 1000  # Maximum number of documents to process in a single batch
```

## Example Cronjob
To run the archiving process daily at 2 AM, add the following to your crontab:
```bash
0 2 * * * /usr/bin/python3 /path/to/mongo-archive.py --config /path/to/config.yaml -y
```

## Buy me a coffee
If you'd like, you can buy me a coffee! ;)

[BuyMeACoffee](https://www.buymeacoffee.com/mohsenparandvar) ☕
