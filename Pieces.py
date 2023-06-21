from collections import Counter
LIST_OF_COLORS = ['W', 'B', 'R', 'U', 'G']

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

class Colorset:
    #includes the bank, players' chips, players' tableaus
    
    #creates a Colorset object for exactly one of the three scenarios:
    #  - a generic colorset dictionary
    #  - an initial colorset for the bank or player of all chips the same value
    #  - gets the colorset of a list of cards
    def __init__(self, dict_of_colors=None, initial_value=None, list_of_cards=None): 
        self.dict_of_colors = dict(zip(LIST_OF_COLORS, [0]*len(LIST_OF_COLORS)))

        if dict_of_colors is not None:
            self.dict_of_colors.update(dict_of_colors)
            
        elif initial_value is not None:
            self.dict_of_colors = dict(zip(LIST_OF_COLORS, [initial_value]*len(LIST_OF_COLORS)))
        
        elif list_of_cards is not None:
            color_list = [card.color for card in list_of_cards]
            self.dict_of_colors.update(Counter(color_list))

            
    def combine(self, amount): #takes in two dicts and returns new dict
        pass

    def subtract(self, amount):
        pass
    
    def check_requirement(self, wallet): #checks whether a colorset meets a requirement
        met_requirements = [self.dict_of_colors[color] <= wallet.dict_of_colors[color] for color in LIST_OF_COLORS]
        return all(met_requirements)


class Noble:
    #requirement is a dict of color code to an int
    #points is an int
    def __init__(self, requirement, points):
        self.requirement = requirement
        self.points = points

    #returns True if noble requirement is met
    def check_requirement(self, tableau):
        tableau_colors = Colorset(list_of_cards = tableau)
        return self.requirement.check_requirement(tableau_colors)
    

class IllegalMoveException(Exception):
    pass



