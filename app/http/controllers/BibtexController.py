import requests

from masonite.view import View
from masonite.request import Request
from masonite.controllers import Controller
from masoniteorm.query import QueryBuilder
from masonite.helpers import config

from app.BibtexEntry import BibtexEntry
from app.services.WorkspaceService import WorkspaceService


class BibtexController(Controller):

    def api_get(self, request: Request):
        bibtex = BibtexEntry.where({'paper_key': request.param('paper_key')}).first()
        if bibtex:
            return {
                'status': 'success',
                'model': bibtex.serialize(),
            }
        else:
            return {
                'status': 'bibtex_entry_does_not_exist',
            }

    def api_set(self, request: Request):
        bibtex = BibtexEntry.where({'paper_key': request.param('paper_key')}).first()

        if bibtex:
            BibtexEntry.where('paper_key', '=', request.input('paper_key')).update({
                'bibtex': request.input('bibtex'),
            })
        else:
            BibtexEntry.create({
                'paper_key': request.input('paper_key'),
                'bibtex': request.input('bibtex'),
            })

        bibtex = BibtexEntry.where({'paper_key': request.param('paper_key')}).first()

        return {"status": "success", "model": bibtex.serialize()}

    def api_generate(self, request: Request, workspaceServices: WorkspaceService):
        paper = workspaceServices.get_paper(request.param('paper_key'))

        doi = [x['value'] for x in paper['metadata'] if x['fieldName'] == 'DOI']

        if len(doi) == 0:
            return {
                'status': 'doi_not_found',
                'message': 'Notice: A DOI was not found in Zotero for this paper.'
            }

        doi = doi[0]

        crossref_user_email = env("CROSSREF_USER_EMAIL", None)
        if not crossref_user_email:
            return {
                'status': 'crossref_user_email_not_found',
                'message': 'Notice: Please set `CROSSREF_USER_EMAIL` in `.env`. Your email will be sent in the `User-Agent` to `https://api.crossref.org` to generate Bibtex records.'
            }

        response = requests.get(
            f"https://api.crossref.org/works/{doi}/transform/application/x-bibtex",
            headers={
                "Accept": "text/bibliography; style=bibtex",
                "User-Agent": f"Survero/0.0 (mailto:{crossref_user_email})",
            }
        )

        return {
            'status': 'success',
            'bibtex': requests.utils.unquote(response.text),
        }
