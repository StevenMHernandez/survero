from masoniteorm.models import Model
from masoniteorm.relationships import belongs_to


class Note(Model):
    __connection__ = "sqlite"
    __fillable__ = ["paper_key", "note", "user_id"]

    @belongs_to('user_id', 'id')
    def user(self):
        from app.User import User
        return User
