from code.sfml_plus import Window
from code.sfml_plus import Key
from code.sfml_plus.ui import Box

Window = Window((1200,600), "Untitled")
Box1 = Box()
Box1.size = 300,300
Box1.open()
Box1.center = 1200/2, 600/2

################################################
from code.sfml_plus import Font, Multiline_Text
################################################

Text1 = Multiline_Text(Font("speech"))
Text1.position = Box1.position
Text1.size = Box1.size
Text1.padding = 5
#
t = "---------------------------\n"
t=t+"TILE TOOL\n"
t=t+"---------------------------\n"
t=t+"\n"
t=t+"GENERAL\n"
t=t+"* Hold Left/Right Mouse - Adds/removes tiles.\n"
t=t+"* Hold Spacebar - Opens up the Tile Selector.\n"
t=t+"\n"
t=t+"TILE SELECTOR\n"
t=t+"* Hold and Drag Left Mouse - Select tiles.\n"
t=t+"* Select Dropdown item - Change tilesheet.\n"
t=t+"\n\n---\n\n"
t=t+"TIPS\n"
t=t+"* A single Room cannot use more than 5 different tilesheets.\n"
t=t+"* A cursor with a lot of tiles can be used as a HUGE eraser.\n"


#
Text1.write(t)

while Window.is_open:
	if Window.is_focused:
		Box1.controls(None,None,None)
		if Key.ENTER.pressed(): print 1

	Window.clear((255,220,0))
	Window.draw(Box1)
	Window.draw(Text1)
	Window.display()