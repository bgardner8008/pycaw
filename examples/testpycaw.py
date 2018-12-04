
from ctypes import cast, POINTER
import comtypes
#from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#==============================================================================
# Wrapper functions around pycaw

class AudioDeviceError(Exception):
    pass

def findActiveAudioDeviceByName(devName):
    devices = AudioUtilities.GetAllActiveDevices()
    for dev in devices:
        if dev.FriendlyName == devName:
            return dev
    raise AudioDeviceError("can't find active audio device '{}'".format(devName))

def findAudioDeviceByName(devName):
    devices = AudioUtilities.GetAllDevices()
    for dev in devices:
        if dev.FriendlyName == devName:
            return dev
    raise AudioDeviceError("can't find audio device '{}'".format(devName))

def setDevVolume(dev, vol):
    interface = dev.immdevice.Activate(IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(vol, None)

def setVolume(devName, vol):
    setDevVolume(findActiveAudioDeviceByName(devName), vol)

def getDevVolume(dev):
    interface = dev.immdevice.Activate(IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume.GetMasterVolumeLevelScalar()

def getVolume(devName):
   return getDevVolume(findActiveAudioDeviceByName(devName))

#==============================================================================

def testSetVol(devName, vol):
    vol0 = getVolume(devName)
    print("orig vol: {}".format(vol0))
    print("setting vol to {}".format(vol))
    setVolume(devName, vol)
    vol0 = getVolume(devName)
    print("after setting, vol: {}".format(vol0))

dev = AudioUtilities.GetDefaultSpeaker()
print("default speaker: {}".format(dev.FriendlyName))
testSetVol(dev.FriendlyName, 0.66)

dev = AudioUtilities.GetDefaultMicrophone()
print("default mic: {}".format(dev.FriendlyName))
testSetVol(dev.FriendlyName, 0.33)
