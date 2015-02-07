from objects import *
import pygame,sys,time
from pygame.locals import *

class Bord():
    def __init__(self):
        DISPLAYSURF=pygame.display.set_mode(self.size)
        self.ins=[]
        self.outs=[]
        self.knoppen=[]
        self.connections=[]
        self.items=[]
        self.surf = pygame.Surface(self.size)
        self.surf.fill(ACHTERGROND)

    def init(self):
        for it in self.items:
            self.ins.extend(it.ins)
            self.outs.extend(it.outs)

    def loopconnections(self):
        for o, i in self.connections:
            i.set(o.waarde)

class klassiekBord(Bord):
    def __init__(self):
        self.size = (720,512)
        Bord.__init__(self)
        self.items.append(Sensor(self,(0,0)))
        self.items.append(Sensor(self,(0,96)))
        self.items.append(Sensor(self,(0,192)))
        self.items.append(Drukknop(self,(0,288)))
        self.items.append(Drukknop(self,(0,352)))
        self.items.append(AndPort(self,(192,128)))
        self.items.append(OrPort(self,(360,128)))
        self.items.append(Memcel(self,(192,256)))
        self.items.append(Invertor(self,(360,256)))
        self.items.append(Comperator(self,(360,0)))
        self.items.append(Transistor(self,(192,0)))
        self.items.append(Pulsgenerator(self,(0,448),id=1))
        self.items.append(LED(self,(528,0)))
        self.items.append(LED(self,(528,64)))
        self.items.append(LED(self,(528,128)))
        self.items.append(LED(self,(528,192)))
        self.items.append(Zoemer(self,(528,256)))
        self.items.append(Teller(self,(192,384)))
        self.items.append(Uitleg(self,(528,384)))

class Sensor():
    def __init__(self,par,topleft):
        self.size = (192,96)
        self.im = pygame.image.load(os.path.join("Items","Sensor.png")).convert()
        tmp = self.im.get_rect()
        tmp.topleft = topleft
        self.surf = par.surf.subsurface(tmp)
        self.surf.blit(self.im,(0,0))
        self.out = AnalogeWaarde(self,0.0,(161,41))
        self.inA = Slider(self,2.5,(12,41))
        self.ins = [self.inA]
        self.outs=[self.out]
        self.lasttextrect=(2,2,1,1)
        self.refresh()

    def refresh(self):
        # print "refreshing",self
        self.out.set(self.inA.waarde)
        self.surf.set_clip(self.lasttextrect)
        self.surf.fill((240,240,240))
        self.surf.set_clip(None)
        surf,rect = drawText(str(self.inA.waarde)+" V",BASICFONT,RED)
        rect.topleft = (62,62)
        self.surf.blit(surf,rect)
        self.lasttextrect=rect

class Drukknop():
    def __init__(self,par,topleft):
        self.size = (192,64)
        self.im = pygame.image.load(os.path.join("Items","Drukknop.png")).convert()
        tmp = self.im.get_rect()
        tmp.topleft = topleft
        self.surf = par.surf.subsurface(tmp)
        self.surf.blit(self.im,(0,0))
        self.out = WaardeVakje(self, LOW,(160,24))
        self.inA = KnopWaarde(self, LOW,(16,24))
        self.outs = [self.out]
        self.ins=[self.inA]

    def refresh(self):
        # print "refreshing",self
        self.out.set(self.inA.waarde)

class LED():
    def __init__(self,par,topleft):
        self.size = (192,64)
        self.im = pygame.image.load(os.path.join("Items","Led.png")).convert()
        self.aan = pygame.image.load(os.path.join("Items","Ledaan.png")).convert()
        tmp = self.im.get_rect()
        tmp.topleft = topleft
        self.surf = par.surf.subsurface(tmp)
        self.surf.blit(self.im,(0,0))
        self.inA = WaardeVakje(self, LOW,(16,24))
        self.outs = []
        self.ins=[self.inA]

    def refresh(self):
        self.surf.blit(self.im,(0,0))
        if self.inA.waarde:
            self.surf.blit(self.aan,(160,24))

class Uitleg():
     def __init__(self,par,topleft):
        self.size = (192,96)
        self.im = pygame.image.load(os.path.join("Items","Uitleg.png")).convert()
        tmp = self.im.get_rect()
        tmp.topleft = topleft
        self.surf = par.surf.subsurface(tmp)
        self.surf.blit(self.im,(0,0))
        self.outs = []
        self.ins=[]

class Zoemer(object):
    def __init__(self,par,topleft):
        self.size = (192,128)
        self.im = pygame.image.load(os.path.join("Items","Zoemer.png")).convert()
        tmp = self.im.get_rect()
        tmp.topleft = topleft
        self.surf = par.surf.subsurface(tmp)
        self.surf.blit(self.im,(0,0))
        self.inA = WaardeVakje(self, LOW,(16,48))
        self.outs = []
        self.ins=[self.inA]

    def refresh(self):
        if self.inA.waarde:
            beep.play(loops=-1)
        else:
            beep.stop()

class Memcel():
    def __init__(self,par,topleft):
        self.size = (168,128)
        self.im = pygame.image.load(os.path.join("Items","Geheugencel.png")).convert()
        tmp = self.im.get_rect()
        tmp.topleft = topleft
        self.surf = par.surf.subsurface(tmp)
        self.surf.blit(self.im,(0,0))
        self.inA = WaardeVakje(self, LOW,(8,24))
        self.inB = WaardeVakje(self, LOW, (8,72))
        self.out = WaardeVakje(self, LOW,(144,48))
        self.ins=[self.inA, self.inB]
        self.outs = [self.out]

    def refresh(self):
        # print "refreshing",self
        if self.inA.waarde:
            self.out.set(HIGH)
        elif self.inB.waarde:
            self.out.set(LOW)

class AndPort():
    def __init__(self,par,topleft):
        self.size = (168,128)
        self.im = pygame.image.load(os.path.join("Items","Enpoort.png")).convert()
        tmp = self.im.get_rect()
        tmp.topleft = topleft
        self.surf = par.surf.subsurface(tmp)
        self.surf.blit(self.im,(0,0))
        self.inA = WaardeVakje(self, LOW,(8,24))
        self.inB = WaardeVakje(self, LOW, (8,72))
        self.out = WaardeVakje(self, LOW,(144,48))
        self.ins=[self.inA, self.inB]
        self.outs = [self.out]


    def refresh(self):
        self.out.set(self.inA.waarde and self.inB.waarde)

class OrPort():
    def __init__(self,par,topleft):
        self.size = (168,128)
        self.im = pygame.image.load(os.path.join("Items","Ofpoort.png")).convert()
        tmp = self.im.get_rect()
        tmp.topleft = topleft
        self.surf = par.surf.subsurface(tmp)
        self.surf.blit(self.im,(0,0))
        self.inA = WaardeVakje(self, LOW,(8,24))
        self.inB = WaardeVakje(self, LOW, (8,72))
        self.out = WaardeVakje(self, LOW,(144,48))
        self.ins=[self.inA, self.inB]
        self.outs = [self.out]

    def refresh(self):
        self.out.set(self.inA.waarde or self.inB.waarde)

class Invertor():
    def __init__(self,par,topleft):
        self.size = (168,128)
        self.im = pygame.image.load(os.path.join("Items","Invertor.png")).convert()
        tmp = self.im.get_rect()
        tmp.topleft = topleft
        self.surf = par.surf.subsurface(tmp)
        self.surf.blit(self.im,(0,0))
        self.inA = WaardeVakje(self, LOW,(8,48))
        self.out = WaardeVakje(self, HIGH,(144,48))
        self.ins=[self.inA]
        self.outs = [self.out]

    def refresh(self):
        self.out.set(not self.inA.waarde)

class Transistor():
    def __init__(self,par,topleft):
        self.size = (192,96)
        self.im = pygame.image.load(os.path.join("Items","Transistor.png")).convert()
        tmp = self.im.get_rect()
        tmp.topleft = topleft
        self.surf = par.surf.subsurface(tmp)
        self.surf.blit(self.im,(0,0))
        self.out = AnalogeWaarde(self,5.0,(145,25))
        self.inA = AnalogeWaarde(self,0.0,(9,25))
        self.ins = [self.inA]
        self.outs=[self.out]
        self.refresh()

    def refresh(self):
        # print "refreshing",self
        self.out.set(5.0-self.inA.waarde)

class Comperator():
    def __init__(self,par,topleft):
        self.size = (192,96)
        self.im = pygame.image.load(os.path.join("Items","Comperator.png")).convert()
        tmp = self.im.get_rect()
        tmp.topleft = topleft
        self.surf = par.surf.subsurface(tmp)
        self.surf.blit(self.im,(0,0))
        self.out = WaardeVakje(self,LOW,(144,24))
        self.inA = AnalogeWaarde(self,0.0,(9,25))
        self.inB = Slider(self,2.5,(50,74))
        self.ins = [self.inA, self.inB]
        self.outs=[self.out]
        self.lasttextrect=(2,2,1,1)
        self.refresh()

    def refresh(self):
        # print "refreshing",self
        self.out.set(self.inA.waarde>=self.inB.waarde)
        self.surf.set_clip(self.lasttextrect)
        self.surf.fill((240,240,240))
        self.surf.set_clip(None)
        surf,rect = drawText(str(self.inB.waarde)+" V",BASICFONT,RED)
        rect.topleft = (90,100)
        self.surf.blit(surf,rect)
        self.lasttextrect=rect

class Pulsgenerator():
    def __init__(self,par,topleft,id=1):
        self.id=id
        self.size = (192,64)
        self.im = pygame.image.load(os.path.join("Items","Pulsgenerator.png")).convert()
        tmp = self.im.get_rect()
        tmp.topleft = topleft
        self.surf = par.surf.subsurface(tmp)
        self.surf.blit(self.im,(0,0))
        self.inA = Slider(self,1,(12,24),mini=1, maxi=10)
        self.out= WaardeVakje(self,LOW,(160,24),id=self.id)
        self.ins = [self.inA]
        self.outs=[self.out]
        self.lasttextrect=(2,2,1,1)
        self.refresh()

    def refresh(self):
        # print "refreshing",self
        pygame.time.set_timer(USEREVENT+self.id,1000/int(self.inA.waarde))
        self.surf.set_clip(self.lasttextrect)
        self.surf.fill((240,240,240))
        self.surf.set_clip(None)
        surf,rect = drawText(str(int(self.inA.waarde))+" Hz",BASICFONT,RED)
        rect.topleft = (58,45)
        self.surf.blit(surf,rect)
        self.lasttextrect=rect

class Teller():
    def __init__(self,par,topleft):
        self.size = (226,128)
        self.counter=0
        self.wasHoog=False
        self.im = pygame.image.load(os.path.join("Items","Teller.png")).convert()
        tmp = self.im.get_rect()
        tmp.topleft = topleft
        self.surf = par.surf.subsurface(tmp)
        self.surf.blit(self.im,(0,0))
        self.inA = WaardeVakje(self,LOW,(16,16))
        self.inB = AanUitKnop(self,LOW,(16,48))
        self.inC = WaardeVakje(self,LOW,(16,80))
        self.inD = KnopWaarde(self,LOW,(149,80))
        self.ins = [self.inA,self.inB,self.inC, self.inD]
        self.outA = WaardeVakje(self,LOW,(304,16))
        self.outB = WaardeVakje(self,LOW,(272,16))
        self.outC = WaardeVakje(self,LOW,(240,16))
        self.outD = WaardeVakje(self,LOW,(208,16))
        self.outs=[self.outA,self.outB,self.outC,self.outD]
        self.lasttextrect=(2,2,1,1)
        self.refresh()

    def refresh(self):
        # print "refreshing",self
        # self.out.set(self.inA.waarde)
        if self.inC.waarde or self.inD.waarde:
                self.counter=0
        if (self.inB.connected and self.inB.waarde) or not self.inB.connected:
            if self.inA.waarde and not self.wasHoog:
                self.count()
                self.wasHoog=True
            if not self.inA.waarde and self.wasHoog:
                self.wasHoog=False
        # outputs
        bits =  bin(16+self.counter)[-1:2:-1]
        for i in range(4):
            if bits[i]=="1":
                self.outs[i].set(True)
            else:
                self.outs[i].set(False)
        # drawing
        self.surf.set_clip(self.lasttextrect)
        self.surf.fill((240,240,240))
        self.surf.set_clip(None)
        surf,rect = drawText(str(self.counter),FONTBIG,RED)
        rect.center = (295,71)
        self.surf.blit(surf,rect)
        self.lasttextrect=rect


    def count(self):
        self.counter+=1
        if self.counter>9:self.counter=0

class WaardeVakje():
    def __init__(self,par,waarde, topleft,id=None):
        self.id=id
        self.waarde = waarde
        self.aan = pygame.image.load(os.path.join("Items","WaardeVakjeAan.png"))
        self.uit = pygame.image.load(os.path.join("Items","WaardevakjeUit.png"))
        tmprect = self.uit.get_rect()
        tmprect.topleft=topleft
        self.par = par
        self.surf = self.par.surf.subsurface(tmprect)
        self.topleft=topleft
        self.refresh()

    def refresh(self):
        # print "refreshing",self
        if self.waarde:
            self.surf.blit(self.aan,(0,0))
        else:
            self.surf.blit(self.uit,(0,0))

    def set(self,waarde):
        if waarde != self.waarde:
            # print "setting",self,"to",waarde
            self.waarde = waarde
            self.par.refresh()
            self.refresh()

class AanUitKnop(WaardeVakje):
    def __init__(self,par,waarde, topleft,id=None):
        WaardeVakje.__init__(self,par,waarde, topleft,id=None)
        self.connected = False
    def notifyconnect(self):
        self.connected=True
    def notifydisconnect(self):
        self.connected=False

class KnopWaarde(WaardeVakje):
    def __init__(self,par,waarde, topleft):
        WaardeVakje.__init__(self,par,waarde, topleft)
        self.aan = pygame.Surface((17,17))
        self.uit = pygame.Surface((17,17))
        self.aan.fill(BLUE)
        self.uit.fill(DARKBLUE)
        self.refresh()

class AnalogeWaarde(WaardeVakje):
    def __init__(self,par,waarde, topleft):
        self.waarde = waarde
        self.im = pygame.Surface((15,15))
        self.tmprect = self.im.get_rect()
        self.tmprect.topleft=topleft
        self.par = par
        self.surf = self.par.surf.subsurface(self.tmprect)
        self.refresh()

    def refresh(self):
        # print "refreshing",self
        colorval = int(((127*self.waarde)/5)+128)
        self.im.fill((colorval,colorval,0))
        self.surf.blit(self.im,(0,0))

class Slider(WaardeVakje):
    def __init__(self,par,waarde, topleft,width=115,mini=0.0, maxi=5.0):
        self.waarde = waarde
        self.width=width
        self.mini=mini
        self.maxi=maxi
        self.par = par
        self.topleft=topleft
        self.im = pygame.image.load(os.path.join("Items","Sliderachtergrond.png")).convert()
        self.button = pygame.Surface((15,15))
        self.button.fill(BLUE)
        self.imrect = self.im.get_rect()
        self.imrect.width=width
        self.im.set_clip(self.imrect)
        self.imrect.topleft=self.topleft
        self.surf = self.par.surf.subsurface(self.imrect)
        self.curpos=None
        self.refresh()

    def refresh(self):
        xval = int((self.width-15)*self.waarde)/self.maxi
        self.curpos = self.button.get_rect()
        self.curpos.left += xval
        self.but = self.surf.subsurface(self.curpos)
        self.surf.blit(self.im,(0,0))
        self.but.blit(self.button,(0,0))

    def calculateValue(self,deltax):
        tmp = float(self.curpos.left + deltax)
        val = (tmp*self.maxi)/float(self.width-15)
        if val < self.mini: val = self.mini
        if val > self.maxi: val = self.maxi
        return val


