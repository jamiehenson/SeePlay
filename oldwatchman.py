#
# Screen watcher code
#
# J. Henson, 2014
#
import counters
from PySide import QtGui


class WatchWindow(QtGui.QWidget):
    def __init__(self, dens, parent = None):
        super(WatchWindow, self).__init__(parent)
        print "Started watching."
        self.start_watching(dens,2,True)

    def paintEvent(self, event):
        #while True:
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw_vision(True,qp)
        qp.end()
        self.update()

    def draw_vision(self, on, qp):
        global board

        img = QtGui.QPixmap.grabWindow(
        QtGui.QApplication.desktop().winId(),
        x = 0,
        y = 0,
        height = hsize,
        width = wsize,
        ).toImage()

        board = get_board(img)
        board_size = [wsize, hsize]

        for y in range(dens):
            for x in range(dens):
                col = match_colour(board[y][x])
                counters.set_counters(col)
                if on == True:
                    #pygame.draw.rect(disp, colour_lookup(col), (x*(wsize/dens/psize), y*(hsize/dens/psize), wsize/dens/psize, hsize/dens/psize))
                    r, g, b = colour_lookup(col)
                    qp.setBrush(QtGui.QColor(r,g,b))
                    qp.drawRect(x*(wsize/dens/psize), y*(hsize/dens/psize), wsize/dens/psize, hsize/dens/psize)

        counters.print_counters()
        counters.set_counters("wipe")

    def start_watching(self, d, p, on):
        global anchor, disp, board, dens, wsize, hsize, psize
        global red, green, blue, yellow, white, orange, purple, black

        anchor = (0,0)
        dens = d
        psize = p
        geo = QtGui.QDesktopWidget().availableGeometry()
        wsize = geo.width()
        hsize = geo.height()

        counters.set_counters("wipe")
        counters.spike_watch(True)

        #self.draw_vision(on)

def get_pixel(x, y, img):
    col = QtGui.QColor(img.pixel(x,y)).getRgb()[:-1]
    return col

def get_field(x, y, img):
    x, y = board_to_pixel(x, y)
    return get_pixel(x,y,img)

def colour_lookup(code):
    cols = {'r': (255, 0, 0),
            'g': (0, 255, 0),
            'b': (0, 0, 255),
            'k': (0, 0, 0),
            'y': (255, 255, 0),
            'p': (255, 0, 255),
            't': (0, 255, 255),
            'w': (255, 255, 255),
            '.': (0, 0, 0)}

    r, g, b = cols[code]

    return r, g, b

def match_colour(pix):
    names = ['r', 'g', 'b', 'k', 'y', 'p', 't', 'w']
    colours = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
              (0, 0, 0), (255, 255, 0), (255, 0, 255),
              (0, 255, 255), (255, 255, 255)]

    c = 0
    for colour in colours:
        diff = 0
        for i in range(3):
            diff += abs(colour[i]-pix[i])
        if diff < 250:
            return names[c]
        c += 1
    return "."

def get_board(img):
    board = []
    for y in range(0, dens):
        board.append([])
        for x in range(0, dens):
            pix = get_field(x, y, img)
            board[y].append(pix)
    return board

def board_to_pixel(x, y):
    x = x*(wsize/dens) + anchor[0]
    y = y*(hsize/dens) + anchor[1]
    return x, y
