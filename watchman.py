from PySide import QtCore, QtGui
import sched, time
from SimpleCV import *

# CV WATCHING PARAMTERS
s = sched.scheduler(time.time, time.sleep)
fps = 10
scale = 0.5

def shoot_screen(sc,w,h):
    originalPixmap = None
    originalPixmap = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId())
    originalPixmap = originalPixmap.scaled(w,h)
    format = 'png'
    path = QtCore.QDir.currentPath() + "/tempout." + format
    originalPixmap.save(path, format)
    
    # BUFFER CODE TESTING
    # byte_array = QByteArray()
    # buffer = QBuffer(byte_array)
    # buffer.open(QIODevice.WriteOnly)
    # originalPixmap.save(buffer, format)
    # sio = cStringIO.StringIO(byte_array)
    # sio.seek(0)

    img = Image(str(path))
    dist = img.colorDistance(SimpleCV.Color.BLACK).dilate(2)
    segmented = dist.stretch(200,255)
    blobs = segmented.findBlobs()
    if blobs:
        circles = blobs.filter([b.isCircle(0.5) for b in blobs])
        if circles:
            segmented.drawCircle((circles[-1].x, circles[-1].y), circles[-1].radius(),SimpleCV.Color.BLUE,3)
            
    segmented.show()

    sc.enter(1/fps, 1/fps, shoot_screen, (sc,w,h,))
    
def start_watching():
    geo = QtGui.QDesktopWidget().availableGeometry()
    w = geo.width()*scale
    h = geo.height()*scale
    s.enter(0, 1/fps, shoot_screen, (s,w,h,))
    s.run()

if __name__ == '__main__':
    start_watching()    

