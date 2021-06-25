from masoniteorm.models import Model


class Note(Model):
    __connection__ = "sqlite"
    __fillable__ = ["paper_key", "note"]
