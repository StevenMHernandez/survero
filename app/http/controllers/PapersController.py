from masonite.view import View
from masonite.request import Request
from masonite.controllers import Controller
from masoniteorm.query import QueryBuilder

from app.Tag import Tag
from app.Note import Note
from app.Screenshot import Screenshot

ITEM_DATA_FIELD__TITLE = 1
ITEM_TYPE__ATTACHMENT = 2
PRIMARY_COLLECTION_ID = 14

class PapersController(Controller):

    def index(self, view: View, request: Request):
        return view.render("papers.index")

    def show(self, view: View, request: Request):
        item = QueryBuilder().on('zotero').table("items").where('key', '=', request.param('key')).first()
        return view.render("papers.show", {'item': item})

    def api_index(self, view: View, request: Request):
        collections = QueryBuilder().on('zotero').table('collections') \
            .where('parentCollectionID', '=', PRIMARY_COLLECTION_ID)\
            .where_not_in('collectionId', [69, 65, 90, 74, 46, 73, 41, 14, 68, 97, 87])\
            .select('collectionID') \
            .get()
        collection_ids = [list(x.values())[0] for x in collections]

        items = QueryBuilder().on('zotero').table("items") \
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
            .group_by('items.itemID, collectionItems.collectionID')\
            .select_raw('items.itemID, items.key, itemDataValues.value as title, collections.collectionName, COUNT(itemAttachments.path) as num_attachments') \
            .order_by('title', 'asc') \
            .get()

        tags = QueryBuilder().on('sqlite').table('tags').group_by('paper_key') \
            .select_raw('paper_key, COUNT(paper_key) as num').get()
        tags = {r['paper_key']: r['num'] for r in tags}
        screenshots = QueryBuilder().on('sqlite').table('screenshots').group_by('paper_key') \
            .select_raw('paper_key, COUNT(paper_key) as num').get()
        screenshots = {r['paper_key']: r['num'] for r in screenshots}
        notes = QueryBuilder().on('sqlite').table('notes').group_by('paper_key') \
            .select_raw('paper_key, COUNT(paper_key) as num').get()
        notes = {r['paper_key']: r['num'] for r in notes}

        def add_additional_fields(r):
            r['num_tags'] = tags.get(r['key'], 0)
            r['num_screenshots'] = screenshots.get(r['key'], 0)
            r['num_notes'] = notes.get(r['key'], 0)
            r['needs_review'] = not (r['num_tags'] or r['num_screenshots'] or r['num_notes'])
            return r

        items = [add_additional_fields(r) for r in items]

        return items

    def api_show(self, view: View, request: Request):
        item = QueryBuilder().on('zotero').table("items").where('key', '=', request.param('key')) \
            .join('collectionItems', 'items.itemID', '=', 'collectionItems.itemID') \
            .join('collections', 'collections.collectionID', '=', 'collectionItems.collectionID') \
            .first()

        item['collections'] = QueryBuilder().on('zotero').table('collections')\
            .join('collectionItems', 'collections.collectionID', '=', 'collectionItems.collectionID')\
            .where('collectionItems.itemID', '=', item['itemID'])\
            .where('parentCollectionID', '=', PRIMARY_COLLECTION_ID)\
            .all()

        item['attachments'] = QueryBuilder().on('zotero') \
            .table("itemAttachments").where('parentItemID', '=', item['itemID']) \
            .where('contentType', '=', 'application/pdf') \
            .join('items', 'itemAttachments.itemID', '=', 'items.itemID') \
            .select('itemAttachments.path, items.key') \
            .all()

        item['metadata'] = QueryBuilder().on('zotero') \
            .table("itemData").where('itemID', '=', item['itemID']) \
            .join('fields', 'itemData.fieldID', '=', 'fields.fieldID') \
            .join('itemDataValues', 'itemData.valueID', '=', 'itemDataValues.valueID') \
            .get()

        item['title'] = [x['value'] for x in item['metadata'] if x['fieldName'] == 'title'][0]

        item['screenshots'] = Screenshot.where('paper_key', '=', request.param('key')).get().serialize()

        item['tags'] = Tag.where('paper_key', '=', request.param('key')).get().serialize()

        item['notes'] = Note.where('paper_key', '=', request.param('key')).get().serialize()

        return item
