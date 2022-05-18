from browpy import document, Element, HTMLElement, title, set_root

def incrementor(obj):
    def fn(_):
        obj.n += 1
        obj.update()
    return fn

def decrementor(obj):
    def fn(_):
        obj.n -= 1
        obj.update()
    return fn

class Number(Element):
    def __init__(self, attrs):
        super().__init__(attrs)
        self.n = 0

    def render(self):
        return <div>
            <button on_click={incrementor(self)}>+</button>
            {self.n}
            <button on_click={decrementor(self)}>-</button>
        </div>


title("Counting Tool")
n = <Number/>
set_root(n)
