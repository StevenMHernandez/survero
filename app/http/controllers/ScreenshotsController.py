from masonite import Upload
from masonite.view import View
from masonite.request import Request
from masonite.controllers import Controller

from app.Screenshot import Screenshot


class ScreenshotsController(Controller):

    def index(self, view: View, request: Request):
        return view.render("screenshots.index")

    def create(self, upload: Upload, request: Request):
        file_name = upload.driver('disk').store(request.input('upload'))
        screenshot = Screenshot.create({
            'paper_key': request.input('paper_key'),
            'file_name': file_name
        })
        return {"status": "success", "model": screenshot.serialize()}

    def api_index(self):
        screenshots = Screenshot.all()
        return screenshots.random(len(screenshots)).serialize()
