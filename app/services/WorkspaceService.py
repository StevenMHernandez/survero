from masonite.request import Request
from masoniteorm.query import QueryBuilder
from masoniteorm.collection import Collection

from app.Workspace import Workspace
from app.Note import Note
from app.Tag import Tag
from app.Screenshot import Screenshot

ITEM_DATA_FIELD__TITLE = 1
ITEM_TYPE__ATTACHMENT = 2
CREATOR_TYPES__EDITOR = 10


class WorkspaceService:
    def __init__(self, request: Request):
        self.request = request
        self.workspace = QueryBuilder().on('zotero').table('collections').where('key', request.param('workpace_key')).get()[0]

    def get_collection_ids(self):
        collections = QueryBuilder().on('zotero').table('collections') \
            .where('parentCollectionID', '=', self.workspace['collectionID']) \
            .select('collectionID') \
            .get()
        collection_ids = [list(x.values())[0] for x in collections]
        return [self.workspace['collectionID']] + collection_ids

    def get_paper_keys(self):
        collection_ids = self.get_collection_ids()

        items = QueryBuilder().on('zotero').table("items") \
            .right_join('deletedItems', 'items.itemID', '=', 'deletedItems.itemID', ) \
            .where_null('deletedItems.dateDeleted') \
            .join('itemData', 'items.itemID', '=', 'itemData.itemID') \
            .join('collectionItems', 'items.itemID', '=', 'collectionItems.itemID') \
            .where_in('collectionItems.collectionID', collection_ids) \
            .group_by('items.itemID, collectionItems.collectionID') \
            .select_raw('items.itemID, items.key') \
            .order_by('title', 'asc') \
            .get()
        return [it['key'] for it in items]

    def get_papers(self):
        collection_ids = self.get_collection_ids()

        items = QueryBuilder().on('zotero').table("items") \
            .right_join('deletedItems', 'items.itemID', '=', 'deletedItems.itemID', ) \
            .where_null('deletedItems.dateDeleted') \
            .join('itemData', 'items.itemID', '=', 'itemData.itemID') \
            .join('itemDataValues', 'itemData.valueID', '=', 'itemDataValues.valueID') \
            .join('collectionItems', 'items.itemID', '=', 'collectionItems.itemID') \
            .join('collections', 'collections.collectionID', '=', 'collectionItems.collectionID') \
            .join('itemAttachments', 'itemAttachments.parentItemId', '=', 'items.itemID') \
            .where('itemAttachments.contentType', '=', 'application/pdf') \
            .where_in('collectionItems.collectionID', collection_ids) \
            .where('itemData.fieldID', '=', ITEM_DATA_FIELD__TITLE) \
            .where('itemTypeID', '!=', ITEM_TYPE__ATTACHMENT) \
            .group_by('items.itemID, collectionItems.collectionID') \
            .select_raw(
            'items.itemID, items.key, itemDataValues.value as title, collections.collectionName, COUNT(itemAttachments.path) as num_attachments') \
            .order_by('title', 'asc') \
            .get()
        return items

    def get_paper(self, paper_key):
        item = QueryBuilder().on('zotero').table("items").where('key', '=', paper_key) \
            .join('collectionItems', 'items.itemID', '=', 'collectionItems.itemID') \
            .join('collections', 'collections.collectionID', '=', 'collectionItems.collectionID') \
            .first()

        item['collections'] = QueryBuilder().on('zotero').table('collections')\
            .join('collectionItems', 'collections.collectionID', '=', 'collectionItems.collectionID')\
            .where('collectionItems.itemID', '=', item['itemID'])\
            .where_in('collectionId', self.get_collection_ids())\
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

        item['authors'] = QueryBuilder().on('zotero') \
            .table("creators") \
            .join('itemCreators', 'creators.creatorID', '=', 'itemCreators.creatorID') \
            .where_not_in('itemCreators.creatorTypeID', [CREATOR_TYPES__EDITOR])\
            .where('itemCreators.itemID', '=', item['itemID'])\
            .order_by('orderIndex')\
            .get()

        item['title'] = [x['value'] for x in item['metadata'] if x['fieldName'] == 'title'][0]

        item['screenshots'] = Screenshot.where('paper_key', '=', paper_key).with_('user').get().serialize()

        item['tags'] = Tag.where('paper_key', '=', paper_key).with_('user').get().serialize()

        item['notes'] = Note.where('paper_key', '=', paper_key).with_('user').get().serialize()

        return item
