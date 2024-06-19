"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

# Rachel Yan (sy625)
# 2021/12/07
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GSprite):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    # Attribute _sound: the sound of the ship when explosion
    # Invariant: _sound is a sound object

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getSound(self):
        """
        Return the sound of the ship.
        """
        return self._sound

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, x, y,source='ship-strip.png'):
        """
        Initializes a new ship.

        Parameter x: the x position of the ship
        Precondition: x is an int or float between 0 and GAME_WIDTH

        Parameter y: the y position of the ship
        Precondition: y is an int or float between 0 and GAME_HEIGHT

        Parameter source: the source of the ship
        Precondition: source is a string, representing the ship
        """
        super().__init__(x=x, y=y, width=SHIP_WIDTH, height=SHIP_HEIGHT,\
        source=source,format=(2,4))
        self._sound = Sound(SHIP_SOUND)

    def scollides(self,bolt):
        """
        Returns True if the alien bolt collides with the ship.

        This method returns False if bolt was not fired by the alien.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        tl = (bolt.x - self.width//2, bolt.y+self.height//2)
        tr = (bolt.x + self.width//2, bolt.y+self.height//2)
        bl = (bolt.x - self.width//2, bolt.y-self.height//2)
        br = (bolt.x - self.width//2, bolt.y-self.height//2)
        if self.contains(tl) or self.contains(tr) or self.contains(bl) or\
         self.contains(br):
            if bolt.getVelocity() < 0:
                return True
            else:
                return False
        else:
            return False

    def move(self,key):
        """
        The method moves the ship.

        When the correct key was pressed, the ship will move by SHIP_MOVEMENT,
        and the method will restrict the ship to stay inside the screen.

        Parameter key: The key to check
        Precondition: key is a bool
        """
        if key == True:
            self.x += SHIP_MOVEMENT
            self.x = min(GAME_WIDTH-SHIP_WIDTH//2,self.x)
        else:
            self.x -= SHIP_MOVEMENT
            self.x = max(0+SHIP_WIDTH/2, self.x)

    # COROUTINE METHOD TO ANIMATE THE SHIP
    def animate(self):
        """
        Animates a the explosion of the ship by changing the frames over
        DEATH_SPEED seconds.

        This method is a coroutine that takes a break (so that the game
        can redraw the image) every time it moves it. The coroutine takes
        the dt as periodic input so it knows how many (parts of) seconds
        to animate.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        animating = True
        time = 0
        while animating:
            # Get the current time
            dt = (yield)
            time += dt
            steps = time/DEATH_SPEED
            amount = steps*self.count
            # Update
            self.frame = int(amount)+1
            # If we go to far, clamp and stop animating
            if self.frame == (self.count):
                animating = False


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    # Attribute _sound: the sound of the alien when explosion
    # Invariant: _sound is a sound object

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getSound(self):
        """
        Return the sound of the alien.
        """
        return self._sound

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x, y,source='alien3.png'):
        """
        Initializes an alien.

        Parameter x: the x position of an alien
        Precondition: x is an int or float between 0 and GAME_WIDTH

        Parameter y: the y position of an alien
        Precondition: y is an int or float between 0 and GAME_HEIGHT

        Parameter source: the source of the alien
        Precondition: source is a string, representing the alien file
        """
        super().__init__(x=x, y=y, width=ALIEN_WIDTH, height=ALIEN_HEIGHT,\
        source=source)
        self._sound = Sound(ALIEN_SOUND)

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def acollides(self,bolt):
        """
        Returns True if the player bolt collides with this alien

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        tl = (bolt.x - self.width//2, bolt.y+self.height//2)
        tr = (bolt.x + self.width//2, bolt.y+self.height//2)
        bl = (bolt.x - self.width//2, bolt.y-self.height//2)
        br = (bolt.x - self.width//2, bolt.y-self.height//2)
        if self.contains(tl) or self.contains(tr) or self.contains(bl) or \
        self.contains(br):
            if bolt.getVelocity() > 0:
                return True
            else:
                return False
        else:
            return False


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVelocity(self):
        """
        Returns the velocity in y direction.
        """
        return self._velocity

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x,y,vb):
        """
        Initializes a ship.

        Parameter x: the x position of the bolt
        Precondition: x is an int or float between 0 and GAME_WIDTH

        Parameter y: the y position of the bolt
        Precondition: y is an int or float between 0 and GAME_HEIGHT

        Parameter vb: the velocity of the bolt
        Precondition: vb is an int of positive or negative value
        """
        super().__init__(x=x, y=y, width=BOLT_WIDTH, height=BOLT_HEIGHT, \
        fillcolor='yellow',linecolor='black')
        self._velocity = vb

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def move(self):
        """
        The method moves the bolts by changing the y position with velocity.
        """
        self.y += self._velocity

    def isPlayerBolt(self):
        """
        Returns True is the bolt is fired by the player. False otherwise.
        """
        if self._velocity > 0:
            return True
        else:
            return False

    def out(self):
        """
        Returns True if the bolt is out of the screen. False otherwise.
        """
        bottom = self.y - (BOLT_HEIGHT)//2
        top = self.y + (BOLT_HEIGHT)//2
        if bottom >= GAME_HEIGHT or top <= 0:
            return True
        else:
            return False
