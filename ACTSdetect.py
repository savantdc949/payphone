import wave
import struct
import math
import sys

class pygoertzel_dtmf:
    def __init__(self, samplerate):
        self.samplerate = samplerate
        
        self.goertzel_freq = [1209.0,1336.0,1477.0,1633.0,2200.0,697.0,770.0,852.0,941.0,1700.0]
        self.s_prev = {}
        self.s_prev2 = {}
        self.totalpower = {}
        self.N = {}
        self.coeff = {}

        # create goertzel parameters for each frequency so that 
        # all the frequencies are analyzed in parallel
        for k in self.goertzel_freq:
            self.s_prev[k] = 0.0
            self.s_prev2[k] = 0.0
            self.totalpower[k] = 0.0
            self.N[k] = 0.0
            
            normalizedfreq = k / self.samplerate
            self.coeff[k] = 2.0*math.cos(2.0 * math.pi * normalizedfreq)

    def __get_number(self, freqs):
        hi = [1209.0,1336.0,1477.0,1633.0,2200.0]
        lo = [697.0,770.0,852.0,941.0,1700.0]
        # get hi freq
        hifreq = 0.0
        hifreq_v = 0.0
        for f in hi:
            if freqs[f]>hifreq_v:
                hifreq_v = freqs[f]
                hifreq = f
        
        # get lo freq
        lofreq = 0.0
        lofreq_v = 0.0
        for f in lo:
            if freqs[f]>lofreq_v:
                lofreq_v = freqs[f]
                lofreq = f
        if lofreq==697.0:
            if hifreq==1209.0:
                return "1"
        elif lofreq==770.0:
            if hifreq==1209.0:
                return "4"
            elif hifreq==1336.0:
                return "5"
            elif hifreq==1477.0:
                return "6"
            elif hifreq==1633.0:
                return "B"
        elif lofreq==852.0:
            if hifreq==1209.0:
                return "7"
            elif hifreq==1336.0:
                return "8"
            elif hifreq==1477.0:
                return "9"
            elif hifreq==1633.0:
                return "C"
        elif lofreq==941.0:
            if hifreq==1209.0:
                return "*"
            elif hifreq==1336.0:
                return "0"
            elif hifreq==1477.0:
                return "#"
            elif hifreq==1633.0:
                return "D" 
        elif lofreq==1700.0:
            if hifreq==2200.0:				
                return "R"
        
    def run(self, sample):
        freqs = {}
        for freq in self.goertzel_freq:
            s = sample + (self.coeff[freq] * self.s_prev[freq]) - self.s_prev2[freq]
            self.s_prev2[freq] = self.s_prev[freq]
            self.s_prev[freq] = s
            self.N[freq]+=1
            power = (self.s_prev2[freq]*self.s_prev2[freq]) + (self.s_prev[freq]*self.s_prev[freq]) - (self.coeff[freq]*self.s_prev[freq]*self.s_prev2[freq])
            self.totalpower[freq]+=sample*sample
            if (self.totalpower[freq] == 0): 
                self.totalpower[freq] = 1
            freqs[freq] = power / self.totalpower[freq] / self.N[freq]
        
        return self.__get_number(freqs)
        
if __name__ == '__main__':
    coincointer = 0
    dollars = 0
    # load wav file
    filename = sys.argv[1]
    wav = wave.open(filename, 'r')
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()

    frames = wav.readframes(nframes * nchannels)
    # convert wave file to array of integers
    frames = struct.unpack_from("%dH" % nframes * nchannels, frames)
    
    # if stereo get left/right
    if nchannels == 2:
        left = [frames[i] for i in range(0,len(frames),2)]
        right = [frames[i] for i in range(1,len(frames),2)]
    else:
        left = frames
        right = left
        
    binsize = 400
    # Split the bin in 4 to average out errors due to noise
    binsize_split = 4
    
    prevvalue = ""
    prevcounter = 0
    for i in range(0,len(left)-binsize,binsize/binsize_split):
        goertzel = pygoertzel_dtmf(framerate)
        for j in left[i:i+binsize]:
            value = goertzel.run(j)
        if value==prevvalue:
            prevcounter+=1
            if prevcounter==10:
                print value # This is where the tone digit is displayed to stdout
                coincointer = coincointer + 1
        else:
            prevcounter=0
            prevvalue=value

    dollars = str(coincointer * 0.25)

print 'Coin count:', coincointer
print '$' + dollars, 'has been inserted.'