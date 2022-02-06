from masoniteorm.models import Model
from masoniteorm.relationships import belongs_to


class BibtexEntry(Model):
    __connection__ = "sqlite"
    __fillable__ = ["paper_key", "bibtex"]
