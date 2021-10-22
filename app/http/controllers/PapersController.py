from masonite.view import View
from masonite.request import Request
from masonite.controllers import Controller
from masoniteorm.query import QueryBuilder
from masonite.helpers import config

from app.Workspace import Workspace
from app.Tag import Tag
from app.Note import Note
from app.Screenshot import Screenshot
from app.services.WorkspaceService import WorkspaceService


class PapersController(Controller):
    def index(self, view: View, workspaceService: WorkspaceService):
        return view.render("papers.index", {'workspace': workspaceService.workspace})

    def show(self, view: View, request: Request, workspaceService: WorkspaceService):
        item = QueryBuilder().on('zotero').table("items").where('key', '=', request.param('key')).first()
        return view.render("papers.show", {'item': item, 'workspace': workspaceService.workspace})

    def api_index(self, request: Request, workspaceService: WorkspaceService):
        items = workspaceService.get_papers()

        tags = QueryBuilder().on('sqlite').table('tags').group_by('paper_key')
        if request.query('tag_group', False):
            tags = tags.where_like('tag', request.query('tag_group') + ': %')
        tags = tags.select_raw('paper_key, COUNT(paper_key) as num') #.get()
        tags = tags.get()
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
            if request.query('tag_group', False):
                r['needs_review'] = not (r['num_tags'])
            else:
                r['needs_review'] = not (r['num_tags'] or r['num_screenshots'] or r['num_notes'])
            return r

        items = [add_additional_fields(r) for r in items]

        return items

    def api_show(self, request: Request, workspaceServices: WorkspaceService):
        return workspaceServices.get_paper(request.param('key'))
