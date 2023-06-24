import pandas as pd
from Pieces import *

df = pd.read_csv("CardNobles.csv")

def get_costs(row):
    df['Cost'] = Colorset(dict_of_colors=row[LIST_OF_COLORS].to_dict())

df.apply(get_costs, axis=1)
df_cards = df[df['Type']=='card']
df_nobles = df[df['Type']=='noble']

def make_card(row):
    tier = row['Tier']
    color = row['Color']
    points = row['Points']
    cost = row['Cost']
    return Card(cost, color, points, tier)

def make_noble(row):
    points = row['Points']
    req = row['Cost']
    return Noble(req, points)

df_cards['all_cards'] = df_cards.apply(make_card, axis=1)
df_nobles['all_nobles'] = df_nobles.apply(make_noble, axis=1)

ALL_CARDS = df_cards['all_cards'].to_list()
ALL_NOBLES = df_nobles['all_nobles'].to_list()