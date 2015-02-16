"""Helper module for the systeembord emulator.

This module contains classes that build the visual and logic aspects for a systeembord emulation
Cannot be used standalone.

.. _Google Python Style Guide:
   http://google-styleguide.googlecode.com/svn/trunk/pyguide.html

"""
from pygame.locals import *
from objects import *


class Board(object):
    """Wrapper class for a Board.

   Attributes:
      ins (list of ValueField or children): All inputs on this Board.
      outs (list of ValueField or children): All inputs on this Board.
      outs (list of ValueField or children): All inputs on this Board.
      connections (list of tuples): Each item is a tuple of (ins[i], outs[j]).
      items (list of BordItem children): The items the board is build with.
      surf (Surface): The Pygame.Surface for this board.
    """
    def __init__(self):
        """Set the simulation window to the appropriate size and initialize lists.

        After setting this up it will call self._add_items() wich must be overridden by child.

        """
        width, height = self.size
        height += 50
        self.size = (width,height)
        # noinspection PyUnusedLocal
        display_surface = pygame.display.set_mode(self.size)
        self.ins = []
        self.outs = []
        self.connections = []
        self.items = []
        self.buttons= []
        self.surf = pygame.Surface(self.size)
        self.surf.fill(BACKGROUND)
        self._add_items()
        self._init()
        self._add_buttons()

    def _init(self):
        """Fill the ins and outs lists

        called only and immediately after the creation of a Board instance
        """
        for it in self.items:
            self.ins.extend(it.ins)
            self.outs.extend(it.outs)

    def _add_items(self):
        pass

    def _add_buttons(self):
        reset_surf,reset_rect = draw_text(" Reset ", font_medium, BLUE)
        reset_rect.bottomleft = (4,self.size[1]-4)
        self.surf.blit(reset_surf,reset_rect)
        self.buttons.append((reset_rect,pygame.event.Event(pygame.USEREVENT, action=RESET)))
        pygame.draw.rect(self.surf,BLACK,reset_rect,4)

        classic_board_surf, classic_board_rect = draw_text(" Classic Board ", font_medium, BLUE)
        classic_board_rect.bottomleft = self.buttons[-1][0].bottomright
        classic_board_rect.left += 8
        self.surf.blit(classic_board_surf, classic_board_rect)
        self.buttons.append((classic_board_rect, pygame.event.Event(pygame.USEREVENT, action=BOARD, code=ClassicBoard)))
        pygame.draw.rect(self.surf, BLACK, classic_board_rect, 4)

        new_board_surf, new_board_rect = draw_text(" New Board ", font_medium, BLUE)
        new_board_rect.bottomleft = self.buttons[-1][0].bottomright
        new_board_rect.left += 8
        self.surf.blit(new_board_surf, new_board_rect)
        self.buttons.append((new_board_rect, pygame.event.Event(pygame.USEREVENT, action=BOARD, code=NewBoard)))
        pygame.draw.rect(self.surf, BLACK, new_board_rect, 4)

        twocounter_board_surf, twocounter_board_rect = draw_text(" Two counters ", font_medium, BLUE)
        twocounter_board_rect.bottomleft = self.buttons[-1][0].bottomright
        twocounter_board_rect.left += 8
        self.surf.blit(twocounter_board_surf, twocounter_board_rect)
        self.buttons.append((twocounter_board_rect, pygame.event.Event(pygame.USEREVENT,action=BOARD, code=TwoCounters)))
        pygame.draw.rect(self.surf, BLACK, twocounter_board_rect, 4)

    def loop_connections(self):
        """Update the connections on the board

        Cycle through the connections list and set inputs to the same value as the connected output.
        """
        for o, i in self.connections:
            i.set(o.value)


class ClassicBoard(Board):
    """The classic Board

   Attributes:
      size (tuple): the dimensions of the board in (x, y)
    """
    def __init__(self):
        """Append all the items to the items list
        """
        self.size = (720, 512)
        Board.__init__(self)

    def _add_items(self):
        self.items.append(Sensor(self, (0, 0)))
        self.items.append(Sensor(self, (0, 96)))
        self.items.append(Sensor(self, (0, 192)))
        self.items.append(PushButton(self, (0, 288)))
        self.items.append(PushButton(self, (0, 352)))
        self.items.append(AndPort(self, (192, 128)))
        self.items.append(OrPort(self, (360, 128)))
        self.items.append(MemoryCell(self, (192, 256)))
        self.items.append(Invertor(self, (360, 256)))
        self.items.append(Comperator(self, (360, 0)))
        self.items.append(Transistor(self, (192, 0)))
        self.items.append(PulseGenerator(self, (0, 448), id=1))
        self.items.append(LED(self, (528, 0)))
        self.items.append(LED(self, (528, 64)))
        self.items.append(LED(self, (528, 128)))
        self.items.append(LED(self, (528, 192)))
        self.items.append(Buzzer(self, (528, 256)))
        self.items.append(Counter(self, (192, 384)))
        self.items.append(Explain(self, (528, 384)))


class NewBoard(Board):
    """The classic Board

   Attributes:
      size (tuple): the dimensions of the board in (x, y)
    """
    def __init__(self):
        """Append all the items to the items list
        """
        self.size = (720, 512)
        Board.__init__(self)

    def _add_items(self):
        self.items.append(Sensor(self, (0, 0)))
        self.items.append(Sensor(self, (0, 96)))
        self.items.append(PushButton(self, (0, 192)))
        self.items.append(PushButton(self, (0, 256)))
        self.items.append(Invertor(self, (24, 384)))
        self.items.append(PulseGenerator(self, (0, 320), id=1))
        self.items.append(Comperator(self, (360, 0)))
        self.items.append(Comperator(self, (192, 0)))
        self.items.append(AndPort(self, (192, 128)))
        self.items.append(AndPort(self, (360, 128)))
        self.items.append(MemoryCell(self, (192, 256)))
        self.items.append(OrPort(self, (360, 256)))
        self.items.append(Counter(self, (192, 384)))
        self.items.append(LED(self, (528, 0)))
        self.items.append(LED(self, (528, 64)))
        self.items.append(LED(self, (528, 128)))
        self.items.append(LED(self, (528, 192)))
        self.items.append(Buzzer(self, (528, 256)))
        self.items.append(Invertor(self, (528, 384)))


class TwoCounters(Board):
    """The classic Board

   Attributes:
      size (tuple): the dimensions of the board in (x, y)
    """
    def __init__(self):
        """Append all the items to the items list
        """
        self.size = (888, 512)
        Board.__init__(self)

    def _add_items(self):
        self.items.append(Sensor(self, (0, 0)))
        self.items.append(Sensor(self, (0, 96)))
        self.items.append(PushButton(self, (0, 192)))
        self.items.append(PushButton(self, (0, 256)))
        self.items.append(PulseGenerator(self, (0, 320), id=1))
        self.items.append(Comperator(self, (360, 0)))
        self.items.append(Comperator(self, (192, 0)))
        self.items.append(AndPort(self, (192, 128)))
        self.items.append(AndPort(self, (360, 128)))
        self.items.append(MemoryCell(self, (192, 256)))
        self.items.append(MemoryCell(self, (360, 256)))
        self.items.append(OrPort(self, (528, 0)))
        self.items.append(Invertor(self, (528, 128)))
        self.items.append(Invertor(self, (528, 256)))
        self.items.append(Counter(self, (0, 384)))
        self.items.append(PulseGenerator(self, (360, 384), id=2))
        self.items.append(Counter(self, (552, 384)))
        self.items.append(LED(self, (696, 0)))
        self.items.append(LED(self, (696, 64)))
        self.items.append(LED(self, (696, 128)))
        self.items.append(LED(self, (696, 192)))
        self.items.append(Buzzer(self, (696, 256)))



class BordItem(object):
    """Wrapper for items on the Board
    """
    def __init__(self, par, topleft):
        """Set basic variables present in every item

        Blits the Image as subsurface to the Board and initializes empty lists
        Arguments:
            par (objects.Objects.Board or children): The parent board this item is placed on
            topleft (tulple): the topleft position on the board as ints (x, y)
        """
        tmp = self.im.get_rect()
        tmp.topleft = topleft
        self.surf = par.surf.subsurface(tmp)
        self.surf.blit(self.im, (0, 0))
        self.ins = []
        self.outs = []


class Sensor(BordItem):
    def __init__(self, par, topleft):
        self.im = pygame.image.load(os.path.join("Items", "Sensor.png")).convert()
        BordItem.__init__(self, par, topleft)
        self.out = AnalogValue(self, 0.0, (161, 41))
        self.inA = Slider(self, 2.5, (12, 41))
        self.ins = [self.inA]
        self.outs = [self.out]
        self.lasttextrect = (2, 2, 1, 1)
        self.refresh()

    def refresh(self):
        self.out.set(self.inA.value)
        self.surf.set_clip(self.lasttextrect)
        self.surf.fill((240, 240, 240))
        self.surf.set_clip(None)
        surf, rect = draw_text(str(self.inA.value) + " V", font_small, RED)
        rect.topleft = (62, 62)
        self.surf.blit(surf, rect)
        self.lasttextrect = rect


class PushButton(BordItem):
    def __init__(self, par, topleft):
        self.im = pygame.image.load(os.path.join("Items", "Drukknop.png")).convert()
        BordItem.__init__(self, par, topleft)
        self.out = ValueField(self, LOW, (160, 24))
        self.inA = ButtonValue(self, LOW, (16, 24))
        self.outs = [self.out]
        self.ins = [self.inA]

    def refresh(self):
        self.out.set(self.inA.value)


class PulseGenerator(BordItem):
    def __init__(self, par, topleft, id=1):
        self.id = id
        self.im = pygame.image.load(os.path.join("Items", "Pulsgenerator.png")).convert()
        BordItem.__init__(self, par, topleft)
        self.inA = Slider(self, 1, (12, 24), mini=1, maxi=10)
        self.out = ValueField(self, LOW, (160, 24), id_num=self.id)
        self.ins = [self.inA]
        self.outs = [self.out]
        self.lasttextrect = (2, 2, 1, 1)
        self.refresh()

    def refresh(self):
        pygame.time.set_timer(USEREVENT + self.id, 1000 / int(self.inA.value))
        self.surf.set_clip(self.lasttextrect)
        self.surf.fill((240, 240, 240))
        self.surf.set_clip(None)
        surf, rect = draw_text(str(int(self.inA.value)) + " Hz", font_small, RED)
        rect.topleft = (58, 45)
        self.surf.blit(surf, rect)
        self.lasttextrect = rect


class LED(BordItem):
    def __init__(self, par, topleft):
        self.im = pygame.image.load(os.path.join("Items", "Led.png")).convert()
        self.aan = pygame.image.load(os.path.join("Items", "Ledaan.png")).convert()
        BordItem.__init__(self, par, topleft)
        self.inA = ValueField(self, LOW, (16, 24))
        self.ins = [self.inA]

    def refresh(self):
        self.surf.blit(self.im, (0, 0))
        if self.inA.value:
            self.surf.blit(self.aan, (160, 24))


class Buzzer(BordItem):
    def __init__(self, par, topleft):
        self.im = pygame.image.load(os.path.join("Items", "Zoemer.png")).convert()
        BordItem.__init__(self, par, topleft)
        self.inA = ValueField(self, LOW, (16, 48))
        self.ins = [self.inA]

    def refresh(self):
        if self.inA.value:
            beep.play(loops=-1)
        else:
            beep.stop()


class Explain(BordItem):
    def __init__(self, par, topleft):
        self.im = pygame.image.load(os.path.join("Items", "Uitleg.png")).convert()
        BordItem.__init__(self, par, topleft)


class MemoryCell(BordItem):
    def __init__(self, par, topleft):
        self.im = pygame.image.load(os.path.join("Items", "Geheugencel.png")).convert()
        BordItem.__init__(self, par, topleft)
        self.inA = ValueField(self, LOW, (8, 24))
        self.inB = ValueField(self, LOW, (8, 72))
        self.out = ValueField(self, LOW, (144, 48))
        self.ins = [self.inA, self.inB]
        self.outs = [self.out]

    def refresh(self):
        if self.inA.value:
            self.out.set(HIGH)
        elif self.inB.value:
            self.out.set(LOW)


class AndPort(BordItem):
    def __init__(self, par, topleft):
        self.im = pygame.image.load(os.path.join("Items", "Enpoort.png")).convert()
        BordItem.__init__(self, par, topleft)
        self.inA = ValueField(self, LOW, (8, 24))
        self.inB = ValueField(self, LOW, (8, 72))
        self.out = ValueField(self, LOW, (144, 48))
        self.ins = [self.inA, self.inB]
        self.outs = [self.out]

    def refresh(self):
        self.out.set(self.inA.value and self.inB.value)


class OrPort(BordItem):
    def __init__(self, par, topleft):
        self.im = pygame.image.load(os.path.join("Items", "Ofpoort.png")).convert()
        BordItem.__init__(self, par, topleft)
        self.inA = ValueField(self, LOW, (8, 24))
        self.inB = ValueField(self, LOW, (8, 72))
        self.out = ValueField(self, LOW, (144, 48))
        self.ins = [self.inA, self.inB]
        self.outs = [self.out]

    def refresh(self):
        self.out.set(self.inA.value or self.inB.value)


class Invertor(BordItem):
    def __init__(self, par, topleft):
        self.im = pygame.image.load(os.path.join("Items", "Invertor.png")).convert()
        BordItem.__init__(self, par, topleft)
        self.inA = ValueField(self, LOW, (8, 48))
        self.out = ValueField(self, HIGH, (144, 48))
        self.ins = [self.inA]
        self.outs = [self.out]

    def refresh(self):
        self.out.set(not self.inA.value)


class Transistor(BordItem):
    def __init__(self, par, topleft):
        self.im = pygame.image.load(os.path.join("Items", "Transistor.png")).convert()
        BordItem.__init__(self, par, topleft)
        self.out = AnalogValue(self, 5.0, (145, 25))
        self.inA = AnalogValue(self, 0.0, (9, 25))
        self.ins = [self.inA]
        self.outs = [self.out]
        self.refresh()

    def refresh(self):
        self.out.set(5.0 - self.inA.value)


class Comperator(BordItem):
    def __init__(self, par, topleft):
        self.im = pygame.image.load(os.path.join("Items", "Comperator.png")).convert()
        BordItem.__init__(self, par, topleft)
        self.out = ValueField(self, LOW, (144, 24))
        self.inA = AnalogValue(self, 0.0, (9, 25))
        self.inB = Slider(self, 2.5, (50, 74))
        self.ins = [self.inA, self.inB]
        self.outs = [self.out]
        self.lasttextrect = (2, 2, 1, 1)
        self.refresh()

    def refresh(self):
        self.out.set(self.inA.value >= self.inB.value)
        self.surf.set_clip(self.lasttextrect)
        self.surf.fill((240, 240, 240))
        self.surf.set_clip(None)
        surf, rect = draw_text(str(self.inB.value) + " V", font_small, RED)
        rect.topleft = (90, 100)
        self.surf.blit(surf, rect)
        self.lasttextrect = rect


class Counter(BordItem):
    def __init__(self, par, topleft):
        self.counter = 0
        self.previous_high = False
        self.im = pygame.image.load(os.path.join("Items", "Teller.png")).convert()
        BordItem.__init__(self, par, topleft)
        self.inA = ValueField(self, LOW, (16, 16))
        self.inB = OnOffButtonValue(self, LOW, (16, 48))
        self.inC = ValueField(self, LOW, (16, 80))
        self.inD = ButtonValue(self, LOW, (149, 80))
        self.ins = [self.inA, self.inB, self.inC, self.inD]
        self.outA = ValueField(self, LOW, (304, 16))
        self.outB = ValueField(self, LOW, (272, 16))
        self.outC = ValueField(self, LOW, (240, 16))
        self.outD = ValueField(self, LOW, (208, 16))
        self.outs = [self.outA, self.outB, self.outC, self.outD]
        self.lasttextrect = (2, 2, 1, 1)
        self.refresh()

    def refresh(self):
        if self.inC.value or self.inD.value:
            self.counter = 0
        if (self.inB.connected and self.inB.value) or not self.inB.connected:
            if self.inA.value and not self.previous_high:
                self.count()
                self.previous_high = True
            if not self.inA.value and self.previous_high:
                self.previous_high = False
        # outputs
        bits = bin(16 + self.counter)[-1:2:-1]
        for i in range(4):
            if bits[i] == "1":
                self.outs[i].set(True)
            else:
                self.outs[i].set(False)
        # drawing
        self.surf.set_clip(self.lasttextrect)
        self.surf.fill((240, 240, 240))
        self.surf.set_clip(None)
        surf, rect = draw_text(str(self.counter), font_big, RED)
        rect.center = (295, 71)
        self.surf.blit(surf, rect)
        self.lasttextrect = rect

    def count(self):
        self.counter += 1
        if self.counter > 9: self.counter = 0


class ValueField(object):
    def __init__(self, par, value, topleft, id_num=None):
        self.id = id_num
        self.value = value
        self.aan = pygame.image.load(os.path.join("Items", "WaardeVakjeAan.png"))
        self.uit = pygame.image.load(os.path.join("Items", "WaardevakjeUit.png"))
        tmp_rect = self.uit.get_rect()
        tmp_rect.topleft = topleft
        self.par = par
        self.surf = self.par.surf.subsurface(tmp_rect)
        self.topleft = topleft
        self.refresh()

    def refresh(self):
        if self.value:
            self.surf.blit(self.aan, (0, 0))
        else:
            self.surf.blit(self.uit, (0, 0))

    def set(self, value):
        if value != self.value:
            self.value = value
            self.par.refresh()
            self.refresh()


class OnOffButtonValue(ValueField):
    def __init__(self, par, value, topleft):
        ValueField.__init__(self, par, value, topleft)
        self.connected = False

    def notify_connect(self):
        self.connected = True

    def notify_disconnect(self):
        self.connected = False


class ButtonValue(ValueField):
    def __init__(self, par, value, topleft):
        ValueField.__init__(self, par, value, topleft)
        self.aan = pygame.Surface((17, 17))
        self.uit = pygame.Surface((17, 17))
        self.aan.fill(BLUE)
        self.uit.fill(DARK_BLUE)
        self.refresh()


class AnalogValue(ValueField):
    def __init__(self, par, value, topleft):
        self.value = value
        self.im = pygame.Surface((15, 15))
        self.tmprect = self.im.get_rect()
        self.tmprect.topleft = topleft
        self.par = par
        self.surf = self.par.surf.subsurface(self.tmprect)
        self.refresh()

    def refresh(self):
        color_value = int(((127 * self.value) / 5) + 128)
        self.im.fill((color_value, color_value, 0))
        self.surf.blit(self.im, (0, 0))


class Slider(ValueField):
    def __init__(self, par, value, topleft, width=115, mini=0.0, maxi=5.0):
        self.value = value
        self.width = width
        self.mini = mini
        self.maxi = maxi
        self.par = par
        self.topleft = topleft
        self.im = pygame.image.load(os.path.join("Items", "Sliderachtergrond.png")).convert()
        self.button = pygame.Surface((15, 15))
        self.button.fill(BLUE)
        self.image_rect = self.im.get_rect()
        self.image_rect.width = width
        self.im.set_clip(self.image_rect)
        self.image_rect.topleft = self.topleft
        self.surf = self.par.surf.subsurface(self.image_rect)
        self.cur_pos = None
        self.tmp_button = None
        self.refresh()

    def refresh(self):
        x_value = int((self.width - 15) * self.value) / self.maxi
        self.cur_pos = self.button.get_rect()
        self.cur_pos.left += x_value
        self.tmp_button = self.surf.subsurface(self.cur_pos)
        self.surf.blit(self.im, (0, 0))
        self.tmp_button.blit(self.button, (0, 0))

    def calculate_value(self, delta_x):
        tmp = float(self.cur_pos.left + delta_x)
        val = (tmp * self.maxi) / float(self.width - 15)
        if val < self.mini: val = self.mini
        if val > self.maxi: val = self.maxi
        return val


