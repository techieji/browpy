from browpy import HTMLElement, document, title, Element

class TestElem(Element):
    def __init__(self, attrs):
        super().__init__(attrs)
        self.text = "This is from inside an element!!!"
    
    def render(self):
        return <button><b>{self.text}</b></button>

    def on_click(self, _):
        print("click registered")
        self.text = ("AERHWAEFUIHAWILUEFH IT WORKS!!!!!")
        self.update(document)

title("Element test")
te = <TestElem/>
te.update(document)
