from application import db
from passlib.hash import pbkdf2_sha256 as sha256

#--------------------------------users----------------------------------
class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    salt = db.Column(db.String(120), nullable=False)
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
                'email': x.email,
                'password': x.password,
                "salt": x.salt,
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

#--------------------------------topic----------------------------------
class TopicModel(db.Model):
    __tablename__ = 'topic'

    id = db.Column(db.Integer, primary_key=True)
    topic_name = db.Column(db.String(120), unique=True, nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, topic_id):
        return cls.query.filter_by(id=topic_id).all()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                "id": x.id,
                'topic_name': x.topic_name,
            }
        return {'topics': list(map(lambda x: to_json(x), TopicModel.query.all()))}


#--------------------------------topic----------------------------------
class TopicOptionModel(db.Model):
    __tablename__ = 'topic_options'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Integer, db.ForeignKey('topic.id'))
    option = db.Column(db.String(120), unique=True, nullable=False)
    result = db.Column(db.Integer, unique=True, nullable=False,default=0)
    topic_name = db.relationship('TopicModel', backref='topic')


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_topic(cls, topic_id):
        return cls.query.filter_by(key=topic_id).all()

    @classmethod
    def find_by_topic_id_option_id(cls, topic_id,option_id):
        return cls.query.filter_by(key=topic_id,id=option_id).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                "option_id": x.id,
                "topic_id": x.key,
                'topic': x.topic_name.topic_name,
                'option': x.option,
                'result': x.result,
            }

        return {'topic_options': list(map(lambda x: to_json(x), TopicOptionModel.query.all()))}
