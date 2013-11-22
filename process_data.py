import sys, csv, codecs
from sqlite3 import dbapi2 as sqlite3

class Database:
    def __init__(self, db=None):
        if db is None:
            self.db = sqlite3.connect(database='hops.db')
        else:
            self.db = db

    def insert_hop(self, name, alpha, description):
        websafe_name = self.create_websafe(name)
        self.db.execute('INSERT INTO hop VALUES(null, ?, ?, ?, ?)', [name, websafe_name, alpha, description]);
        self.db.commit()

    def list_hops(self):
        cur = self.db.execute('SELECT * from hop');
        hops = cur.fetchall()
        return hops

    def get_hop_id_by_name(self, name):
        websafe_name = self.create_websafe(name)
        cur = self.db.execute('SELECT id FROM hop where websafe_name=?', [websafe_name])
        hop_id = cur.fetchall()
        return hop_id[0][0]

    def create_websafe(self, name):
        return name.replace(' ', '_').replace(')', '_').replace('(', '_').lower()

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

def splitrow(row):

    return {
        'name' : row[0].replace('"', '').strip(),
        'alpha' : row[1].replace('"', '').strip(),
        'alts' : row[2].replace('"', '').strip(),
        'description' : row[3].replace('"', '').strip(),
    }

f = codecs.open(sys.argv[1], 'r', 'utf-8')
csvreader = unicode_csv_reader(f)
db = Database()

for line in csvreader:
    hop = splitrow(line)
    hop_id = db.insert_hop(hop['name'], hop['alpha'], hop['description'])
