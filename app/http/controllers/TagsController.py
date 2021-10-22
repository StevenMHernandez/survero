from masonite.view import View
from masonite.request import Request
from masonite.controllers import Controller
from masoniteorm.collection import Collection
from masoniteorm.query import QueryBuilder

from app.Tag import Tag
from app.services.WorkspaceService import WorkspaceService


class TagsController(Controller):

    def index(self, view: View, workspaceService: WorkspaceService):
        return view.render("tags.index", {'workspace': workspaceService.workspace})

    def api_index(self, workspaceService: WorkspaceService):
        tags = QueryBuilder().on('sqlite').table("tags") \
            .where_in('paper_key', workspaceService.get_paper_keys()) \
            .group_by('tags.tag') \
            .select_raw('tags.tag, COUNT(tags.tag) as num_tags,  MIN(tags.id) as tag_id') \
            .order_by('num_tags', direction="DESC") \
            .get()

        return tags

    def api_show(self, request: Request, workspaceService: WorkspaceService):
        tag_name = Tag.find(request.param('tag_id')).tag

        paper_ids = QueryBuilder().on('sqlite').table("tags") \
            .where('tag', '=', tag_name) \
            .where_in('paper_key', workspaceService.get_paper_keys()) \
            .select('paper_key') \
            .get()
        paper_ids = [x['paper_key'] for x in paper_ids]

        items = QueryBuilder().on('zotero').table("items") \
            .right_join('deletedItems', 'items.itemID', '=', 'deletedItems.itemID', ) \
            .where_null('deletedItems.dateDeleted') \
            .join('itemData', 'items.itemID', '=', 'itemData.itemID') \
            .join('itemDataValues', 'itemData.valueID', '=', 'itemDataValues.valueID') \
            .where_in('items.key', paper_ids) \
            .where('itemData.fieldID', '=', ITEM_DATA_FIELD__TITLE) \
            .group_by('items.itemID') \
            .select_raw('items.itemID, items.key, itemDataValues.value as title') \
            .order_by('title', 'asc') \
            .get()

        return Collection(items).random(len(items)).serialize()

    def create(self, request: Request):
        tag = Tag.create({
            'paper_key': request.input('paper_key'),
            'tag': request.input('tag'),
            'user_id': request.user().id,
        })
        return {"status": "success", "model": tag.serialize()}

    def update(self, request: Request):
        tags = Tag.where('tag', '=', request.input('old_tag_value')).update({
            "tag": request.input('new_tag_value'),
        })
        return {"status": "success", "model": tags.serialize()}

    def delete(self, request: Request):
        Tag.where('id', request.param('id')).delete()
        return {"status": "success"}
