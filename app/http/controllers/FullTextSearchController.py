from masonite.view import View
from masonite.request import Request
from masonite.controllers import Controller
from masoniteorm.query import QueryBuilder
from masoniteorm.collection import Collection

ITEM_DATA_FIELD__TITLE = 1
ITEM_TYPE__ATTACHMENT = 2
PRIMARY_COLLECTION_ID = 14
CREATOR_TYPES__EDITOR = 10

class FullTextSearchController(Controller):

    def index(self, view: View, request: Request):
        return view.render("full_text_search.index")

    def api_index(self, request: Request):
        search_terms = request.query('query').split(" ")

        collections = QueryBuilder().on('zotero').table('collections') \
            .where('parentCollectionID', '=', PRIMARY_COLLECTION_ID)\
            .where_not_in('collectionId', [69, 65, 90, 74, 46, 73, 41, 14, 68, 97, 87, 61])\
            .select('collectionID') \
            .get()
        collection_ids = [list(x.values())[0] for x in collections]

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
            .where('itemData.fieldID', '=', ITEM_DATA_FIELD__TITLE) \
            .where('itemTypeID', '!=', ITEM_TYPE__ATTACHMENT)\
            .group_by('items.itemID')\
            .select_raw('items.itemID, items.key, itemDataValues.value as title, collections.collectionName, COUNT(itemAttachments.path) as num_attachments') \
            .order_by('title', 'asc') \
            .get()

        return items

    def api_alternatives(self, request: Request):
        search_terms = request.query('query').split(" ")

        alternatives = None
        for q in search_terms:
            items = QueryBuilder().on('zotero').table('fulltextWords')\
                .where_like('word', '%' + q + '%').get()

            if alternatives is None:
                alternatives = items
            else:
                alternatives += items

        return Collection([alt['word'] for alt in alternatives if alt['word'] not in search_terms]).unique()

