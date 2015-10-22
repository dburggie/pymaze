
import random





def _random_item(collection):
    return collection[ random.randrange( len(collection) ) ]





class Codes:
    background = 0
    foreground = 1
    temporary  = 2
    forbidden  = 3





class Path:
    def __init__(self, position, parent = None):
        self.position = position
        self.parent = parent
        if parent:
            self.length = parent.length + 1
        else:
            self.length = 1



    def add(self, v):
        """Return a tuple containing v+position."""
        return v[0]+self.position[0], v[1]+self.position[1]



    def avg(self):
        """Return the average position of this and it's parent."""
        x = ( self.parent.position[0] + self.position[0] ) / 2
        y = ( self.parent.position[1] + self.position[1] ) / 2
        return x,y



    def truncate(self, p):
        node = self.parent
        while node and node.position != p:
            node = node.parent
        return node






# maze object uses color codes to describe walls, floors, and temp-paths
# these codes are 0:wall, 1:floor, 2:temp, 3:off-limits

class Maze:



    def __init__(self, size):
        # note: size is the number of nodes in the maze, not the actual size
        self.size = 1 + 2 * size[0], 1 + 2 * size[1]
        self.width = self.size[0]
        self.height = self.size[1]

        self.path = None

        # setup maze grid
        self.grid = []
        for y in range(self.height):
            self.grid.append([])
            for x in range(self.width):
                self.grid[y].append(0)

        # setup book-keepers
        self.empty = []
        self.updates = {}
        self.initialized = False
        self.full = False
        for y in range(1, self.height, 2):
            for x in range(1, self.width, 2):
                self.empty.append( (x,y) )



    def init(self):
        if not self.path:
            self.resetPath()
        else:
            self.step()
            x,y = self.path.position

            # check if we've made a loop, eat it if we have
            code = self.grid[y][x]
            if code == Codes.temporary:
                self.draw(Codes.background)
                self.path = self.path.truncate(self.path.position)
                self.draw(Codes.temporary)
                return

            # check if we got a long way away, end if we have
            elif self.path.length >= 40:
                self.draw(Codes.foreground)
                self.path = None
                self.initialized = True
            
            # otherwise, just print it
            else:
                self.draw(Codes.temporary)



    def update(self):

        # handle edge cases: all done, and un-initialized
        if self.full:
            return
        if not self.initialized:
            self.init()
            return

        # handle an empty path
        if not self.path:
            self.resetPath()
            if not self.path:
                self.full = True
                return
            self.draw(Codes.temporary)
        else:
            self.step()
            x,y = self.path.position
            code = self.grid[y][x]
            if code == Codes.background:
                self.draw(Codes.temporary)
            elif code == Codes.foreground:
                self.draw(Codes.foreground)
                node = self.path
                while node:
                    if node.position in self.empty:
                        self.empty.remove(node.position)
                    node = node.parent
                self.path = None
            elif code == Codes.temporary:
                self.draw(0)
                self.path = self.path.truncate(self.path.position)
                self.draw(2)



    def step(self):
        """Extend the path in a legal direction."""

        # make a list of potential targets
        potentials = []
        for v in ( (0,-2), (2,0), (0,2), (-2,0) ):
            potentials.append(self.path.add(v))

        # cull the list
        candidates = []
        for x,y in potentials:
            if x < 0 or y < 0:
                continue
            if x >= self.width or y >= self.height:
                continue
            if self.grid[y][x] == Codes.forbidden:
                continue
            p = self.path.parent
            if p and p.parent and (x,y) == p.parent.position:
                continue
            candidates.append( (x,y) )

        # pick one of the candidates
        p = _random_item(candidates)
        self.path = Path(p, self.path)



    def resetPath(self):
        self.draw(0)
        if len(self.empty) > 0:
            p = self.empty[ random.randrange(len(self.empty)) ]
            self.path = Path(p)



    def draw(self, color):
        """Draw contents of path into the grid, tracking updates."""
        if not self.path:
            return
        # draw the head
        x,y = self.path.position
        self.grid[y][x] = color
        self.updates[ (x,y) ] = color

        # draw the tail
        node = self.path
        target = node.parent
        while target:
            x,y = target.position
            self.grid[y][x] = color
            self.updates[ (x,y) ] = color
            x,y = node.avg()
            self.grid[y][x] = color
            self.updates[(x,y)] = color
            node = target
            target = target.parent



    def getUpdates(self):
        ups = self.updates
        self.updates = {}
        return ups






if __name__ == "__main__":
    m = Maze( (10,10) )
    for i in range(10):
        m.update()
    print "empty:  ", m.empty
    print "updates:", m.updates
    print "grid:   ", m.grid




