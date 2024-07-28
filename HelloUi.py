import ui

class M:
  def __init__(self):
    self.next_messages = [
      'you clicked',
      'you clicked again',
      'more clicking!'
      ]
    self.next_i = 0
    
  def next(self):
    ni = self.next_i
    ni = ni + 1
    l = len(self.next_messages)
    self.next_i = ni % l
    return self.next_messages[self.next_i]
    
  def do_click(self, sender):
    sender.title=self.next()


m = M()
v = ui.load_view()
v.name = 'demo'

button = ui.Button(title='click')
button.center = (v.width * 0.5, v.height * 0.5)
button.background_color = "#9ab4ff"
button.width = 120
button.flex = 'LRTB'
button.action = (lambda sender: m.do_click(sender))

v.add_subview(button)
v.present('sheet')

