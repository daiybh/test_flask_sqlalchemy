from app import db

class Park(db.Model):
    name = db.Column(db.String(50))
    park_id = db.Column(db.String(50), primary_key=True)
    pgmfilepath = db.Column(db.String(50))


    def to_dict(self):
        return {
            'name': self.name,
            'park_id': self.park_id,
            'pgmfilepath': self.pgmfilepath
        }
