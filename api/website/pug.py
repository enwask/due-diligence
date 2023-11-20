from fastapi import HTTPException
from ninjadog import render


# Class for rendering pug templates and serving them as html
class PugRenderer:
    def __init__(self, path: str):
        self.path = path

    def render(self, template: str, context: dict[str, any], pretty: bool = True) -> str:
        return render("", f"{self.path}/{template}", context, pretty=pretty, with_jinja=True)

    def response(self, template: str, context: dict[str, any], pretty: bool = True) -> str:
        try:
            return self.render(template, context, pretty=pretty)
        except Exception as e:
            raise HTTPException(status_code=404, detail="We couldn't find the requested page.") from e
