from masoniteorm.models import Model


class Tag(Model):
    __connection__ = "sqlite"
    __fillable__ = ["paper_key", "tag"]
