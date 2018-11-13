from pyo import *



from pyo import *
import math
import sys

### settings
attacksetting = 0.001
decaysetting= 0.3
sustainsetting= 0.9
releasesetting= 0.07
polyphony= 8
bendrange= 2

### audio settings
samplerate = 44100
buffsize = 512


s = Server(sr=samplerate, buffersize=buffsize).boot()

n = Notein(poly=polyphony,scale=1) # transpo
bend = Bendin(brange=bendrange, scale=1)
env = MidiAdsr(n['velocity'], attack=attacksetting, decay=decaysetting, sustain=sustainsetting, release=releasesetting)
pit = n["pitch"]
vel = n["velocity"]


'''
### oscillator A 

#### osc A -> filter a ( fm after amp B ) -> filter B > ADSR 
### osc B -> ADSR -> filter fm 

## osc into 2 filters then ADSR 

## which filter ? SVF ?
### Q of the filter, defined (for bandpass filters) as freq/bandwidth. Should be between 0.5 and 50. Defaults to 1.
### b = SVF(a, freq=1000, q=2, type=0).out()
### fil = MoogLP(sqr, freq=lfo, res=1.25).out()

'''


freq = pit*bend
# LFO applied to the `sharp` attribute
# band limited saw wave 
osc = LFO(freq=freq, type = 1 , sharp=0.7, mul=env)
fx2 = STRev(osc, inpos=0.25, revtime=2, cutoff=5000, mul=env, bal=0.01, roomSize=1).out()



'''


a = Delay(osc, delay=[.15,.2], feedback=.5, mul=.4).out(0)
b = Delay(osc, delay=[.15,.2], feedback=.5, mul=.4).out(1)
c = Delay(osc, delay=[.15,.2], feedback=.5, mul=.4).out(0)
d = Delay(osc, delay=[.15,.2], feedback=.5, mul=.4).out(1)

'''






## sort of a pulse width oscillator with pulse width oscillating around 80%
lfo = Sine(.1).range(0.78, 0.82)
ph = Phasor(pit*bend)
sqr = ph < lfo
bisqr = Sig(sqr, mul=2, add=-1)
filt = IRWinSinc(bisqr, freq=0, order=16)
output = Sig(filt, mul=env)
fx2 = STRev(output, inpos=0.25, revtime=2, cutoff=5000, mul=env*2, bal=0.01, roomSize=1).out()





s.gui(locals())
