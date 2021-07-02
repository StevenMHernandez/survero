from masonite.view import View
from masonite.request import Request
from masonite.controllers import Controller
from masoniteorm.query import QueryBuilder

ITEM_DATA_FIELD__TITLE = 1
ITEM_TYPE__ATTACHMENT = 2
PRIMARY_COLLECTION_ID = 14


class AuthorsController(Controller):

    def index(self, view: View):
        return view.render("authors.index")

    def graph(self, view: View):
        return view.render("authors.graph")

    def show(self, view: View, request: Request):
        author = QueryBuilder().on('zotero').table("creators").where('creatorID', '=', request.param('creator_id')).first()
        return view.render("authors.show", {'author': author})

    def api_index(self):
        collections = QueryBuilder().on('zotero').table('collections') \
            .where('parentCollectionID', '=', PRIMARY_COLLECTION_ID)\
            .select('collectionID') \
            .get()
        collection_ids = [list(x.values())[0] for x in collections]

        authors = QueryBuilder().on('zotero').table("creators")\
            .join('itemCreators', 'creators.creatorID', '=', 'itemCreators.creatorID')\
            .join('items', 'items.itemID', '=', 'itemCreators.itemID')\
            .where('items.libraryID', '=', 1)\
            .right_join('deletedItems', 'items.itemID', '=', 'deletedItems.itemID', ) \
            .where_null('deletedItems.dateDeleted') \
            .join('itemData', 'items.itemID', '=', 'itemData.itemID') \
            .join('itemDataValues', 'itemData.valueID', '=', 'itemDataValues.valueID') \
            .join('collectionItems', 'items.itemID', '=', 'collectionItems.itemID')\
            .join('collections', 'collections.collectionID', '=', 'collectionItems.collectionID') \
            .where_in('collectionItems.collectionID', collection_ids)\
            .where('itemData.fieldID', '=', ITEM_DATA_FIELD__TITLE) \
            .where('items.itemTypeID', '!=', ITEM_TYPE__ATTACHMENT)\
            .group_by('creators.creatorID')\
            .select_raw('creators.creatorID, creators.firstName, creators.lastName, COUNT(DISTINCT items.key) as num_papers')\
            .order_by('title', 'asc')\
            .get()

        return authors

    def api_graph(self):
        collections = QueryBuilder().on('zotero').table('collections') \
            .where('parentCollectionID', '=', PRIMARY_COLLECTION_ID)\
            .select('collectionID') \
            .get()
        collection_ids = [list(x.values())[0] for x in collections]

        authors = QueryBuilder().on('zotero').table("creators")\
            .join('itemCreators', 'creators.creatorID', '=', 'itemCreators.creatorID')\
            .join('items', 'items.itemID', '=', 'itemCreators.itemID')\
            .where('items.libraryID', '=', 1)\
            .right_join('deletedItems', 'items.itemID', '=', 'deletedItems.itemID', ) \
            .where_null('deletedItems.dateDeleted') \
            .join('itemData', 'items.itemID', '=', 'itemData.itemID') \
            .join('itemDataValues', 'itemData.valueID', '=', 'itemDataValues.valueID') \
            .join('collectionItems', 'items.itemID', '=', 'collectionItems.itemID')\
            .join('collections', 'collections.collectionID', '=', 'collectionItems.collectionID') \
            .where_in('collectionItems.collectionID', collection_ids)\
            .where('itemData.fieldID', '=', ITEM_DATA_FIELD__TITLE) \
            .where('items.itemTypeID', '!=', ITEM_TYPE__ATTACHMENT)\
            .group_by('creators.creatorID')\
            .select_raw('creators.creatorID, creators.firstName, creators.lastName, COUNT(DISTINCT items.key) as num_papers, GROUP_CONCAT(DISTINCT items.key) as paper_keys')\
            .order_by('title', 'asc')\
            .get()

        authors = [a for a in authors if a['num_papers'] >= 1]
        authors = [a for a in authors if len(a['firstName']) > 1]

        authors_per_paper = {}
        for a in authors:
            author_value = {"id": a['creatorID'], "fullName": a['firstName'] + " " + a['lastName']}
            for p in a['paper_keys'].split(","):
                if p not in authors_per_paper:
                    authors_per_paper[p] = [author_value]
                else:
                    authors_per_paper[p].append(author_value)

        nodes = []
        for a in authors:
            nodes.append({
                "id": a['creatorID'],
                "name": f"{a['firstName']} {a['lastName']} ({a['num_papers']})"
            })
        links = []
        for p in authors_per_paper.keys():
            authors = authors_per_paper[p]
            if len(authors) > 1:
                for i in range(len(authors) - 1):
                    for j in range(i + 1, len(authors)):
                        links.append({
                            "source": authors[i]['id'],
                            "target": authors[j]['id'],
                        })

        return {'nodes': nodes, 'links': links}

    def api_show(self, request: Request):
        author = QueryBuilder().on('zotero').table("creators").where('creatorId', '=', request.param('creator_id')).first()

        papers = QueryBuilder().on('zotero').table("items") \
            .right_join('deletedItems', 'items.itemID', '=', 'deletedItems.itemID', ) \
            .where_null('deletedItems.dateDeleted') \
            .where('items.libraryID', '=', 1)\
            .join('itemData', 'items.itemID', '=', 'itemData.itemID') \
            .join('itemDataValues', 'itemData.valueID', '=', 'itemDataValues.valueID') \
            .join('collectionItems', 'items.itemID', '=', 'collectionItems.itemID')\
            .join('collections', 'collections.collectionID', '=', 'collectionItems.collectionID') \
            .join('itemCreators', 'items.itemID', '=', 'itemCreators.itemID')\
            .where('itemCreators.creatorID', '=', author['creatorID'])\
            .where('itemData.fieldID', '=', ITEM_DATA_FIELD__TITLE) \
            .where('itemTypeID', '!=', ITEM_TYPE__ATTACHMENT)\
            .group_by('items.itemID, collectionItems.collectionID')\
            .select_raw('items.itemID, items.key, itemDataValues.value as title, collections.collectionName') \
            .order_by('title', 'asc') \
            .get()

        papers_organized = {}
        for p in papers:
            if p['key'] not in papers_organized:
                papers_organized[p['key']] = p
                papers_organized[p['key']]['collections'] = [p['collectionName']]
                del papers_organized[p['key']]['collectionName']
            else:
                papers_organized[p['key']]['collections'].append(p['collectionName'])

        author['papers'] = papers_organized

        return author
