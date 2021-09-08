from masonite.view import View
from masonite.request import Request
from masonite.controllers import Controller
from masoniteorm.query import QueryBuilder

ITEM_DATA_FIELD__TITLE = 1
ITEM_TYPE__ATTACHMENT = 2
PRIMARY_COLLECTION_ID = 14
CREATOR_TYPES__EDITOR = 10
ITEM_DATA_FIELD__PUBLICATION_TITLE = 37


class PublicationsController(Controller):

    def index(self, view: View):
        return view.render("publications.index")

    def graph(self, view: View):
        return view.render("publications.graph")

    def api_index(self):

        collections = QueryBuilder().on('zotero').table('collections') \
            .where('parentCollectionID', '=', PRIMARY_COLLECTION_ID)\
            .where_not_in('collectionId', [69, 65, 90, 74, 46, 73, 41, 14, 68, 97, 87, 61])\
            .select('collectionID') \
            .get()
        collection_ids = [list(x.values())[0] for x in collections]

        publications = QueryBuilder().on('zotero').table('itemDataValues') \
            .join('itemData', 'itemDataValues.valueID', '=', 'itemData.valueID') \
            .join('items', 'itemData.itemId', '=', 'items.itemID') \
            .join('collectionItems', 'items.itemID', '=', 'collectionItems.itemID') \
            .join('collections', 'collections.collectionID', '=', 'collectionItems.collectionID') \
            .where_in('collectionItems.collectionID', collection_ids)\
            .where('itemData.fieldID', '=', ITEM_DATA_FIELD__PUBLICATION_TITLE) \
            .group_by('value') \
            .select_raw('value as publicationTitle, COUNT(value) as count') \
            .get()

        papers = QueryBuilder().on('zotero') \
            .statement("""
        SELECT items.key, IDV1.value as publication, IDV2.value as title, collectionItems.collectionID FROM items
        LEFT JOIN deletedItems on items.itemID = deletedItems.itemID
        JOIN collectionItems on items.itemID = collectionItems.itemID
        JOIN collections on collections.collectionID = collectionItems.collectionID
        JOIN itemData as ID1 on items.itemID = ID1.itemID
        JOIN itemData as ID2 on items.itemID = ID2.itemID
        JOIN itemDataValues AS IDV1 on (ID1.valueID = IDV1.valueId and ID1.fieldID = ?)
        JOIN itemDataValues AS IDV2 on (ID2.valueID = IDV2.valueId and ID2.fieldID = ?)
        WHERE deletedItems.dateDeleted IS NULL
        ORDER BY IDV1.value;
        """, [ITEM_DATA_FIELD__PUBLICATION_TITLE, ITEM_DATA_FIELD__TITLE])

        papers = [p for p in papers if p['collectionID'] in collection_ids]

        return {'publications': publications, 'papers': papers}