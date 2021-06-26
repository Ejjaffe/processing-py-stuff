# PROGRAM OBJECTS #######################################################################################################

class Mapper(object):
    """
    A slapshod mapper object for cartesian-to-canvas coordinate mapping
    """
    def __init__(self, coordsx=(-1.0,1.0), coordsy=(-1.0,1.0), px=100, py=100):
        """
        coordsx : 2-tuple of floats
            min and max x coordinates
            
        coordsy : 2-tuple of floats
            min and max y coordinates
            
        px : int
            number of canvas pixels in x direction
            
        py : int
            number of canvas pixxels in y direction 
        
        """
        self.coordsx = coordsx
        self.coordsy = coordsy
        self.px = px
        self.py = py
        
    def y_mapper(self, y):
        """
        map y from cartesian plane to canvas
        """
        start_1, stop_1 = self.coordsy
        # note here that 0 is at the top, so the canvas lower bound is the number of pixels
        return map(y, start_1, stop_1, self.py, 0)
    
    def x_mapper(self, x):
        """
        map x from cartesian plane to canvas
        """
        start_1, stop_1 = self.coordsx
        return map(x, start_1, stop_1, 0, self.px)
        
    def convert(self, x, y):
        """
        map x,y from cartesian plane to canvas
        returns (x_canvas, y_canvas)
        
        You can unpack the tuple:
        >>> x_canvas, y_canvas = Mapper().convert(x_cart, y_cart)
        """
        return self.x_mapper(x), self.y_mapper(y)

class ParabolicLines(object):
    """
    Set of quasi-randomly placed horizontal lines bounded by a (limited) parabola.
    Lines move up and down for funsies.
    """
    def __init__(self, coeff, d_from_0, mapper=Mapper(), n_lines=10, shift_lines=True, speed=0.01):
        """
        coeff : float
            lines are bounded by coeff * x^2
            
        d_from_0 : float, should be positive
            lines stop at d_from_0 in the direction of the sign of coeff.
            example: if coeff = -1.3 then the lines would go from 0 to -d_from_0
            example: if coeff = 0.75 then the lines would go from 0 to d_from_0
            
        mapper : Mapper 
            the mapper object for your canvas (you only need one)
            
        n_lines : int
            number of lines drawn within in your parabola
            
        shiftLines : bool
            whether or not to shift the lines up and down or not
        """
        self.coeff = coeff
        self.dir = self.coeff/abs(self.coeff)
        self.d_from_0 = d_from_0
        self.mapper=mapper
        self.n_lines = n_lines
        self.shift_lines = shift_lines
        self.linepos = self._init_linepos()
        self.t = 0
        self.t_step = speed
        
    def _init_linepos(self):
        """
        Step 1. create n_lines num. of cells from 0 to 1 that are spaced (1 / n_lines) apart.
        Step 2. place one line at random height within each cell
        Step 3. scale values such that instead of going 0-1, they now go 0 to sign(coeff)*d_from_0.
        
        returns a list of n_lines floats from 0 to sign(coeff) * d_from_0
        """
        cell_mins = [i/float(self.n_lines) for i in range(0, self.n_lines)] # minimum value of cell, max val is min + 1/n_lines
        ht_over_cell_min = [random(0,1)/float(self.n_lines) for i in range(0, self.n_lines)] # random height within cell
        unscaled_heights = [min_ + rand_ht for min_, rand_ht in zip(cell_mins, ht_over_cell_min)] # all line heights unscaled
        heights =  [v * self.d_from_0 * self.dir for v in unscaled_heights] # all line heights scaled
        return heights
    
    def _line_extent(self, ht):
        """
        how wide the line is in both directions from 0 based on it's height.
        This is what makes the parabola shape.
        
        You could modify this to return two values to use as left and right bounds and create asymmetric shapes
        """
        return sqrt(abs(ht/self.coeff))
    
    def _draw_lines(self):
        """
        Will draw all lines in the ParabolicLines object on the canvas
        """
        for y in self.linepos:
            ext = self._line_extent(y)
            x0, y0 = self.mapper.convert(-ext, y)
            x1, y1 = self.mapper.convert(ext, y)
            line(x0,y0,x1,y1)
            
    def _adjust_lines(self):
        """
        makes the line heights jump up and down :)
        """
        self.linepos = [l + 0.005 * cos(self.t) for l in self.linepos]
        
    def _step_time(self):
        self.t += self.t_step
        
    def draw_and_step(self):
        if self.shift_lines:
            self._step_time()
            self._adjust_lines()
        self._draw_lines()

# PROGRAM VARIABLES #######################################################################################################

# canvas        
X_PIXELS = 1000
Y_PIXELS = 1000

canvas_mapper = Mapper(coordsx=[-1.5,1.5], coordsy=[-2, 2], px=X_PIXELS, py=Y_PIXELS)

# parabolas
n_parabolas = 8
coeffs = [random(-3,3) for _ in range(n_parabolas)]
max_hts = [random(-1,1) for _ in range(n_parabolas)]
n_lines = [int(random(5,20)) for _ in range(n_parabolas)]
do_shifts = [random(0,1)>0.2 for _ in range(n_parabolas)]
speeds = [random(0.005, 0.01) for _ in range(n_parabolas)]

# SCRIPT ####################################################################################################################

parabolas = []

for coeff, max_ht, n_line, do_shift, speed in zip(coeffs, max_hts, n_lines, do_shifts, speeds):
    new_parab = ParabolicLines(
        coeff=coeff, 
        d_from_0=max_ht, 
        mapper=canvas_mapper, 
        n_lines=n_line, 
        shift_lines=do_shift,
        speed = speed
    )
    parabolas.append(new_parab)
    
def setup():
    size(X_PIXELS, Y_PIXELS)
    background(255);
    strokeWeight(3)
    
def draw():
    clear()
    background(255);
    for parabola in parabolas:
        parabola.draw_and_step()
    
