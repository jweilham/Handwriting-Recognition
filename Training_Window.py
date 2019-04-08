
from Window import *


class Training_Window(Window):

    def __init__(self, filename):
        Window.__init__(self, filename = filename, train = True)

