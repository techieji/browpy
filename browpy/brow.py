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

    @staticmethod
    def remove_node(old):
        try:
            old.elem.parentNode.removeChild(old.elem)
        except AttributeError:
            pass

    def _update_node(self, new_elem, upper):
        try:
            self.elem.parentNode.replaceChild(new_elem, self.elem if old is None else old)
        except AttributeError:
            (self.upper if upper is None else upper).attach(new_elem)

    def bind_attrs(self):
        for attr, v in self.attrs.items():
            if attr.startswith('on_'):
                self.elem.bind(attr[3:], v)

    def update(self, upper=None, old=None):
        new_elem = getattr(bry_html, self.name.upper())(**self.attrs)
        self._update_node(new_elem, upper)
        HTMLElement.remove_node(old)
        self.elem = new_elem
        self.set_subordinates()
        self.bind_attrs()
        for x in self.subelements:
            if type(x) is HTMLElement:
                x.update()
            elif type(x) is str:
                self.elem <= x

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
