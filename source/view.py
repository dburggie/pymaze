import pygame


QUIT = 0
Q_KEYS = [pygame.K_q, pygame.K_ESCAPE]

RESET = 1
R_KEYS = [pygame.K_r]

SAVE = 2
S_KEYS = [pygame.K_s]



# UI:
#   UI.init() -- initialize the module
#   UI.initialized -- boolean, True if module is initialized
#   genTiles() -- setup tiles from colors and blocksize members
#   setGridSize(size) -- setup screen resolution from blocksize and size
#   start() -- open screen and start displaying
#   draw(tiles) -- tiles [((x,y),c)...], draw them
#   print() -- print the changes from draw() to the screen
#   screencap(filname) -- print the screen to the given filename
#   getEvents() -- get a list of ui requests using the above codes
#   wait() -- wait so that we don't go faster than fps frames per second

class View:
    initialized = False

def initialized():
    return View.initialized

def init():
    if not View.initialized:
        pygame.init()
        View.initialized = True

class UI:

    def __init__(self):
        self.blocksize = 8,8
        self.colors = None
        self.tiles = None
        self.surface = None
        self.clock = pygame.time.Clock()
        self.fps = 20
        self.resolution = None



    def wait(self):
        self.clock.tick(self.fps)



    def genTiles(self):
        self.tiles = []
        for i in range(len(self.colors)):
            self.tiles.append( pygame.Surface(self.blocksize) )
            self.tiles[i].fill( self.colors[i] )



    def start(self):
        if not View.initialized:
            return
        pygame.display.set_mode( self.resolution )
        self.surface = pygame.display.get_surface()
        self.surface.fill( self.colors[0] )
        pygame.display.flip()




    def render(self, changes):
        """Draw contents of tiles to screen."""
        # changes is a dictionary object
        # the keys are locations
        # the values are the color codes
        for location in changes:
            x = self.blocksize[0] * location[0]
            y = self.blocksize[1] * location[1]
            color = changes[location]
            self.surface.blit( self.tiles[color], (x,y) )



    def draw(self):
        pygame.display.flip()



    def screencap(self, filename):
        pygame.image.save(self.surface, filename)



    def setGridSize(self, gridsize):
        x,y = gridsize
        x *= self.blocksize[0]
        y *= self.blocksize[1]
        self.resolution = x,y



    def getEvents(self):
        events = []
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                events.append(QUIT)
            elif e.type == pygame.KEYDOWN:
                k = e.key
                if k in Q_KEYS:
                    events.append(QUIT)
                elif k in R_KEYS:
                    events.append(RESET)
                elif k in S_KEYS:
                    events.append(SAVE)
        return events




