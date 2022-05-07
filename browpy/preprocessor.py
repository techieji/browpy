from html.parser import HTMLParser

class Preprocessor(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.final_text = ""
        self.level = 0

    def handle_starttag(self, tag, attrs):
        self.level += 1
        self.final_text += f'HTMLElement("{tag}", {dict(attrs)}, '

    def handle_data(self, data):
        if self.level:
            self.final_text += f'"{data}", '
        else:
            self.final_text += data

    def handle_endtag(self, _):
        self.level -= 1
        self.final_text += ')'
        if self.level:
            self.final_text += ', '

    def handle_startendtag(self, tag, attrs):
        self.final_text += f'HTMLElement("{tag}", {dict(attrs)})'
        if self.level:
            self.final_text += ', '

if __name__ == '__main__':
    import sys
    p = Preprocessor()
    with open(sys.argv[1]) as f:
        p.feed(f.read())
    with open(sys.argv[2], 'w') as f:
        print(p.final_text, file=f)
