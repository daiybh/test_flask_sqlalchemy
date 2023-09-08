from app import db

class Led(db.Model):
    ledid = db.Column(db.String(50), primary_key=True)
    park_id = db.Column(db.String(50))

    def to_dict(self):
        return {
            'ledid': self.ledid,
            'park_id': self.park_id
        }
