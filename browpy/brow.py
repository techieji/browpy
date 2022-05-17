from browser import document
import browser.html as bry_html

_attrdict = type('AttrDict', (dict,), {'__getitem__': dict.get, '__setitem__': dict.__setattr__})

class HTMLElement:
    def __init__(self, name, attrs, *subelements):
        self.name = name
        self.attrs = _attrdict(attrs)
        self.subelements = subelements
        self.elem = None
        self.upper = None

    def set_subordinates(self):
        for x in self.subelements:
            if type(x) is HTMLElement:
                x.upper = self.elem

    def update(self, upper=None, old=None):
        upper = self.upper if upper is None else upper
        if type(upper) is HTMLElement:
            upper = upper.elem
        # new_elem = self.render()
        new_elem = getattr(bry_html, self.name.upper())(**self.attrs)
        if self.elem is not None and self.elem.parentNode is not None:    # 2nd condition is if element isn't linked to document?
            self.elem.parentNode.replaceChild(new_elem, self.elem if old is None else old)
        else:
            upper <= new_elem
        if old is not None and old.elem is not None and old.elem.parentNode is not None:
            old.elem.parentNode.removeChild(old.elem)
        self.elem = new_elem
        self.set_subordinates()
        for attr, v in self.attrs.items():
            if attr.startswith('on_'):
                self.elem.bind(attr[3:], v)
        for x in self.subelements:
            if type(x) is HTMLElement:
                x.update()
            elif type(x) is str:
                self.elem <= x

    def replace_with(self, new_elem):
        self.elem.parentNode.replaceChild(new_elem.elem, self.elem)

    def render(self):
        s = ""
        for x in self.subelements:
            if type(x) is HTMLElement:
                s += x.render()
            elif issubclass(type(x), Element):
                s += x.render().render()
            else:
                s += x
        return getattr(bry_html, self.name.upper())(s, **self.attrs)

    def set_text(self, *new_content):
        self.subelements = new_content

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
            new_elem.update(upper, self.elem)
            # new_elem.elem = new_elem.render()
            # self.elem.replace_with(new_elem)
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
