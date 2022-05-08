from browpy import set_root, Element, title, favicon, HTMLElement, document

class Counter(Element):
    def __init__(self, attrs):
        super().__init__(attrs)
        self.state = 0

    def render(self):
        return <button>{self.state}</button>

    def on_click(self, event):
        self.state += 1
        self.update(document)

title('Browpy demo')
favicon('browpy.ico')
set_root(<Counter/>)
