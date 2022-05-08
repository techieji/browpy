from browser import document
import browser.html as bry_html

class HTMLElement:
    def __init__(self, name, attrs, *subelements):
        self.name = name
        self.attrs = attrs
        self.subelements = subelements
        self.elem = None
        self.bindings = {}

    def update(self, upper):
        new_elem = self.render()
        if type(new_elem) is HTMLElement:
            new_elem.update(upper)
        if self.elem is not None and self.elem.parentNode is not None:    # 2nd condition is if element isn't linked to document?
            self.elem.parentNode.replaceChild(new_elem, self.elem)
        else:
            upper <= new_elem
        self.elem = new_elem

    def replace_with(self, new_elem):
        self.elem.parentNode.replaceChild(new_elem.elem, self.elem)

    def render(self):
        s = ""
        for x in self.subelements:
            if type(x) is HTMLElement:
                s += x.render()
            else:
                s += x
        res = getattr(bry_html, self.name.upper())(s, **self.attrs)
        for attr, fn in self.bindings.items():
            print(attr, fn)
            res.bind(attr, fn)
        return res

    def set_text(self, *new_content):
        self.subelements = new_content

    def bind_lazy(self, event_name, fn):
        self.bindings[event_name] = fn

    def bind(self, event_name, fn):
        self.elem.bind(event_name, fn)

class Element:
    def __init__(self, attrs):
        self.attrs = attrs
        self.name = type(self).__name__
        self.elem = None

    def update(self, upper):
        if self.elem is None:
            self.elem = self.render()
            self.elem.update(upper)
        else:
            new_elem = self.render()
            new_elem.elem = new_elem.render()
            self.elem.replace_with(new_elem)
            self.elem = new_elem
        for attr in dir(self):    # Avoid rebinding methods every update?
            if attr.startswith('on_'):
                print(attr[3:], getattr(self, attr))
                self.elem.bind(attr[3:], getattr(self, attr))

    def render(self):
        raise NotImplementedError()

def title(name):
    document.select('head')[0] <= bry_html.TITLE(name)

def favicon(filen):
    print('Favicons not supported yet.')

def set_root(elem):
    elem.update(document)
