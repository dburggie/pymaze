import model, view

class Console:

    default_colors = ( (0,0,0), (255,255,255), (255,0,0), (255,255,255) )



    def __init__(self, size = (50,50), bs = (8,8)):
        if not view.initialized():
            view.init()
        self.size = 1 + 2 * size[0], 1 + 2 * size[1]
        self.ui = view.UI()
        self.ui.blocksize = bs
        self.ui.colors = Console.default_colors
        self.maze = model.Maze(size)



    def setColors(self, colors):
        self.ui.colors = colors



    def setFPS(self, fps):
        self.ui.fps = fps



    def setup(self):
        self.ui.genTiles()
        self.ui.setGridSize(self.size)
        self.ui.start()



    def draw(self):
        changes = self.maze.getUpdates()
        self.ui.render(changes)
        self.ui.draw()

    def resetPath(self):
        self.maze.resetPath()

    def stepper(self):
        self.setup()
        while True:
            self.ui.wait()
            for e in self.ui.getEvents():
                if e == view.QUIT:
                    return
                elif e == view.RESET:
                    self.maze.update()
                    self.draw()

    def run(self):
        self.setup()
        captures = 0
        while True:
            self.ui.wait()
            for e in self.ui.getEvents():
                if e == view.QUIT:
                    return
                elif e == view.RESET:
                    self.resetPath()
                elif e == view.SAVE:
                    fn = "capture-{:0>2}.png".format(captures)
                    print "saving capture:", fn
                    self.ui.screencap(fn)
            if self.maze.full:
                continue
            self.maze.update()
            self.draw()



