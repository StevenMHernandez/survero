from masonite.view import View
from masonite.request import Request
from masonite.controllers import Controller
from masoniteorm.collection import Collection
from masoniteorm.query import QueryBuilder

from app.Tag import Tag


class TagsController(Controller):

    def index(self, view: View):
        return view.render("tags.index")

    def api_index(self):
        tags = QueryBuilder().on('sqlite').table("tags")\
            .group_by('tags.tag')\
            .select_raw('tags.tag, COUNT(tags.tag) as num_tags')\
            .order_by('num_tags', direction="DESC")\
            .get()

        return tags

    def create(self, request: Request):
        tag = Tag.create({
            'paper_key': request.input('paper_key'),
            'tag': request.input('tag'),
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
