from Window import *


class User_Window(Window):


    def __init__(self):
        Window.__init__(self, w = 700, h = 500)
        
	# Update menubar
        self.menubar.insert_command(0, label = "Save & Quit", command=self.saveq)
        self.config(menu=self.menubar)



    def saveq(self):
        self.save("user_input/" + self.filename)
        self.destroy()
