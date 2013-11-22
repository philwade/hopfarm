import sys, csv, codecs
import MySQLdb

class Database:
    def __init__(self, db=None):
        if db is None:
            self.db = MySQLdb.connect(host="mysql.XXXXXXXXXXXXX.com", user="XXXXXXXX", passwd="XXXXXXXXXXX", db="XXXXXXXXXXXXX").cursor()
        else:
            self.db = db

    def insert_hop(self, name, alpha=None, description=None):
        hop_id = self.get_hop_id_by_name(name)
        if hop_id == None:
            websafe_name = self.create_websafe(name)
            self.db.execute('INSERT INTO hop VALUES(null, %s, %s, %s, %s)', [name, websafe_name, alpha, description])
            hop_id = self.db.lastrowid
        else:
            self.update_hop(hop_id, alpha, description)
        return hop_id

    def update_hop(self, hop_id, alpha, description):
        cur = self.db.execute('UPDATE hop set alpha_acid=%s, description=%s WHERE id=%s', [alpha, description, hop_id])

    def create_style(self, name):
        websafe_name = self.create_websafe(name)
        style_id = self.get_style_id(name)

        if style_id == None:
            self.db.execute('INSERT INTO beer_style VALUES(null, %s, %s, null)', [name, websafe_name])
            style_id = self.db.lastrowid

        return style_id

    def list_hops(self):
        self.db.execute('SELECT * from hop');
        hops = self.db.fetchall()
        return hops

    def get_hop_id_by_name(self, name):
        websafe_name = self.create_websafe(name)
        self.db.execute('SELECT id FROM hop where websafe_name=%s', [websafe_name])
        hop_id = self.db.fetchall()

        if hop_id:
            return hop_id[0][0]
        else:
            return None

    def link_hop_style(self, style_id, hop_id):

        if not self.check_style_link(style_id, hop_id):
            self.db.execute('INSERT INTO hop_style_map values(%s, %s)', [hop_id, style_id])

    def check_style_link(self, style_id, hop_id):
        self.db.execute('SELECT * FROM hop_style_map WHERE hop_id=%s and style_id=%s', [hop_id, style_id])

        pair = self.db.fetchall()

        if pair:
            return True
        return False

    def get_style_id(self, name):
        name = self.create_websafe(name)
        self.db.execute('SELECT id from beer_style where websafe_name=%s', [name])
        style_id = self.db.fetchall()

        if style_id:
            return style_id[0][0]
        else:
            return None

    def create_hop_alt(self, hop_id, alt_id):
       self.db.execute('SELECT * from hop_alternative where hop_id=%s and alternative_id=%s', [hop_id, alt_id])
       alt_exists = self.db.fetchall()

       if not alt_exists:
            self.db.execute('INSERT into hop_alternative VALUES(%s, %s)', [hop_id, alt_id])

    def create_websafe(self, name):
        return name.replace(' ', '_').replace('.', '').replace(')', '').replace('(', '').lower()

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

def create_alts(main_hop_id, alts):
    for alt in alts:
        alt.strip().replace('"', '')
        hop_id = db.get_hop_id_by_name(alt)

        if hop_id == None:
           hop_id = db.insert_hop(alt)

    db.create_hop_alt(main_hop_id, hop_id)

f = codecs.open(sys.argv[1], 'r', 'utf-8')
style_name = f.readline().replace(',', '').strip()
csvreader = unicode_csv_reader(f)
db = Database()

style_id = db.create_style(style_name)
for line in csvreader:
    hop = splitrow(line)
    hop_id = db.insert_hop(hop['name'], hop['alpha'], hop['description'])
    db.link_hop_style(style_id, hop_id)
    alts = hop['alts'].split(',')
    create_alts(hop_id, alts)

