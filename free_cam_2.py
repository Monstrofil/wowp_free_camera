import BigWorld, Math
import Keys
import GlobalEvents
import gui.ClientHangarSpace as space
import math
import GUI
from TeamObject import TeamObject
import math




class FreeCamera():
    def __init__(self):
        self.aircam = None
        self.cam = None
        self.current = 0
        GlobalEvents.onKeyEvent += self.handleKeyEvent

    def get_cam(self):
        return self.cam

    def dist(a, b):
        dx = b.x - a.x
        dy = b.y - a.y
        dz = b.z - a.z
        dist = round(math.sqrt(dx * dx + dy * dy + dz * dz), 2)

    def get_nearest(self): #nearest entity
        temp = []
        items = BigWorld.entities.items()
        owner_pos = BigWorld.camera().position
        for item in items:
            entity = items[1]
            entity_pos = entity.position
            temp.append([dist(entity_pos,owner_pos) , entity])
        temp.sort()
        return temp[1][1]
        
    
    def handleKeyEvent(self, event):
        if event.isCtrlDown():
            if event.key == getattr(Keys, 'KEY_Z') and event.isKeyDown() and self.aircam == None: #setting new cam
                self.aircam = BigWorld.camera()
                self.cam = BigWorld.CursorCamera() #saving old cam
                self.cam.source = BigWorld.dcursor().matrix
                BigWorld.camera(self.cam)
                print '[FREECAMERA]: Installed'
            if event.key == getattr(Keys, 'KEY_X') and event.isKeyDown() and self.aircam != None:
                BigWorld.camera(self.aircam)
                self.aircam = None

            if event.key == getattr(Keys, 'KEY_C') and event.isKeyDown():
                self.current += 1
                if self.current >= len(BigWorld.entities.items()):
                    self.current = 0
                entity = BigWorld.entities.items()[self.current][1]
                while (True): #only planes
                    if issubclass(entity.__class__, TeamObject):
                        self.current += 1
                        if self.current >= len(BigWorld.entities.items()):
                            self.current = 0
                        entity = BigWorld.entities.items()[self.current][1]
                    else:
                        break
                        
                self.cam.target = entity.matrix
cam = FreeCamera()
