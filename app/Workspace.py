from masoniteorm.models import Model
from masoniteorm.relationships import belongs_to


class Workspace(Model):
    __connection__ = "sqlite"
    __fillable__ = ["collection_key"]
