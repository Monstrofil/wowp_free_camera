import BigWorld, Math
import Keys
import GlobalEvents
import gui.ClientHangarSpace as space
import math
import GUI
import math




class FreeCamera():
    def __init__(self):
        self.aircam = None
        self.cam = None
        self.current = 0
        GlobalEvents.onKeyEvent += self.handleKeyEvent

    def get_cam(self):
        return self.cam
        
    
    def handleKeyEvent(self, event):
        if event.isCtrlDown():
            if event.key == getattr(Keys, 'KEY_Q') and event.isKeyDown() and self.aircam == None: #setting new cam
                self.aircam = BigWorld.camera()
                self.cam = BigWorld.CursorCamera() #saving old cam
                self.cam.source = BigWorld.dcursor().matrix
                BigWorld.camera(self.cam)
                print '[FREECAMERA]: Installed'
            if event.key == getattr(Keys, 'KEY_W') and event.isKeyDown() and self.aircam != None:
                BigWorld.camera(self.aircam)
                self.aircam = None

            if event.key == getattr(Keys, 'KEY_E') and event.isKeyDown():
                if len(BigWorld.models()) != 0:
                    entity = BigWorld.models()[self.current]
                    while 'fake' in entity.name():
                        self.current += 1
                        if self.current >= len(BigWorld.models()):
                            self.current = 0
                        entity = BigWorld.models()[self.current]
                    self.cam.target = entity.matrix
                    self.current += 1
                    if self.current >= len(BigWorld.models()):
                        self.current = 0
cam = FreeCamera()
