"""
Code Example Extension for Python Markdown
=========================================
Markdown extension which allows to insert code examples as HTML escaped code and rendered code.
It extends Fenced Code Blocks
See <https://Python-Markdown.github.io/extensions/fenced_code_blocks>
for documentation.
Base extension code Copyright 2007-2008 [Waylan Limberg](http://achinghead.com/).
All changes Copyright 2008-2014 The Python Markdown Project
License: [BSD](http://www.opensource.org/licenses/bsd-license.php)
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import markdown
from markdown import Extension
from markdown.preprocessors import Preprocessor
from markdown.extensions.codehilite import CodeHilite, CodeHiliteExtension
import re

# Global vars
FENCED_BLOCK_RE = re.compile( \
    r'(?P<fence>^(?:\[{2}code_example))[ ]*(\{?\.?(?P<lang>[a-zA-Z0-9_+-]*)\}?)?[ ]*\n(?P<code>.*?)(?<=\n)(?P<end>(?:code_example\]{2}))[ ]*$',
    re.MULTILINE|re.DOTALL
    )
CODE_WRAP = '<pre><code%s>%s</code></pre>'
LANG_TAG = ' class="%s"'
RESULT = '''
%s<div class="code_example"><div class="bd-example">%s</div>%s</div>%s
'''

class CodeExampleExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        """ Add CodeExampleBlockPreprocessor to the Markdown instance. """
        md.registerExtension(self)

        md.preprocessors.add('ez_code_example',
                                 CodeExampleBlockPreprocessor(md),
                                 ">normalize_whitespace")


class CodeExampleBlockPreprocessor(Preprocessor):

    def __init__(self, md):
        super(CodeExampleBlockPreprocessor, self).__init__(md)

        self.checked_for_codehilite = False
        self.codehilite_conf = {}

    def run(self, lines):
        """ Match and store Fenced Code Blocks in the HtmlStash. """

        # Check for code hilite extension
        if not self.checked_for_codehilite:
            for ext in self.markdown.registeredExtensions:
                if isinstance(ext, CodeHiliteExtension):
                    self.codehilite_conf = ext.config
                    break

            self.checked_for_codehilite = True

        text = "\n".join(lines)
        while 1:
            m = FENCED_BLOCK_RE.search(text)
            if m:
                lang = ''
                if m.group('lang'):
                    lang = LANG_TAG % m.group('lang')

                # If config is not empty, then the codehighlite extension
                # is enabled, so we call it to highlite the code
                if self.codehilite_conf:
                    highliter = CodeHilite(m.group('code'),
                            linenums=self.codehilite_conf['linenums'][0],
                            guess_lang=self.codehilite_conf['guess_lang'][0],
                            css_class=self.codehilite_conf['css_class'][0],
                            style=self.codehilite_conf['pygments_style'][0],
                            lang=(m.group('lang') or None),
                            noclasses=self.codehilite_conf['noclasses'][0])

                    code = highliter.hilite()
                else:
                    code = CODE_WRAP % (lang, self._escape(m.group('code')))

                placeholder = self.markdown.htmlStash.store(code, safe=True)
                text = '%s\n<div class="ez-code-example">%s</div> \n %s\n%s' % (text[:m.start()], m.group('code'), placeholder, text[m.end():])
            else:
                break
        return text.split("\n")

    def _escape(self, txt):
        """ basic html escaping """
        txt = txt.replace('&', '&amp;')
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt = txt.replace('"', '&quot;')
        return txt


def makeExtension(configs=None):
    return CodeExampleExtension()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
