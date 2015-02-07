__author__ = 'Pieter'
'''
Created on 19 jan. 2014

@author: Pieter
'''

import sys,time, objects
from pygame.locals import *
from objects.Objects import klassiekBord
from objects import *
FPS = 60

def buildBord():
    bord = klassiekBord()
    bord.init()
    # cell = Memcel()
    # schakelaarA = pygame.image.load("Drukknop.png").convert()
    # recta = schakelaarA.get_rect()
    # recta.topleft = (0,0)
    # bord.blit(schakelaarA,recta)
    # schakelaarB = pygame.image.load("Drukknop.png").convert()
    # rect = schakelaarB.get_rect()
    # rect.topleft = recta.bottomleft
    # bord.blit(schakelaarB,rect)
    # enInA = pygame.Rect(201,154,17,17)
    # enInB = pygame.Rect(201,202,17,17)
    # schakOutA = pygame.Rect(161,26,17,17)
    # schakOutB = pygame.Rect(161,90,17,17)
    # schakOutC = pygame.Rect(161,155,17,17)
    # outs = [schakOutA, schakOutB, schakOutC]
    # ins = [enInA, enInB]
    return bord, bord.ins, bord.outs
def main():
    pygame.display.set_caption('Systeembord')
    line=None
    isDown=None
    start=None
    current = None
    bord, ins, outs = buildBord()
    startblokje=None
    change = False
    vasthoudknop = None
    sliding=False
    slideblock=None
    lastpos=None
    pulsticked=[]

    while True:
            checkForQuit()
            if pulsticked:
                for out in pulsticked:
                    out.set(LOW)
                pulsticked=[]
                change=True

            # Get Left mouse button down
            for event in pygame.event.get():
                if event.type==MOUSEBUTTONDOWN and event.button==1:
                    cur=event.pos
                    # check if it's on an output port
                    for out in outs:
                        offx, offy = out.surf.get_abs_offset()
                        if out.surf.get_rect().collidepoint(cur[0]-offx,cur[1]-offy):
                            #if on an output set starting point for temporary line
                            start = out.surf.get_rect().center
                            start = (start[0]+offx,start[1]+offy)
                            startblokje = out
                            #setting isDown so we know we're dragging
                            isDown=True
                            break

                    else:
                        #check to see if clicked on a button
                        for i in [x for x in ins if x.__class__== objects.Objects.KnopWaarde]:
                            offx, offy = i.surf.get_abs_offset()
                            if i.surf.get_rect().collidepoint(cur[0] - offx, cur[1] - offy):
                                #if it's a button activate it.
                                i.set(HIGH)
                                change = True
                                vasthoudknop = i
                                isDown = True
                                break
                        # check to see if we're on a slider
                        for i in [x for x in ins if x.__class__== objects.Objects.Slider]:
                            offx, offy = i.surf.get_abs_offset()
                            if i.surf.get_rect().collidepoint(cur[0] - offx, cur[1] - offy):
                                # if so start sliding it
                                slideblock=i
                                sliding=True
                                lastpos=cur

                # check left mous button up
                if event.type==MOUSEBUTTONUP and event.button==1:
                    current =event.pos
                    # if we're dragging it's an output, button or slider
                    if isDown:
                        # stop dragging
                        isDown=False
                        line=False
                        for i in ins:
                            offx, offy = i.surf.get_abs_offset()
                            # checking if the end of the drag is a valid input. Valid is of the same datatype (analog or digital)
                            if (i.surf.get_rect().collidepoint(current[0]-offx,current[1]-offy) and ((startblokje.__class__==i.__class__) or (startblokje.__class__==objects.Objects.WaardeVakje and i.__class__==objects.Objects.AanUitKnop))):
                                # if so, reset the temp start point
                                start=None
                                current=None
                                tmpcon = (startblokje,i)
                                # check if the connection already exists
                                for con in bord.connections:
                                    if tmpcon==con:
                                        break
                                    # or the input is already occupied
                                    elif i in con:
                                        break
                                else:
                                    #add to the connectionlist and notify a special button
                                    bord.connections.append((startblokje,i))
                                    if i.__class__==objects.Objects.AanUitKnop:
                                        i.notifyconnect()
                                    change=True
                                break
                        # if it's not a valid output
                        else:
                            # release the button if we';re dragging that
                            if vasthoudknop:
                                vasthoudknop.set(LOW)
                                vasthoudknop=None
                                change=True
                                isDown=False
                                break
                    # stop operating a slider
                    if sliding:
                        pass
                        change=True
                        sliding=False

                # dragging mouse while started from an output
                if event.type==MOUSEMOTION and isDown and start:
                    current =event.pos
                    line = True

                # dragging mouse when started on a slider
                if event.type==MOUSEMOTION and sliding:
                    cur=event.pos
                    deltax=cur[0]-lastpos[0]
                    slideblock.set(slideblock.calculateValue(deltax))
                    lastpos=cur
                    change=True

                # release of right mouse button
                if event.type==MOUSEBUTTONUP and event.button==3:
                    cur=event.pos
                    for out in outs:
                        offx, offy = out.surf.get_abs_offset()
                        if out.surf.get_rect().collidepoint(cur[0]-offx,cur[1]-offy):
                            # print mouse on an output, removing last made link from this output"
                            for i in range(len(bord.connections)-1,-1,-1):
                                if bord.connections[i][0]==out:
                                    bord.connections[i][1].set(LOW)
                                    if bord.connections[i][1].__class__==objects.Objects.AanUitKnop:
                                        bord.connections[i][1].notifydisconnect()
                                    bord.connections.pop(i)
                                    change=True
                                    break

                    # NOt an ouput that has a connection. switching buttons
                    else:
                        # print "switch knopstatus"
                        for i in [x for x in ins if x.__class__== objects.Objects.KnopWaarde]:
                            offx, offy = i.surf.get_abs_offset()
                            if i.surf.get_rect().collidepoint(cur[0]-offx,cur[1]-offy):
                                i.set(not i.waarde)
                                change=True
                                break

                #checking if the clock ticked
                for i in range(1,10,1):
                    if event.type==USEREVENT+i:
                        for out in [x for x in outs if x.__class__==objects.Objects.WaardeVakje and x.id]:
                            if out.id==i:
                                out.set(HIGH)
                                change=True
                                pulsticked.append(out)

                # press r to reset board
                if event.type==KEYUP and event.key==K_r:
                    bord.connections=[]
                    for i in [x for x in ins if x.__class__==objects.Objects.WaardeVakje]:
                        i.set(HIGH)
                        i.set(LOW)
                    for i in [x for x in ins if x.__class__==objects.Objects.Slider]:
                        i.set(2.5)
                    for out in [x for x in outs if x.__class__==objects.Objects.WaardeVakje and x.id]:
                        out.par.inA.set(1)
            if change:
                bord.loopconnections()
                bord.loopconnections()
                bord.loopconnections()
                change=False
            DISPLAYSURF.fill(ACHTERGROND)
            DISPLAYSURF.blit(bord.surf, bord.surf.get_rect())
            fps=FPSCLOCK.get_fps()
            surf, rect = drawText("FPS: " + str(fps),BASICFONT,RED)
            rect.bottomright = (720, 512)
            DISPLAYSURF.blit(surf, rect)
            #drawing connection
            for o,i in bord.connections:
                offxo, offyo = o.surf.get_abs_offset()
                offxi, offyi = i.surf.get_abs_offset()
                xo, yo = o.surf.get_rect().center
                xi, yi = i.surf.get_rect().center
                pygame.draw.line(DISPLAYSURF,RED,(xo+offxo, yo+offyo),(xi+offxi,yi+offyi),3)

            if line==True:
                pygame.draw.line(DISPLAYSURF,RED,start,current)
            pygame.display.update()
            FPSCLOCK.tick_busy_loop(FPS)

def checkForQuit():
    # Terminates the program if there are any QUIT or escape key events.
    for event in pygame.event.get(QUIT): # get all the QUIT events
        pygame.quit() # terminate if any QUIT events are present
        sys.exit()
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            pygame.quit() # terminate if the KEYUP event was for the Esc key
            sys.exit()
        pygame.event.post(event) # put the other KEYUP event objects back


if __name__ == '__main__':
    main()
