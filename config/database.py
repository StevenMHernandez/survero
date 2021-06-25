""" Database Settings """

import os

from masonite.environment import LoadEnvironment, env
from masoniteorm.query import QueryBuilder
from masoniteorm.connections import ConnectionResolver

"""
|--------------------------------------------------------------------------
| Load Environment Variables
|--------------------------------------------------------------------------
|
| Loads in the environment variables when this page is imported.
|
"""

LoadEnvironment()

"""
The connections here don't determine the database but determine the "connection".
They can be named whatever you want.
"""

DATABASES = {
    'default': env('DB_CONNECTION', 'sqlite'),
    'sqlite': {
        'driver': 'sqlite',
        'database': '/usr/src/db/survero/survero.sqlite',
        'prefix': ''
    },
    'zotero': {
        'driver': 'sqlite',
        'database': '/usr/src/db/zotero/zotero.sqlite',
        'prefix': ''
    }
}

DB = ConnectionResolver().set_connection_details(DATABASES)
