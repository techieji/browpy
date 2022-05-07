p = (<html><body onload="brython()"><img href="me.jpg"/><p>This is a paragraph, and <b class="asdf">this part</b> is bold!</p></body></html>)

html({}, body({'onload': "brython()"}, img({'href': 'me.jpg'}), p(TEXT("This is a paragraph, and "), b({'class': 'asdf'}, 'this part'), TEXT(' is bold!'))
