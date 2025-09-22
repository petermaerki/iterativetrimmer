# Refactoring iterativetrimmer

Old version from positron website: `static_v1`.

This webpage is ment to be deployed as github webpage https://petermaerki.github.io/iterativetrimmer.
It is a static page.

Python implementation in `iterativetrimmer.py`.

Inner workings

`index.html`
 * loads python WASM from https://pyscript.net
 * calls `index.py`
   * which imports `iterativetrimmer.py`
   * which calls `load_readme()`
     * which loads `README.md` and converts it ot html
     * set the html element with id `readme`

 * loads button `do_calculate`
   * which calls `iterativetrimmer.do_calculate()`
     * which sets the html elements with id `loesung_sollwert`, `loesung_a`, ...


## https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site

## Pyscript

### This page is base on

https://pyscript.com/@examples/pyscript-jokes/
https://pyscript.com/@ntoll/piratical

### Links for Pyscript and Micropython WASM

* https://pyscript.net/
* https://pyscript.net/main.py
* https://github.com/pyscript/pyscript.net
* https://pyscript.com/@examples
* https://docs.pyscript.net/2025.8.1/user-guide/first-steps/
