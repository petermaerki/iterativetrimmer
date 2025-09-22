import pathlib
import markdown

from pyscript.web import page

readme_text = pathlib.Path("README.md").read_text()

page["div#readme"].innerHTML = markdown.markdown(readme_text)
