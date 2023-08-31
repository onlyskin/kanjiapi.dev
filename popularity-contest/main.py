import functions_framework
from google.cloud import storage

import csv
from collections import Counter
from datetime import datetime, timedelta, date
import json


def list_of_kanji_from_csv_lines(f):
    reader = csv.DictReader(f)
    items = list(reader)
    return [i['cs_object'].replace('v1/kanji/', '') for i in items if i['cs_object'].startswith('v1/kanji/') and i['sc_status'] in ('200', '304')]


def all_kanji_from_csv_strings(files):
    all_kanji = []
    for file in files:
        all_kanji.extend(list_of_kanji_from_csv_lines(file.splitlines()))
    return all_kanji


def get_match_string(dt):
    return dt.strftime('%Y_%m_%d_%H')


def get_last_n_hours_datetimes(n):
    return [datetime.utcnow() - timedelta(hours=i) for i in range(0, n)]
        

@functions_framework.cloud_event
def handle(e):
    print('popularity contest cloud function triggered')
    new_log_file_name = e.data['name']
    print(f'{new_log_file_name} written to kanjiapi-dev-logging')

    logging_bucket_name = 'kanjiapi-dev-logging'
    popularity_bucket_name = 'kanjiapi-popularity-contest'

    storage_client = storage.Client()

    usage_blobs_matching_new_log_datetime = [
            blob for blob
            in storage_client.list_blobs(logging_bucket_name)
            if new_log_file_name[:38]in blob.name
    ]

    popularity_bucket = storage_client.bucket(popularity_bucket_name)

    blobs_as_contents = [blob.download_as_text() for blob
                         in usage_blobs_matching_new_log_datetime]
    all_kanji_for_hour = all_kanji_from_csv_strings(blobs_as_contents)
    counter = Counter(all_kanji_for_hour)
    file_contents = json.dumps(counter.most_common())

    upload_blob_name = new_log_file_name[19:32]
    blob = popularity_bucket.blob(upload_blob_name)
    blob.cache_control = "max-age=1"
    blob.upload_from_string(file_contents, content_type='application/json')


class MockEvent:
    def __init__(self, name_stub):
        self.data = { 'name': name_stub}


if __name__ == '__main__':
    today = date.today()

    for i in range(0, 24):
        hour = datetime(today.year, today.month, today.day, i)
        name_stub = f'kanjiapi.dev_usage_{get_match_string(hour)}'
        mock_event = MockEvent(name_stub)
        print(mock_event.data)
        handle(mock_event)
