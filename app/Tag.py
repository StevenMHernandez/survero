from masoniteorm.models import Model
from masoniteorm.relationships import belongs_to


class Tag(Model):
    __connection__ = "sqlite"
    __fillable__ = ["paper_key", "tag"]

    @belongs_to('user_id', 'id')
    def user(self):
        from app.User import User
        return User
