import os
import datetime as dt
from datetime import datetime
from dateutil import tz

from masonite.helpers import config


class DBAgeService:
    def __init__(self):
        self.updated_at = int(os.path.getmtime(config('database.databases.zotero.database')))

    def updated_at_formatted(self):
        return datetime.fromtimestamp(
            self.updated_at,
            tz=tz.gettz(config('application.time_zone'))
        ).strftime("%y/%m/%d %H:%M:%S")

