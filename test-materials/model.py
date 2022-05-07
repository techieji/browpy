from browpy import set_root, Element
from browpy.html import button
from browpy.meta import title, favicon

class Counter(Element):
    def __init__(self, attrs):
        super().__init__(attrs, 'Counter')
        self.state = 0

    def render(self):
        return <button>{self.state}</button> # Turns into html.button(self.state)

    def on_click(self, event):
        self.state += 1

title('Browpy demo')
favicon('browpy.ico')
set_root(<Counter>)
