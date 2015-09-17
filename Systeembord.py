#!/usr/bin/env python
"""
Created on 19 jan. 2014

@author: Pieter Schutz
Licensed with GPL.

"""

import sys
from pygame.locals import *
import objects
from objects.Objects import *
from objects import *
import Tkinter as tk
from tkFileDialog import askopenfilename, asksaveasfilename

__author__ = "Pieter Schutz"
__copyright__ = "Copyright 2015, Pieter Schutz"
__credits__ = ["Pieter Schutz"]
__license__ = "GPL"
__version__ = "0.3.0"
__maintainer__ = "Pieter Schutz"
__email__ = "schutz@ggh.nu"
__status__ = "Development"

def buildbord(boardclass, connections=None, values=None):
    bord = boardclass()
    if connections:
        bord.connections = connections
    if values:
        for i, it in values.items():
            bord.itemdict[i].value = it
            bord.itemdict[i].refresh()
            bord.itemdict[i].par.refresh()
    bord.loop_connections()
    return bord, bord.ins, bord.outs, bord.buttons


def main():
    display_surface = pygame.display.set_mode((200, 200))
    pygame.display.set_caption('Systeembord')
    line = None
    isdown = None
    start = None
    current = None
    bord, ins, outs, buttons = buildbord(ClassicBoard)
    startblokje = None
    change = False
    vasthoudknop = None
    sliding = False
    sliding_block = None
    last_position = None
    last_loop_ticked_pulses = []

    while True:
        check_for_quit()

        if last_loop_ticked_pulses:
            for out in last_loop_ticked_pulses:
                out.set(LOW)
            last_loop_ticked_pulses = []
            change = True

        # Get Left mouse button down
        for event in pygame.event.get(MOUSEBUTTONDOWN):
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                cur = event.pos
                # check if it's on an output port
                for out in outs:
                    offset_x, offset_y = out.surf.get_abs_offset()
                    if out.surf.get_rect().collidepoint(cur[0] - offset_x, cur[1] - offset_y):
                        # if on an output set starting point for temporary line
                        start = out.surf.get_rect().center
                        start = (start[0] + offset_x, start[1] + offset_y)
                        startblokje = out
                        # setting isdown so we know we're dragging
                        isdown = True
                        break

                else:
                    # check to see if clicked on a button
                    for i in [x for x in ins if x.__class__ == objects.Objects.ButtonValue]:
                        offset_x, offset_y = i.surf.get_abs_offset()
                        if i.surf.get_rect().collidepoint(cur[0] - offset_x, cur[1] - offset_y):
                            # if it's a button activate it.
                            i.set(HIGH)
                            change = True
                            vasthoudknop = i
                            isdown = True
                            break
                    # check to see if we're on a slider
                    for i in [x for x in ins if x.__class__ == objects.Objects.Slider]:
                        offset_x, offset_y = i.surf.get_abs_offset()
                        if i.surf.get_rect().collidepoint(cur[0] - offset_x, cur[1] - offset_y):
                            # if so start sliding it
                            sliding_block = i
                            sliding = True
                            last_position = cur

            # check left mouse button up
        for event in pygame.event.get(MOUSEBUTTONUP):
            if event.type == MOUSEBUTTONUP and event.button == 1:
                current = event.pos
                # if we're dragging it's an output, button or slider
                if isdown:
                    # stop dragging
                    isdown = False
                    line = False
                    for i in ins:
                        offset_x, offset_y = i.surf.get_abs_offset()
                        # checking if the end of the drag is a valid input.
                        # Valid is of the same data type (analog or digital)
                        if (i.surf.get_rect().collidepoint(current[0] - offset_x, current[1] - offset_y) and
                                ((startblokje.__class__ == i.__class__) or
                                     (startblokje.__class__ == objects.Objects.ValueField and
                                              i.__class__ == objects.Objects.OnOffButtonValue))):
                            # if so, reset the temp start point
                            start = None
                            current = None
                            tmp_connection = (startblokje.id, i.id)
                            # check if the connection already exists
                            for con in bord.connections:
                                if tmp_connection == con:
                                    break
                                # or the input is already occupied
                                elif i in con:
                                    break
                            else:
                                # add to the connection list and notify a special button
                                bord.connections.append((startblokje.id,i.id))
                                if i.__class__ == objects.Objects.OnOffButtonValue:
                                    i.notify_connect()
                                change = True
                            break
                    # if it's not a valid output
                    else:
                        # release the button if we';re dragging that
                        if vasthoudknop:
                            vasthoudknop.set(LOW)
                            vasthoudknop = None
                            change = True
                            isdown = False
                            break
                # stop operating a slider
                if sliding:
                    pass
                    change = True
                    sliding = False

                # Handling buttons
                for button in buttons:
                    if button[0].collidepoint(cur):
                        pygame.event.post(button[1])

                # release of right mouse button
            if event.type == MOUSEBUTTONUP and event.button == 3:
                cur = event.pos
                for out in outs:
                    offset_x, offset_y = out.surf.get_abs_offset()
                    if out.surf.get_rect().collidepoint(cur[0] - offset_x, cur[1] - offset_y):
                        # print mouse on an output, removing last made link from this output"
                        for i in range(len(bord.connections) - 1, -1, -1):
                            if bord.connections[i][0] == out.id:
                                bord.itemdict[bord.connections[i][1]].set(LOW)
                                if bord.itemdict[bord.connections[i][1]].__class__ == objects.Objects.OnOffButtonValue:
                                    bord.itemdict[bord.connections[i][1]].notify_disconnect()
                                bord.connections.pop(i)
                                change = True
                                break

                # Not an output that has a connection. switching buttons
                else:
                    # print "switch knopstatus"
                    for i in [x for x in ins if x.__class__ == objects.Objects.ButtonValue]:
                        offset_x, offset_y = i.surf.get_abs_offset()
                        if i.surf.get_rect().collidepoint(cur[0] - offset_x, cur[1] - offset_y):
                            i.set(not i.value)
                            change = True
                            break




            # dragging mouse while started from an output
        for event in pygame.event.get(MOUSEMOTION):
            if event.type == MOUSEMOTION and isdown and start:
                current = event.pos
                line = True

            # dragging mouse when started on a slider
            if event.type == MOUSEMOTION and sliding:
                cur = event.pos
                deltax = cur[0] - last_position[0]
                sliding_block.set(sliding_block.calculate_value(deltax))
                last_position = cur
                change = True


            # checking if the clock ticked
        for i in range(1, 5, 1):
            if pygame.event.peek(USEREVENT+i):
                event = pygame.event.get(USEREVENT+i)
                for out in [x for x in outs if x.__class__ == objects.Objects.ValueField and x.countid]:
                    if out.countid == i:
                        out.set(HIGH)
                        change = True
                        last_loop_ticked_pulses.append(out)
        
        for event in pygame.event.get(USEREVENT):
            if event.action == RESET:
                    bord.connections = []
                    for i in [x for x in ins if x.__class__ == objects.Objects.ValueField]:
                        i.set(HIGH)
                        i.set(LOW)
                    for i in [x for x in ins if x.__class__ == objects.Objects.Slider]:
                        i.set(2.5)
                    for out in [x for x in outs if x.__class__ == objects.Objects.ValueField and x.countid]:
                        out.par.inA.set(1)

            if event.action == BOARD:
                if type(bord) == event.code:
                    pass
                else:
                    bord, ins, outs, buttons = buildbord(event.code)
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT, action=RESET))
            if event.action == SAVE:
                options = {}
                options['defaultextension'] = ".sbs"
                options['filetypes'] = [('systeembord files', '.sbs'), ('all files', '.*')]
                options['title'] = 'Opslaan'
                options['initialfile'] = bord.__class__.__name__+'.sbs'
                root = tk.Tk()
                root.withdraw()
                file_path = asksaveasfilename(**options)
                if file_path:
                    with open(file_path, "w") as f:
                        f.write(repr(bord))
            if event.action == LOAD:
                options = {}
                options['defaultextension'] = ".sbs"
                options['filetypes'] = [('systeembord files', '.sbs'), ('all files', '.*')]
                root = tk.Tk()
                root.withdraw()
                file_path = askopenfilename(**options)
                if file_path:
                    with open(file_path, "r") as f:
                        loaded = eval(f.read())
                    bord, ins, outs, buttons = buildbord(loaded['board'], connections=loaded['connections'], values=loaded['values'])


        if change:
            bord.loop_connections()
            bord.loop_connections()
            change = False
        display_surface.fill(BACKGROUND)
        display_surface.blit(bord.surf, bord.surf.get_rect())
        fps = fps_clock.get_fps()
        # drawing connection
        for o, i in bord.connections:
            offset_x_out, offset_y_out = bord.itemdict[o].surf.get_abs_offset()
            offset_x_in, offset_y_in = bord.itemdict[i].surf.get_abs_offset()
            xo, yo = bord.itemdict[o].surf.get_rect().center
            xi, yi = bord.itemdict[i].surf.get_rect().center
            pygame.draw.line(display_surface, RED, (xo + offset_x_out, yo + offset_y_out),
                             (xi + offset_x_in, yi + offset_y_in), 3)

        if line:
            pygame.draw.line(display_surface, RED, start, current)
        pygame.display.update()
        # fps_clock.tick_busy_loop(FPS)


def check_for_quit():
    # Terminates the program if there are any QUIT or escape key events.
    for _ in pygame.event.get(QUIT):  # get all the QUIT events
        pygame.quit()  # terminate if any QUIT events are present
        sys.exit()
    for event in pygame.event.get(KEYUP):  # get all KEYUP events
        if event.key == K_ESCAPE:
            pygame.quit()  # terminate if the KEYUP event was for the Esc key
            sys.exit()
        pygame.event.post(event)  # put the other KEYUP event objects back


if __name__ == '__main__':
    main()
