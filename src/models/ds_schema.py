from src import db
from datetime import datetime


class DsSchema(db.Model):
    __tablename__ = 'ds_schemas'
    id = db.Column(db.Integer, primary_key=True)
    schema_name = db.Column(db.String(100))
    tables = db.Column(db.Text)
    fields = db.Column(db.Text)
    views = db.Column(db.Text)
    last_updated = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
