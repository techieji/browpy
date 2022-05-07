from browser import document
import browser.html as bry_html

class HTMLElement:
    def __init__(self, name, attrs, *subelements):
        self.name = name
        self.attrs = attrs
        self.subelements = subelements
        self.elem = None

    def update(self, upper):
        self.elem = self.render()
        upper <= self.elem

    def render(self):
        s = self.subelements[0]  # It kills me to do this
        for x in self.subelements[1:]:
            s += x
        return getattr(bry_html, self.name.upper())(s)

class Element(HTMLElement):
    def __init__(self, attrs, name):
        super().__init__(name, attrs)

    def render(self):
        raise NotImplementedError()
