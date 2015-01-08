import BigWorld, Math
import Keys
import GlobalEvents
import gui.ClientHangarSpace as space
import math
import GUI


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
        self.left = 0
        self.right = 0
        self.a = 20
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
            self.cam.invViewProvider.b = camMatrix
            #matrix = Math.Matrix(BigWorld.dcursor().matrix)
            #maxrix.setRotateYPR(myaw(), mpitch(), matrix.roll)
            #self.cam.invViewProvider.a = maxrix
        except:
            pass

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
            self.cam.invViewProvider.a = BigWorld.player().matrix
        self.SetPosition()
        
        return

    def onUpdateHookBtn(self):
        if self.aircam != None:
            self.btn()
            updateHandler = BigWorld.callback(0.001, lambda : self.onUpdateHookBtn())

    def get_cam(self):
        return self.cam
    
    def handleKeyEvent(self, event):
        if event.key == getattr(Keys, 'KEY_P') and event.isKeyDown():
            self.delta += 0.05 #increase speed
        if event.key == getattr(Keys, 'KEY_L') and event.isKeyDown():
            self.delta -= 0.05 #decrease speed
            self.delta = max(self.delta,0)
        if event.key == getattr(Keys, 'KEY_Y') and event.isKeyDown(): #setting new cam
            self.aircam = BigWorld.camera()
            self.cam = BigWorld.FreeCamera() #saving old cam
            self.onUpdateHookBtn()
            self.position = BigWorld.player().position
            self.position = Math.Vector3(BigWorld.camera().position.x, BigWorld.camera().position.y, BigWorld.camera().position.z)
            self.label = GUI.Text('')
            matrix = Math.Matrix(BigWorld.dcursor().matrix)          

            self.cam.invViewProvider = Math.MatrixProduct()
            camMatrix = Math.Matrix()
            camMatrix.setRotateYPR((math.radians(0), math.radians(0), math.radians(0)))
            camMatrix.translation = self.position
            self.cam.invViewProvider.a = BigWorld.dcursor().matrix
            ident = Math.Matrix()
            ident.setIdentity()
            self.cam.invViewProvider.b = camMatrix
            BigWorld.camera(self.cam)
            print '[FREECAMERA]: Installed'
            updateHandler = BigWorld.callback(0.001, lambda : self.onUpdateHookBtn()) #buttons 4 move
        if event.key == getattr(Keys, 'KEY_U') and event.isKeyDown():
            BigWorld.camera(self.aircam)
            self.aircam = None

cam = FreeCamera()
