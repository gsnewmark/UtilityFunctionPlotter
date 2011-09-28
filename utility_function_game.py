# -*- coding: utf-8 -*- 

from random import uniform, random

class FortuneGame(object):
    """
    Class that represents game from second exercise from 7th chapter
    of DeGroot's book.

    Used to find x values in building of utility function.

    _delta - step of x change
    _min_random - minimum value of Y
    _max_random - maximum value of Y
    _tests_number - how many test games to play
    _best_x - best x that was found
    _best_x_gain - winnings obtained by choosing _best_x
    """
    def __init__(
            self, 
            delta=1, 
            min_random=-10000, 
            max_random=10000, 
            tests_number=1000
            ):
        super(FortuneGame, self).__init__()
        self._delta = delta
        self._min_random = min_random
        self._max_random = max_random
        self._tests_number = tests_number
        self._best_x = None
        self._best_x_gain = None

    def play(self, left_margin, right_margin):
        """
        Plays the game

        left_margin - minimum gain
        right_margin - maximum gain
        """
        self._best_x = None
        self._best_x_gain = None 
        while True:
            x, gain = self._find_x_and_gain(left_margin, right_margin)
            if self._best_x:
                ans = raw_input("Use best x so far (" + str(self._best_x) + "): ")
                if ans == u"y":
                    return self._best_x

    def _find_x_and_gain(self, left_margin, right_margin):
        """
        Reads x from user and finds related information.
        Returns obtained x and its average gain.
        
        left_margin - minimum gain
        right_margin - maximum gain   
        """
        self._min_random = left_margin
        self._max_random = right_margin  
        x = safely_read_float_value(u"Choose x: ")
        x_gain = self._play_test_x(x, left_margin, right_margin)
        print self._estimate_x(x, x_gain, left_margin, right_margin) 
        return x, x_gain

    def _play_test_x(self, x, l, r):
        """
        Plays _test_number of games with defined game and returns average
        gain.
        
        x - number the user has chosen
        l - minimum gain of X 
        r - maximum gain of X
        """
        sum_of_gains = 0
        for i in range(self._tests_number):
            y = self._get_Y_value()
            if y >= x:
                sum_of_gains += y
            else:
                sum_of_gains += self._get_X_value(l, r)
        return sum_of_gains / self._tests_number

    def _estimate_x(self, x, gain, l, r):
        """
        Estimates whether this x is the best.
        
        x - number the user has choosen
        gain - winnings obtained by choosing x
        l - minimum gain of X 
        r - maximum gain of X  
        """
        x_info = u"Average gain: " + unicode(gain) + u"\n"

        l_sum = 0
        r_sum = 0
        for i in range(1, 101):
            l_sum += self._play_test_x(x - self._delta * i, l, r) 
            r_sum += self._play_test_x(x + self._delta * i, l, r) 
        l_avr = l_sum / 100
        r_avr = r_sum / 100

        if l_avr >= gain:
            return x_info + u"Decrease x to improve the game's result."
        elif r_avr >= gain:
            return x_info + u"Increase x to improve the game's result."  
        elif gain > self._best_x_gain:   
            self._best_x_gain = gain
            self._best_x = x 
            return x_info + u"This x may be the best one."
        else:
            return x_info

    def _get_Y_value(self):
        """Returns (pseudo-) random value of random variable Y."""
        return uniform(self._min_random, self._max_random)

    def _get_X_value(self, l, r):
        """
        Returns winning according to (1/2,1/2) distibution of X.
        
        l - first possible gain
        r - second possible gain
        """
        if random() >= 0.5:
            return l
        else:
            return r


def safely_read_float_value(text):
    """
    Safely reads float value from keyboard and returns it as result.
    Prints text as invitation message.
    """
    while True:
        try:
            variable = float(raw_input(text))
        except ValueError:
            print "You supplied incorrect value, must be number.\n"
        else:
            return variable  


if __name__ == "__main__":
    game = FortuneGame()
    game.play(0, 1000)
