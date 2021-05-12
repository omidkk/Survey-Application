from application import db
from passlib.hash import pbkdf2_sha256 as sha256

#--------------------------------users----------------------------------
class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    group = db.Column(db.String(120), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def admin_add_to_group(cls, username, group):
        item = cls.query.filter_by(username=username).first()
        item.group = group
        db.session.commit()

    @classmethod
    def admin_create_admin(cls, username, password):
        item = cls(
                username=username,
                password=sha256.hash(password),
                group='admin'
            )
        db.session.add(item)
        db.session.commit()

    @classmethod
    def update_user(cls, username, updates):
       pass

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                "id": x.id,
                'username': x.username,
                'password': x.password,
                "team_name": x.team_name,
                "country": x.country,
                "group": x.group
            }

        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete_by_username(cls, username):
        db.session.query(cls).filter(cls.username == username).delete()
        db.session.commit()
        return {'message': 'item deleted successfully '}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
