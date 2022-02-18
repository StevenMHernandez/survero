from masonite.view import View
from masonite.request import Request
from masonite.controllers import Controller
from masoniteorm.query import QueryBuilder
from masonite.helpers import config

from app.services.WorkspaceService import WorkspaceService


class PublicationsController(Controller):
    def index(self, view: View, workspaceService: WorkspaceService):
        return view.render("publications.index", {'workspace': workspaceService.workspace})

    def api_index(self, workspaceService: WorkspaceService):
        collection_ids = workspaceService.get_collection_ids()

        publications = QueryBuilder().on('zotero').table('itemDataValues') \
            .join('itemData', 'itemDataValues.valueID', '=', 'itemData.valueID') \
            .join('items', 'itemData.itemId', '=', 'items.itemID') \
            .join('collectionItems', 'items.itemID', '=', 'collectionItems.itemID') \
            .join('collections', 'collections.collectionID', '=', 'collectionItems.collectionID') \
            .where_in('collectionItems.collectionID', collection_ids) \
            .where_in('itemData.fieldID', [
                workspaceService.ITEM_DATA_FIELD__PUBLICATION_TITLE,
                workspaceService.ITEM_DATA_FIELD__CONFERENCE_NAME,
            ]) \
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
        JOIN itemDataValues AS IDV1 on (ID1.valueID = IDV1.valueId and ID1.fieldID IN (?,?))
        JOIN itemDataValues AS IDV2 on (ID2.valueID = IDV2.valueId and ID2.fieldID = ?)
        WHERE deletedItems.dateDeleted IS NULL
        ORDER BY IDV1.value;
        """, [
            workspaceService.ITEM_DATA_FIELD__PUBLICATION_TITLE,
            workspaceService.ITEM_DATA_FIELD__CONFERENCE_NAME,
            workspaceService.ITEM_DATA_FIELD__TITLE
        ])

        papers = [p for p in papers if p['collectionID'] in collection_ids]

        return {'publications': publications, 'papers': papers}
