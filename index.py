from pyscript.web import page

from iterativetrimmer import IterativeTrimmer

def do_calculate(e):
    resistance_text, = page["input#resistance"].value
    resistance_Ohm = float(resistance_text)

    trimmer = IterativeTrimmer(resistance_Ohm)

    page["div#loesung_sollwert"].innerHTML = trimmer.sollwert
    page["b#loesung_a"].innerHTML = trimmer.loesung_a
    page["b#loesung_b"].innerHTML = trimmer.loesung_b
    page["b#loesung_c"].innerHTML = trimmer.loesung_c
    page["b#loesung_d"].innerHTML = trimmer.loesung_d


def load_readme():
    if len(page["div#readme"].innerHTML) > 100:
        return

    import pathlib
    import markdown

    readme_md = pathlib.Path("README.md").read_text()

    page["div#readme"].innerHTML = markdown.markdown(readme_md)

load_readme()
