from code.sfml_plus import Window
from code.sfml_plus import Key, Mouse, Camera

##########################################

from code.level_editor.toolbox import ToolBox

##########################################

Window = Window((1200,600), "ToolBox")
ToolBox = ToolBox(*Window.size)

Camera = Camera(Window)
Mouse = Mouse(Window)

while Window.is_open:
	if Window.is_focused:
		ToolBox.controls(Key, Mouse, Camera)
		
		if Key.TAB.pressed(): ToolBox.toggle()

	Window.clear((255,220,0))
	Window.draw(ToolBox)
	Window.display(Mouse)