import BigWorld, Math
import Keys
import GlobalEvents
import gui.ClientHangarSpace as space
import math
import GUI
import math


class FreeCamera():
    def __init__(self):
        self.cam = None
        self.position = Math.Vector3(0, 50, 0)
        self.delta = 2
        self.aircam = None
        self.speed = 0
        self.speed_back = 0
        self.last_yaw = None
        self.last_pitch = None
        self.free = None
        self.left = 0
        self.right = 0
        self.a = 20
        self.fixed = False
        GlobalEvents.onKeyEvent += self.handleKeyEvent

    def myaw(self):
        matrix = Math.Matrix(BigWorld.dcursor().matrix)
        if self.last_yaw == None:
            self.last_yaw = matrix.yaw
            return matrix.yaw
        else:
            yaw = self.last_yaw
            self.last_yaw = matrix.yaw
            return yaw + (matrix.yaw - yaw) / 4 #bad code :)

    def mpitch(self):
        matrix = Math.Matrix(BigWorld.dcursor().matrix)
        if self.last_pitch == None:
            self.last_pitch = matrix.pitch
            return matrix.pitch
        else:
            pitch = self.last_pitch
            self.last_pitch = matrix.pitch
            return pitch + (matrix.pitch - pitch) / 4 #bad code too :)
        return 

    def SetPosition(self):
        try:
            camMatrix = Math.Matrix()
            camMatrix.setRotateYPR((math.radians(0), math.radians(0), math.radians(0)))
            camMatrix.translation = self.position
            self.cam.target = camMatrix
            #matrix = Math.Matrix(BigWorld.dcursor().matrix)
            #maxrix.setRotateYPR(myaw(), mpitch(), matrix.roll)
            #self.cam.source = maxrix
        except:
            pass

    def dist(self, a, b):
        dx = b.x - a.x
        dy = b.y - a.y
        dz = b.z - a.z
        dist = round(math.sqrt(dx * dx + dy * dy + dz * dz), 2)
        return dist

    def get_nearest(self): #nearest entity
        temp = []
        items = BigWorld.entities.items()
        owner_pos = self.position
        for item in items:
            entity = item[1]
            entity_pos = entity.position
            temp.append([self.dist(entity_pos, owner_pos) ,entity])
        temp.sort()
        return temp[0][1]

    def get_nearest_model(self): #nearest bomb or rocket
        temp = []
        items = BigWorld.models()
        owner_pos = self.position
        for item in items:
            entity = item
            entity_pos = entity.position
            temp.append([self.dist(entity_pos, owner_pos) ,entity])
        if len(temp) != 0:
            temp.sort()
            return temp[0][1]
        else:
            return BigWorld.player()

    def btn(self): #moving camera
        if BigWorld.isKeyDown(getattr(Keys, 'KEY_S'), 0):
            self.speed_back += 0.001 * self.a
            self.speed_back = min(self.speed_back, abs(self.delta))
            self.position.z -= self.delta * math.cos(self.myaw())
            self.position.x -= self.delta * math.sin(self.myaw())
            self.position.y += self.delta * math.sin(self.mpitch() * 2)
        elif self.aircam != None:
            self.speed_back -= 0.002 * self.a
            self.speed_back = max(self.speed_back, 0)
            self.position.z -= self.speed_back * math.cos(self.myaw())
            self.position.x -= self.speed_back * math.sin(self.myaw())
            self.position.y += self.speed_back * math.sin(self.mpitch() * 2)
        if BigWorld.isKeyDown(getattr(Keys, 'KEY_W'), 0):
            self.speed += 0.001 * self.a
            self.speed = min(self.speed, abs(self.delta))
            self.position.z += self.speed * math.cos(self.myaw())
            self.position.x += self.speed * math.sin(self.myaw())
            self.position.y -= self.speed * math.sin(self.mpitch() * 2)
        elif self.aircam != None:
            self.speed -= 0.002 * self.a
            self.speed = max(self.speed, 0)
            self.position.z += self.speed * math.cos(self.myaw())
            self.position.x += self.speed * math.sin(self.myaw())
            self.position.y -= self.speed * math.sin(self.mpitch() * 2)
        if BigWorld.isKeyDown(getattr(Keys, 'KEY_D'), 0):
            self.position.z -= self.delta * math.sin(self.myaw())
            self.position.x += self.delta * math.cos(self.myaw())
        if BigWorld.isKeyDown(getattr(Keys, 'KEY_A'), 0):
            self.position.z += self.delta * math.sin(self.myaw())
            self.position.x -= self.delta * math.cos(self.myaw())
        if BigWorld.isKeyDown(getattr(Keys, 'KEY_Z'), 0):
            self.position.y -= self.delta
        if BigWorld.isKeyDown(getattr(Keys, 'KEY_Q'), 0):
            self.position.y += self.delta
        if BigWorld.isKeyDown(getattr(Keys, 'KEY_G'), 0):
            m = Math.Matrix()
            self.cam.source = BigWorld.player().matrix
        self.SetPosition()
        
        return

    def onUpdateHookBtn(self):
        if self.aircam != None:
            self.btn()
            updateHandler = BigWorld.callback(0.001, lambda : self.onUpdateHookBtn())

    def get_cam(self):
        return self.cam
    
    def handleKeyEvent(self, event):
        if event.isCtrlDown():
            if event.key == getattr(Keys, 'KEY_P') and event.isKeyDown():
                self.delta += 0.05 #increase speed
            if event.key == getattr(Keys, 'KEY_L') and event.isKeyDown():
                self.delta -= 0.05 #decrease speed
                self.delta = max(self.delta,0)
            if event.key == getattr(Keys, 'KEY_Y') and event.isKeyDown(): #setting new cam
                self.aircam = BigWorld.camera()
                self.cam = BigWorld.CursorCamera() #saving old cam
                self.onUpdateHookBtn()
                self.position = BigWorld.player().position
                self.position = Math.Vector3(BigWorld.camera().position.x, BigWorld.camera().position.y, BigWorld.camera().position.z)
                self.label = GUI.Text('')
                matrix = Math.Matrix(BigWorld.dcursor().matrix)          
                camMatrix = Math.Matrix()
                camMatrix.setRotateYPR((math.radians(0), math.radians(0), math.radians(0)))
                camMatrix.translation = self.position
                self.cam.source = BigWorld.dcursor().matrix
                ident = Math.Matrix()
                ident.setIdentity()
                self.cam.target = camMatrix
                BigWorld.camera(self.cam)
                print '[FREECAMERA]: Installed'
                updateHandler = BigWorld.callback(0.001, lambda : self.onUpdateHookBtn()) #buttons 4 move
            if event.key == getattr(Keys, 'KEY_U') and event.isKeyDown():
                BigWorld.camera(self.aircam)
                self.aircam = None

            if event.key == getattr(Keys, 'KEY_N') and event.isKeyDown(): #nearest
                cam1 = BigWorld.CursorCamera()
                cam1.target = self.get_nearest().matrix
                cam1.source = BigWorld.dcursor().matrix
                BigWorld.camera(cam1)

            if event.key == getattr(Keys, 'KEY_B') and event.isKeyDown(): #nearest model
                cam1 = BigWorld.CursorCamera()
                cam1.target = self.get_nearest_model().matrix
                cam1.source = BigWorld.dcursor().matrix
                BigWorld.camera(cam1)
            

cam = FreeCamera()
