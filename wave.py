"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# Rachel Yan (sy625)
# 2021/12/07
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.
    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    #Attribute _direction: the direction of left or right of the aliens moving
    #Invariant: _direction is 1 or -1
    #
    #Attribute _blank: the blank time between the alien fires
    #Invariant: _blank is a random int between 1 and BOLT_RATE
    #
    #Attribute _step: The number of steps the aliens moved
    #Invariant: _step is an int >= 0
    #
    #Attribute _animator:A coroutine for performing an animation
    #Invariant: _animator is a generator-based coroutine (or None)
    #
    #Attribute _dead: the condition of the ship dead or not
    #Invariant: _dead is a bool
    #
    #Attribute _lives: The number of lives of the ship
    #Invariant: _lives is an int between 0 and SHIP_LIVES
    #
    #Attribute _detect: the condition of the ship hit by a bolt or not
    #Invariant: _detect is a bool
    #
    #Attribute _win: The condition of the player winning the game or not
    #Invariant: _win is a bool
    #
    #Attribute _count: The display text of the number of lives left of the ship
    #Invariant: _count is a GLabel object
    #
    #Attribute _score: The score of the player
    #Invariant: _score is an int >= 0
    #
    #Attribute _scoretext: The display text of the score
    #Invariant: _scoretext is a GLabel object

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getDead(self):
        """
        Returns the condition of the ship is dead or not.
        """
        return self._dead

    def getLives(self):
        """
        Returns the number of lives of the ship.
        """
        return self._lives

    def getWin(self):
        """
        Returns the condition of the player win or not.
        """
        return self._win

    def setDead(self,yesno):
        """
        Sets the condition of the ship dead or not.

        Parameter yesno: The condition of ship dead or not
        Precondition: yesno is a bool
        """
        self._dead = yesno

    def setShip(self,restart):
        """
        Sets the ship when restart the game.

        Parameter restart: The condition of the game is restarted or not
        Precondition: restart is a bool
        """
        if restart == True:
            self._ship = Ship(GAME_WIDTH//2,SHIP_BOTTOM+SHIP_WIDTH//2)

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes a new wave of invaders.
        """
        self._aliens = self._addalien()
        self._ship = Ship(GAME_WIDTH//2,SHIP_BOTTOM+SHIP_HEIGHT//2)
        self._dline = GPath(linewidth=2,\
        points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],linecolor="grey")
        self._time = 0
        self._direction = 1
        self._bolts = []
        self._blank = random.randint(1, BOLT_RATE)
        self._step = 0
        self._animator = None
        self._dead = False
        self._lives = SHIP_LIVES
        self._detect = False
        self._win = False
        self._count = GLabel(text="Life: "+str(self._lives),font_size\
        =ARCADE_SMALL,font_name=ARCADE_FONT,x=730,y=670,linecolor=WHITE_COLOR)
        self._score = 0
        self._scoretext = GLabel(text="Score: "+str(self._score),font_size\
        =ARCADE_SMALL,font_name=ARCADE_FONT,x=90,y=670,linecolor=WHITE_COLOR)

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,dt,input):
        """
        Updates the ship, aliens and bolts.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter input: the input
        Precondition: input is an instance of GInput
        """
        # Look at the key presses
        # Doing this way cause left and right to cancel each other out
        # update the ship
        if self._ship is not None and (self._animator is None):
            if input.is_key_down('right'):
                self._ship.move(True)
            if input.is_key_down('left'):
                self._ship.move(False)
        # update the aliens
        self._time += dt
        if self._time > ALIEN_SPEED:
            self._movealien()
            self._time = 0
            self._step += 1
        #update the bolts
        up1 = False
        if input.is_key_down('up'):
            up1 = True
        self._shipbolt(up1)
        self._alienbolt()
        self._deletealien()
        self._deleteship()
        self._animation(dt)
        self._checkline()

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws the ship, aliens, defense line, lives and bolts in the view.

        Parameter view: The view window
        Precondition: view is an instance of GView
        """
        for r in self._aliens:
            for a in r:
                if a is not None:
                    a.draw(view)
        if self._ship is not None:
            self._ship.draw(view)
        self._dline.draw(view)
        if self._bolts != []:
            for b in self._bolts:
                b.draw(view)
        self._count.draw(view)
        self._scoretext.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def resumegame(self):
        """
        Set the conditions for the game to continue after pausing.
        """
        self.setDead(False)
        self.setShip(True)
        self._detect = False

    def _addalien(self):
        """
        Initialize the 2D list of aliens.
        """
        rlist = []
        for r in range(ALIEN_ROWS):
            alist = []
            for a in range(ALIENS_IN_ROW):
                ax = (a+1)*(ALIEN_H_SEP+ALIEN_WIDTH)
                ay = GAME_HEIGHT - ALIEN_CEILING - (ALIEN_ROWS-r-1)*\
                (ALIEN_V_SEP+ALIEN_HEIGHT)
                asource = ALIEN_IMAGES[r//2%3]
                alist.append(Alien(ax, ay, asource))
            rlist.append(alist)
        return rlist

    def _movealien(self):
        """
        Move all the aliens in the list of aliens.

        The aliens will move back and forth between the left and right side of
        the screen. When the rightmost aliens move to the right edge, the aliens
        will move down one step, and move from right to left. When the leftmost
        aliens move to the left edge, the aliens will move down one step and
        move from left to right again.
        """
        lefta = self._checkleft()
        righta = self._checkright()
        right1 = GAME_WIDTH - (righta.x + ALIEN_WIDTH//2)
        left1 = lefta.x - ALIEN_WIDTH//2
        rightresult = self._direction == 1 and right1 > ALIEN_H_SEP
        leftresult = self._direction == -1 and left1 > ALIEN_H_SEP
        if rightresult or leftresult:
            for r in self._aliens:
                for a in r:
                    if a is not None:
                        a.x += self._direction * ALIEN_H_WALK
        else:
            for r in self._aliens:
                for a in r:
                    if a is not None:
                        a.y -= ALIEN_V_WALK
            self._direction *= -1

    def _shipbolt(self,up):
        """
        Update the bolts of ship.

        When the key 'up' is pressed and when there are no other bolts of ship,
        add the bolt of the ship into the list, and fire the bolt.

        Parameter up: whether the key 'up' is pressed or not
        Precondition: up is a bool
        """
        b = 0
        add = True
        while b < len(self._bolts):
            if self._bolts[b].out():
                del self._bolts[b]
            else:
                self._bolts[b].move()
                if self._bolts[b].isPlayerBolt():
                    add = False
                b += 1
        if self._animator is None:
            if up == True and add == True:
                if self._ship is not None:
                    sbolts = Bolt(self._ship.x,(SHIP_HEIGHT+SHIP_BOTTOM),\
                    BOLT_SPEED)
                    self._bolts.append(sbolts)

    #ALIEN BOLT UPDATE
    def _alienbolt(self):
        """
        Update the bolts of aliens

        Look for the bottom alien in each row that is not empty. Randomly choose
        the alien as the shooter, and let it fire the bolts. Wait for the random
        blank time and pick another random alien to shoot.
        """
        if self._step == self._blank:
            alist = []
            for c in range(ALIENS_IN_ROW):
                flag = 0
                for i in range(len(self._aliens)):
                    if self._aliens[i][c] is not None:
                        flag += 1
                if flag > 0:
                    if c not in alist:
                        alist.append(c)
            shooter = []
            for a in alist:
                keep = []
                for r in range(len(self._aliens)):
                    if self._aliens[r][a] is not None:
                        keep.append(r)
                shooter.append(min(keep))
            s0 = random.randint(0,len(shooter)-1)
            s1 = alist[s0]
            shooterx = self._aliens[shooter[s0]][s1].x
            shootery = self._aliens[shooter[s0]][s1].y
            abolts = Bolt(shooterx,(shootery-ALIEN_HEIGHT//2),-BOLT_SPEED)
            self._bolts.append(abolts)
            self._step = 0
            self._blank = random.randint(1,BOLT_RATE)

    def _deletealien(self):
        """
        Deal with the aliens when hit by the bolt.

        Delete the alien when hit by the bolt from ship, add scores to
        the player and make the sound of alien explode.
        """
        for i in range(len(self._aliens)):
            r = self._aliens[i]
            for a in range(len(r)):
                if r[a] is not None:
                    for b in self._bolts:
                        if r[a] is not None:
                            if r[a].acollides(b):
                                r[a].getSound().play()
                                if i == 0:
                                    self._score += ALIEN_POINTS*ALIEN_ROWS
                                else:
                                    self._score += ALIEN_POINTS*(ALIEN_ROWS-i)
                                self._scoretext.text="Score: "+str(self._score)
                                r[a] = None
                                self._bolts.remove(b)

    def _deleteship(self):
        """
        Deal with the ship when hit by the bolt.

        Returns True when the ship is hit by bolts from alien, False other wise.
        Make the sound of ship explode when hit by bolts
        """
        if self._ship is not None:
            for b in self._bolts:
                if self._ship.scollides(b):
                    if self._ship is not None:
                        self._bolts.remove(b)
                        self._ship.getSound().play()
                        self._detect = True
        else:
            self._detect = False

    def _animation(self,dt):
        """
        Animates the explosion of the ship.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        if not self._animator is None:
            try:
                self._animator.send(dt)
            except:
                self._animator = None
                self._ship = None
                self._bolts.clear()
                self._dead = True
                self._lives -= 1
                self._count.text ="Life: "+str(self._lives)
        elif self._detect == True:
            self._animator = self._ship.animate()
            next(self._animator)

    def _checkline(self):
        """
        Check whether alien went past defenseline and whether all aliens killed.

        End the game and state the player win if all the aliens are killed. End
        the game and state that the player lost if the aliens went past the
        defense line
        """
        flag = 0
        for r in self._aliens:
            for a in r:
                if a is not None:
                    if (a.y-ALIEN_HEIGHT//2) <= DEFENSE_LINE:
                        self._win = False
                        self._dead = True
                        self._lives = 0
                else:
                    flag += 1
        if flag == ALIEN_ROWS * ALIENS_IN_ROW:
            self._dead = True
            self._win = True

    def _checkright(self):
        """
        Returns the rightmost alien in the alien list.
        """
        max1 = 0
        row = 0
        for r in range(len(self._aliens)):
            n = self._aliens[r]
            if n is not None:
                for a in range(len(n)):
                    if n[a] is not None:
                        if a >= max1:
                            max1 = a
                            row = r
        return self._aliens[row][max1]

    def _checkleft(self):
        """
        Returns the leftmost alien in the alien list.
        """
        mlist = []
        min1 = 0
        row = 0
        for r in range(len(self._aliens)):
            n = self._aliens[r]
            if n is not None:
                for a in range(len(n)):
                    if n[a] is not None:
                        mlist.append(a)
                        min1 = min(mlist)
                        row = r
        return self._aliens[row][min1]
