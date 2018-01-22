from src import db
from src.models.permission import Permission


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    permissions = db.Column(db.Integer)

    @staticmethod
    def insert_roles():
        roles = {
            'Guest': (Permission.READ |
                      Permission.WRITE, True),
            'User': (Permission.READ |
                     Permission.WRITE |
                     Permission.EXECUTE ,False),
            'Admin': (0xff, False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
            db.session.commit()
