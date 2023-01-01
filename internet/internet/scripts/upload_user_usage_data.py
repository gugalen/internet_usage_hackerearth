import csv
from ..models import UsageData
import os


def readCsv():
    path = os.getcwd()
    d = os.path.abspath(os.path.join(path, os.pardir))
    file_path = os.path.join(d, 'internet/internet/data/data.csv')
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
        return data

def insertData(data:list):
    usage_list = []
    for row in data:
        usage = UsageData()
        usage.username = row['username']
        usage.mac_address = row['mac_address']
        usage.start_time = row['start_time']
        usage.usage_time = row['usage_time']
        usage.upload = row['upload']
        usage.download = row['download']
        usage_list.append(usage)
    UsageData.objects.bulk_create(usage_list)


def run():
    data = readCsv()
    if data:
        insertData(data)
