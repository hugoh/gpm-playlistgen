import json

from dbitem import *

class DbPlaylist(DbItem):

    def __init__(self):
        columns = [
            DbColumn('id', 'TEXT'),
            DbColumn('name', 'TEXT'),
            DbColumn('description', 'TEXT'),
            DbColumn('version', 'TEXT'),
            DbColumn('type', 'TEXT'),
            DbColumn('args', 'TEXT'),
            DbColumn('closed', 'INTEGER'),
        ]
        DbItem.__init__(self, columns)

    def from_playlist(self, p):
        self.id = p.get('id')
        self.name = p.get('name', '')
        self.description = p.get('description')
        d = json.loads(p.get('description'))
        self.version = d.get('version', '')
        self.type = d.get('type', '')
        self.args = d.get('args', '')
        if d.get('closed', False) == True:
            self.closed = 1
        else:
            self.closed = 0
