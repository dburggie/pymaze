
import random
import pygame

default_size = (50,50)

_palette = ( (0,0,0), (255,255,255), (255,0,0) )

# rng elements, be sure you call random.seed() before using this module

_rng_vectors = ( (0,-1), (1,0), (0,1), (-1,0) )
_rng_index_count = len(_rng_vectors)

def _random_vector():
    return _rng_vectors[ random.randrange(_rng_index_count) ]

def _random_item(item_list):
    return item_list[ random.randrange(len(item_list)) ]

def _inflate(v):
    return 1 + 2 * v[0], 1 + 2 * v[1]

def _deflate(v):
    return (v[0] - 1) / 2, (v[1] - 1) / 2


# The Path class represents a non-branching path within the maze
# We will be taking a random walk, checking the color of the target square
# and responding accordingly.
# When we encounter our own path, we must remove the loop we've formed.
# We do this by truncating the path to the node we just hit.
# We're implementing this as a linked list of nodes.
class Path:

    maxima = (20,20)

    def __init__(self, parent, position):
        self.parent = parent
        self.position = position

    def walk(self):
        """Walk a step in a reasonable random direction."""
        x, y = self.position
        dx, dy = _random_vector()
        newpos = x+dx, y+dy
        # don't go to our parent node or out of bounds
        while not self._legal_target(newpos):
            dx,dy = _random_vector()
            newpos = x+dx, y+dy
        return Path(self, newpos)

    def _legal_target(self, v):
        """Check if v is at a legal position for a step in a random walk."""
        # illegal if v is our parent
        if self.parent and v == self.parent.position:
            return False
        # legal if within boundaries
        if 0 <= v[0] < Path.maxima[0] and 0 <= v[1] < Path.maxima[1]:
            return True
        else:
            return False

    def truncateTo(self, target):
        """Return the most recent node in the list with the given position."""
        node = self.parent
        while node and node.position != target:
            node = node.parent
        return node


# The Maze class represents a maze as it is being built.
# A maze is a two dimensional grid of nodes. Adjacent nodes may or may not be
# connected by a path. The Maze class allows us to draw Path objects into our
# maze.
class Maze:

    def __init__( self, size):
        self.width, self.height = size
        self.size = _inflate(size)
        self.grid = []
        for y in range(self.height):
            self.grid.append([])
            for x in range(self.width):
                self.grid[y].append(0)
        self.surface = None

    def init(self):
        sx, sy = 0,1
        ex = self.size[0] - 1
        ey = self.size[1] - 2
        if self.surface:
            self.surface.fill(_palette[0])
            self.surface.set_at( (sx,sy), _palette[1] )
            self.surface.set_at( (ex,ey), _palette[1] )

    def draw(self, path, color):
        """Draw Path object into maze with given color."""
        x,y = path.position
        self.grid[y][x] = color
        x,y = _inflate(path.position)
        if self.surface:
            self.surface.set_at( (x,y), _palette[color] )
        node = path
        target = node.parent
        while target:
            self._draw_segment(node.position,target.position,color)
            node = target
            target = target.parent

    def _draw_segment(self, start, end, color):
        """Draw segment between nodes."""
        self.grid[end[1]][end[0]] = color
        dx,dy = end[0] - start[0], end[1] - start[1]
        x,y = _inflate(start)
        target = _inflate(end)
        while (x,y) != target:
            x += dx
            y += dy
            if self.surface:
                self.surface.set_at( (x,y), _palette[color] )



    def getSurface(self, surface):
        return self.surface


    def getAt(self, position):
        x,y = position
        return self.grid[y][x]

    def getNode(self, color = 0):
        """Returns node position of given color, or None if none."""
        cells = []
        for y in range(self.height):
            for x in range(self.width):
                if color == self.grid[y][x]:
                    cells.append( (x,y) )
        if len(cells) == 0:
            return None
        else:
            return _random_item(cells)



# the Builder class maintains a Maze object, and builds it until it is full.
class Builder:
    def __init__(self, size):
        Path.maxima = size
        self.path = None
        self.size = size
        self.maze = Maze(size)
        self.done = False

    def init(self):
        self.maze.init()
        self.path = Path( None, (0,0) )
        self.path = self.path.walk() 
        while self.maze.getAt(self.path.position) == 0:
            self.draw(1)
            self.path = self.path.walk()
        self.path = None

    def draw(self, color):
        """Draw the path the given color."""
        if self.path:
            self.maze.draw(self.path, color)

    def reset(self):
        self.draw(0)
        self.path = None

    def newPath(self):
        """Setup a new Path within the maze at an open node."""
        p = self.maze.getNode(0)
        if p == None:
            self.done = True
            self.path = None
        else:
            self.path = Path(None, p)

    def step(self):
        """Let the path continue it's random walk one step."""
        if self.path:
            self.path = self.path.walk()
        else:
            self.newPath()

    def update(self):
        """Check what we stepped on and respond."""
        if self.path == None:
            return
        p = self.path.position
        code = self.maze.getAt(p)
        # respond to wall by drawing it in and starting an new path.
        if 1 == code:
            self.draw(1)
            self.path = None
        # respond to path by truncating path
        elif 2 == code:
            self.draw(0)
            self.path = self.path.truncateTo(p)
        self.draw(2)

_quit_keys  = [ pygame.K_q, pygame.K_ESCAPE ]
_reset_keys = [ pygame.K_r ]
_save_keys  = [ pygame.K_s ]
_save_format = "image_pymaze_{:0>3}.png"

def run(size, fps = 10):
    pygame.init()
    builder = Builder(default_size)
    pygame.display.set_mode( _inflate(default_size) )
    builder.maze.surface = pygame.display.get_surface()
    builder.init()
    clock = pygame.time.Clock()
    saves= 0
    finished = False
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            elif e.type == pygame.KEYDOWN:
                k = e.key
                if k in _quit_keys:
                    return
                elif k in _reset_keys:
                    builder.reset()
                elif k in _save_keys:
                    filename = _save_format.format(saves)
                    print "saving to", filename
                    saves += 1
                    surface = pygame.display.get_surface()
                    pygame.image.save(surface, filename)
        pygame.display.flip()
        clock.tick(fps)
        if builder.done:
            if not finished:
                print "done."
                finished = True
            continue
        builder.step()
        builder.update()

if __name__ == "__main__":
    run(default_size, 30)





