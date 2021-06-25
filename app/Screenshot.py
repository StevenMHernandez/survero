from masoniteorm.models import Model


class Screenshot(Model):
    __connection__ = "sqlite"
    __fillable__ = ["paper_key", "file_name"]
