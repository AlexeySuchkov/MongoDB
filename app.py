import csv
from pprint import pprint
from pymongo import MongoClient

file = 'artists.csv'
db_name = 'homework'


class Ticket:

    def __init__(self, file, db_name):
        self.file = file
        self.client = MongoClient()
        self.db = self.client[db_name]
        self.raw_collection = self.db.raw_ticket
        self.collection = self.db.ticket

    def read_data(self):
        with open(self.file, encoding='utf8') as file:
            reader = csv.DictReader(file)
            self.raw_collection.insert_many([row for row in reader]).inserted_ids
        self.raw_collection.drop()

    def cheapest(self, find_doc={}):
        cursor = self.collection.find(find_doc, {'_id': False}).sort('Цена').collation(
            {'locale': 'en_US', 'numericOrdering': True})
        return [elem for elem in cursor]

    def find_artist(self, artist_name):
        return self.cheapest({'Исполнитель': {'$regex': f'/*{artist_name}', '$options': '$i'}})


if __name__ == '__main__':
    ticket = Ticket(file, db_name)

    ticket.read_data()
    print('Отсортировано по цене:')
    pprint(ticket.cheapest())
    print('Поиск по исполнителю:')
    pprint(ticket.find_artist('ча'))
