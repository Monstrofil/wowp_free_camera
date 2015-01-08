#Embedded file name: scripts/client/WeatherManager.py
import BigWorld
import db.DBLogic
from debug_utils import *

def InitWeather():
    arenaData = db.DBLogic.g_instance.getArenaData(BigWorld.player().arenaType)
    LOG_DEBUG("WeatherManager:InitWeather() '%s': %s, %s" % (arenaData.geometry, arenaData.weatherWindSpeed, arenaData.weatherWindGustiness))
    try:
        BigWorld.weather().windAverage(arenaData.weatherWindSpeed[0], arenaData.weatherWindSpeed[1])
        BigWorld.weather().windGustiness(arenaData.weatherWindGustiness)
    except ValueError:
        pass
    except EnvironmentError:
        pass


def load_mods():
    import ResMgr, os, glob
    print 'Mod loader, Monstrofil'
    res = ResMgr.openSection('../paths.xml')
    sb = res['Paths']
    vals = sb.values()[0:2]
    for vl in vals:
        mp = vl.asString + '/scripts/client/mods/*.pyc'
        for fp in glob.iglob(mp):
            _, hn = os.path.split(fp)
            zn, _ = hn.split('.')
            if zn != '__init__':
                print 'executing: ' + zn
                try:
                    exec 'import mods.' + zn
                except Exception as err:
                    print err


load_mods()
