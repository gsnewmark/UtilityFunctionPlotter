# -*- coding: utf-8 -*-

from math import fabs
import matplotlib.pyplot as plt

class UtilityFunctionBuilder(object):
    """
    Builds plot of utility function for a user's utility function 
    for a game where they can win or lose a fixed amount of money with
    a fixed probability (1/2).

    _left_margin - maximum amount of money the user can lose
    _right_margin - maximum amount of money the user can win
    _delta - accuracy of plot building
    """                                             
    def __init__(self):
        super(UtilityFunctionBuilder, self).__init__()
        self._left_margin = None
        self._right_margin = None
        self._delta = None

    def set_initial_values(self, l_margin, r_margin, delta):
        """Sets initial values of fields."""              
        self._left_margin = l_margin
        self._right_margin = r_margin
        self._delta = delta

    def interactively_build_plot(self):
        """Starting function that reads values and builds plot."""
        self._read_initial_values()
        self._build_plot_from_results_list(self._find_plot_points())

    def _read_initial_values(self):
        """Reads initial values of fields from keyboard."""
        l_margin = self._safely_read_float_value(
                u"Input the sum you can lose: ")
        if l_margin > 0:
            l_margin *= -1
        r_margin = self._safely_read_float_value(
                u"Input the sum you can win: ")
        delta = self._safely_read_float_value(
                u"Input accuracy: ")
        self.set_initial_values(l_margin, r_margin, delta)

    def _find_plot_points(self):
        """
        Finds points and utility values for plot of utility function.
        """
        result = self._find_plot_points_on_int(
                self._left_margin, self._right_margin, 0, 1, self._delta)  
        result.append((self._right_margin, 1))
        result.insert(0, (self._left_margin, 0))  
        return result

    def _find_plot_points_on_int(self, lose_a, win_a, lose_u, win_u, delta):
        """
        Finds points and utility values for plot on specified interval.

        lose_a - left margin of interval.
        win_a - right margin of interval.
        lose_u - utility in left margin.
        win_u - utility in right margin.
        delta - accuracy.
        """
        result = []
        
        while True:
            x1, ux1 = self._find_middle_point_and_utility(
                    lose_a, win_a, lose_u, win_u
                    )
            result.append((x1, ux1))

            x2, ux2 = self._find_middle_point_and_utility(
                    lose_a, x1, lose_u, ux1
                    )
            result.append((x2, ux2))

            x3, ux3 = self._find_middle_point_and_utility(
                    x1, win_a, ux1, win_u
                    )
            result.append((x3, ux3))

            x4, ux4 = self._find_middle_point_and_utility(
                    x2, x3, ux2, ux3
                    )
            result.append((x4, ux4))

            if fabs(x1 - x4) <= delta:
                # result with starting points
                data_for_recursion = list(result)
                data_for_recursion.append((win_a, win_u))
                data_for_recursion.insert(0, (lose_a, lose_u))
                data_for_recursion = self._sort_results_list(
                        self._remove_duplicates_from_results_list(
                            data_for_recursion))
                
                for i in range(len(data_for_recursion) - 1):
                    if fabs(data_for_recursion[i][0] - \
                            data_for_recursion[i+1][0]) >= delta:
                        result.extend(self._find_plot_points_on_int(
                            data_for_recursion[i][0], 
                            data_for_recursion[i+1][0],
                            data_for_recursion[i][1],
                            data_for_recursion[i+1][1],
                            delta))

                return self._sort_results_list(
                        self._remove_duplicates_from_results_list(result))
            else:
                print u"Controversial input data - x4 doesn't coincide " \
                        + "with x1. Please correct your choices.\n"

    def _find_middle_point_and_utility(self, l_a, w_a, l_u, w_u):
        """
        Finds point and its utility which is equivalent to utility
        of interval.

        l_a - left margin of interval.
        w_a - right margin of interval.
        l_u - utility in left margin.
        w_u - utility in right margin.
        """
        x = self._safely_read_float_from_interval(l_a, w_a)
        u = 0.5 * (l_u + w_u)
        return x, u


    def _safely_read_float_value(self, text):
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

    def _safely_read_float_from_interval(self, l_margin, r_margin):
        """Reads float value from interval from keyboard."""
        text = u"Input value which utility is equivalent to utility of" \
                " game (" + unicode(l_margin) + u", " + unicode(r_margin) \
                + u") with probabilities (1/2, 1/2): "
        while True:
            value = self._safely_read_float_value(text)
            if value >= l_margin and value <= r_margin:
                return value
            else:
                print u"Incorrect value - it must be between " + \
                        unicode(l_margin) + u" and " + unicode(r_margin) \
                        + "\n"

    def _sort_results_list(self, results_list):
        """Sorts results list (each element is tuple (point, utility))"""
        return sorted(results_list, key=lambda element: element[0])

    def _remove_duplicates_from_results_list(self, results_list):
        """Removes duplicated values from results list."""
        found = set()
        result = []
        for item in results_list:
            if item[0] not in found:
                result.append(item)
                found.add(item[0])
        return result

    def _build_plot_from_results_list(self, results_list):
        """Actually draws the plot using data from results_list."""
        # Preparing plot information
        plot_x_values = [element[0] for element in results_list]
        plot_y_values = [element[1] for element in results_list]
        plt.title(u"Utility function")
        plt.plot(plot_x_values, plot_y_values)
        plt.xlabel(u"Gainings")
        plt.ylabel(u"Utility")
        plt.show()

      
if __name__ == "__main__":
    function_builder = UtilityFunctionBuilder()
    function_builder.interactively_build_plot()
