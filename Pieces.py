from collections import Counter

# stores the information for a single card
class Card:
    #cost is a dict of color code to an int
    #color is a color code (single letter string)
    #points is an int
    #tier is an int (1 to 3)
    def __init__(self, cost, color, points, tier):
        self.cost = cost
        self.color = color
        self.points = points
        self.tier = tier


# class Chip:
#     def __init__(self, color):
#         self.color = color


class Noble:
    #requirement is a dict of color code to an int
    #points is an int
    def __init__(self, requirement, points):
        self.requirement = requirement
        self.points = points

    #returns True if noble requirement is met
    def check_requirements(self, list_of_cards):
        list_of_colors = [card.color for card in list_of_cards]
        count_dictionary = Counter(list_of_colors)
        met_reqs_list = [self.requirement[color] <= count_dictionary[color] for color in self.requirement]
        return all(met_reqs_list)
