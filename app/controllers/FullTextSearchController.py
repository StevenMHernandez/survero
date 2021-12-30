from masonite.views import View
from masonite.request import Request
from masonite.controllers import Controller
from masoniteorm.query import QueryBuilder
from masoniteorm.collection import Collection
from masonite.configuration import config

from app.services.WorkspaceService import WorkspaceService


class FullTextSearchController(Controller):

    def index(self, view: View, workspaceService: WorkspaceService):
        return view.render("full_text_search.index", {'workspace': workspaceService.workspace})

    def api_index(self, request: Request, workspaceService: WorkspaceService):
        search_terms = request.input('query').split(" ")

        collection_ids = workspaceService.get_collection_ids()

        items = QueryBuilder().on('zotero').table('fulltextWords')\
            .where_in('word', search_terms)\
            .join('fulltextItemWords', 'fulltextWords.wordID', '=', 'fulltextItemWords.wordID')\
            .join('items', 'fulltextItemWords.itemID', '=', 'items.itemID')\
            .join('itemAttachments', 'itemAttachments.itemID', '=', 'items.itemID')\
            .get()
        item_ids = [it['parentItemID'] for it in items]

        items = QueryBuilder().on('zotero').table("items") \
            .where_in('items.itemID', item_ids) \
            .right_join('deletedItems', 'items.itemID', '=', 'deletedItems.itemID', ) \
            .where_null('deletedItems.dateDeleted') \
            .join('itemData', 'items.itemID', '=', 'itemData.itemID') \
            .join('itemDataValues', 'itemData.valueID', '=', 'itemDataValues.valueID') \
            .join('collectionItems', 'items.itemID', '=', 'collectionItems.itemID')\
            .join('collections', 'collections.collectionID', '=', 'collectionItems.collectionID') \
            .join('itemAttachments', 'itemAttachments.parentItemId', '=', 'items.itemID')\
            .where('itemAttachments.contentType', '=', 'application/pdf')\
            .where_in('collectionItems.collectionID', collection_ids)\
            .where('itemData.fieldID', '=', workspaceService.ITEM_DATA_FIELD__TITLE) \
            .where('itemTypeID', '!=', workspaceService.ITEM_TYPE__ATTACHMENT)\
            .group_by('items.itemID')\
            .select_raw('items.itemID, items.key, itemDataValues.value as title, collections.collectionName, COUNT(itemAttachments.path) as num_attachments') \
            .order_by('title', 'asc') \
            .get()

        tags = QueryBuilder().on('sqlite').table('tags')\
            .where_in('paper_key', [it['key'] for it in items])\
            .select_raw('paper_key, substr(tag, 0, instr(tag, \':\')) as tag_group')\
            .get()

        def add_additional_fields(it):
            it['tag_groups'] = Collection([t['tag_group'] for t in tags if t['paper_key'] == it['key'] and t['tag_group'] != '']).unique().serialize()
            return it

        items = [add_additional_fields(it) for it in items]

        return items

    def api_alternatives(self, request: Request):
        search_terms = request.input('query').split(" ")

        alternatives = None
        for q in search_terms:
            items = QueryBuilder().on('zotero').table('fulltextWords')\
                .where_like('word', '%' + q + '%').get()

            if alternatives is None:
                alternatives = items
            else:
                alternatives += items

        return Collection([alt['word'] for alt in alternatives if alt['word'] not in search_terms]).unique()

