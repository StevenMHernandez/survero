import os
from masonite import Upload
from masonite.view import View
from masonite.request import Request
from masonite.controllers import Controller
from masoniteorm.query import QueryBuilder
from masonite.helpers import config

from app.Screenshot import Screenshot
from app.services.WorkspaceService import WorkspaceService

class ScreenshotsController(Controller):

    def index(self, view: View, workspaceService: WorkspaceService):
        return view.render("screenshots.index", {'workspace': workspaceService.workspace})

    def create(self, upload: Upload, request: Request):
        file_name = upload.driver('disk').store(request.input('upload'))
        screenshot = Screenshot.create({
            'paper_key': request.input('paper_key'),
            'file_name': file_name,
            'user_id': request.user().id,
        })
        return {"status": "success", "model": screenshot.serialize()}

    def delete(self, request: Request):
        screenshot = Screenshot.find(request.param('id'))
        os.remove(f"{config('storage.DRIVERS.disk.location')}/{screenshot.file_name}")
        Screenshot.where('id', request.param('id')).delete()

        return {"status": "success"}

    def api_index(self, workspaceService: WorkspaceService):
        screenshots = Screenshot \
            .where_in('paper_key', workspaceService.get_paper_keys())\
            .order_by('created_at', 'DESC')\
            .with_('user').all().serialize()

        items = QueryBuilder().on('zotero').table("items") \
            .where_in('items.key', [s['paper_key'] for s in screenshots]) \
            .join('itemData', 'items.itemID', '=', 'itemData.itemID') \
            .join('itemDataValues', 'itemData.valueID', '=', 'itemDataValues.valueID') \
            .where('itemData.fieldID', '=', ITEM_DATA_FIELD__TITLE) \
            .group_by('items.itemID') \
            .select_raw('items.key, itemDataValues.value as title') \
            .order_by('title', 'asc') \
            .get()

        titles = {it['key']: it['title'] for it in items}

        def add_items(s):
            s['paper_title'] = titles[s['paper_key']]
            return s

        screenshots = [add_items(s) for s in screenshots]

        return screenshots
