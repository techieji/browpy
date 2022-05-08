from html.parser import HTMLParser

class Preprocessor(HTMLParser):
    TAGS = ['A', 'ABBR', 'ACRONYM', 'ADDRESS', 'APPLET', 'AREA', 'B', 'BASE', 'BASEFONT', 'BDO', 'BIG', 'BLOCKQUOTE', 'BODY', 'BR', 'BUTTON', 'CAPTION', 'CENTER', 'CITE', 'CODE', 'COL', 'COLGROUP', 'DD', 'DEL', 'DFN', 'DIR', 'DIV', 'DL', 'DT', 'EM', 'FIELDSET', 'FONT', 'FORM', 'FRAME', 'FRAMESET', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'HEAD', 'HR', 'HTML', 'I', 'IFRAME', 'IMG', 'INPUT', 'INS', 'ISINDEX', 'KBD', 'LABEL', 'LEGEND', 'LI', 'LINK', 'MAP', 'MENU', 'META', 'NOFRAMES', 'NOSCRIPT', 'OBJECT', 'OL', 'OPTGROUP', 'OPTION', 'P', 'PARAM', 'PRE', 'Q', 'S', 'SAMP', 'SCRIPT', 'SELECT', 'SMALL', 'SPAN', 'STRIKE', 'STRONG', 'STYLE', 'SUB', 'SUP', 'SVG', 'TABLE', 'TBODY', 'TD', 'TEXTAREA', 'TFOOT', 'TH', 'THEAD', 'TITLE', 'TR', 'TT', 'U', 'UL', 'VAR', 'ARTICLE', 'ASIDE', 'AUDIO', 'BDI', 'CANVAS', 'COMMAND', 'DATA', 'DATALIST', 'EMBED', 'FIGCAPTION', 'FIGURE', 'FOOTER', 'HEADER', 'KEYGEN', 'MAIN', 'MARK', 'MATH', 'METER', 'NAV', 'OUTPUT', 'PROGRESS', 'RB', 'RP', 'RT', 'RTC', 'RUBY', 'SECTION', 'SOURCE', 'TEMPLATE', 'TIME', 'TRACK', 'VIDEO', 'WBR', 'DETAILS', 'DIALOG', 'MENUITEM', 'PICTURE', 'SUMMARY']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.final_text = ""
        self.level = 0

    def handle_starttag(self, _, attrs):
        tag = self.get_actual_tag()
        self.level += 1
        self.final_text += f'HTMLElement(f"{tag}", {dict(attrs)}, '

    def handle_data(self, data):
        if self.level:
            self.final_text += f'f"{data}", '
        else:
            self.final_text += data

    def handle_endtag(self, _):
        self.level -= 1
        self.final_text += ')'
        if self.level:
            self.final_text += ', '

    def handle_startendtag(self, _, attrs):
        tag = self.get_actual_tag()
        if type(self).is_html_tag(tag):
            self.final_text += f'make_element(f"{tag}", {dict(attrs)})'
        else:
            self.final_text += f'{tag}({dict(attrs)})'
        if self.level:
            self.final_text += ', '

    def get_actual_tag(self):
        return self.get_starttag_text().replace('<', '').replace('>', '').replace('/', '').strip()

    @classmethod
    def is_html_tag(klass, tag):
        return tag.upper() in klass.TAGS

if __name__ == '__main__':
    import sys
    p = Preprocessor()
    with open(sys.argv[1]) as f:
        p.feed(f.read())
    with open(sys.argv[2], 'w') as f:
        print(p.final_text, file=f)
