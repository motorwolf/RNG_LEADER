import random
import math

def print_test(stringy):
    """ Just a test to make sure import works ok"""
    print(stringy)

def start_game(name):
    """ Create Map, Player """
    game_map = Map(20,20)
    player = Player(name)
    attributes = player.attribute_dict()
    map_data = game_map.map_attributes()
    return [game_map, player, attributes, map_data]
    
class Player():
    """ Creates a player of the game. Requires a name entry. """
    def __init__(self,name):
        self.name = name
        self.mutation = self.generate_mutation()# determines one randomly 
        self.position = {
                "x": None,
                "y": None
                }
        self.regent = random.choice(regents)
        self.item = random.choice(macguffins) #random_item

    def attribute_dict(self):
        """ Returns a dictionary of attributes. """
        attr_dict = {
                    'name': self.name,
                    'mutation': self.mutation,
                    'position': {
                            "x": self.position['x'],
                            "y": self.position['y']
                        },
                    'regent': self.regent,
                    'item': self.item,
                }
        return attr_dict

    def generate_mutation(self):
        """Randomly determines a mutation for player character """
        mutations = ['long arms','sharp vision'] # should this be a list?
        return random.choice(mutations)

    def move(self,direction):
        print(self.position['x'])
        print(self.position['y'])
        
        def update(operator,direction):
            move_this_way = 'y' if direction in "UD" else 'x'
            # move_this_way = ""
            # if direction in "UD":
            #     move_this_way = "y"
            # else:
            #     move_this_way = "x"
            if operator == 'add':
                self.position[move_this_way] += 1
            if operator == 'sub':
                self.position[move_this_way] -= 1

        direction_tree = {
                 "U": ('add',"U"), 
                 "D": ('sub',"D"),
                 "L": ('sub',"L"),
                 "R": ('add','R')
                 }
        update(direction_tree[direction][0],direction_tree[direction][1])
    
class Map():

    def __init__(self,length,width):
        
        self.width = width # x coordinate
        self.length = length # y coordinate
        self.start_position = [math.floor(width/2), 1]
        self.win_position =  [5,length]
        self.map_terrain = self.create_map()
    
    def __repr__(self):
        return f"<Map width={self.width} length={self.length} start_pos={self.start_position} win_pos={self.win_position}>"

    def create_map(self):
        """ Outputs terrain map represented as a multi-dimensional list. """
        totalTiles = self.length * self.width
        treePercent = random.randrange(1,4) * 0.1
        trees = math.floor(totalTiles * treePercent)
        grass = totalTiles - trees
        elements = [trees,grass]
        terrain_map = []
        terrain_row = []
        while (sum(elements)) > 0:
            print('loop ran')
            if len(terrain_row) < self.width:
                terrain_choice = random.randrange(0,len(elements))
                elements[terrain_choice] -= 1
                terrain_row.append(terrain_choice + 1)
            else:
                terrain_map.append(terrain_row)
                terrain_row = []
        terrain_map.append(terrain_row) #loop will skip last row unless it is added after if/else conditional
        return terrain_map

    def map_attributes(self):
        """ Returns a dictionary of relevant attributes to be turned into JSON. """
        map_dict = {
                "start_pos": self.start_position,
                "win_pos": self.win_position,
                "terrain": self.map_terrain
                }
        return map_dict

    def render_map(self):
        """ The map updates to move player every turn. """

regents = [("Iris","F"), ('Julius Caesar',"M"), ("Penelope","ghost","F"), ("Butkis Stallone",'dog',"M"), ("Little Mac",'human',"M"), ("Gaye Advert","F"), ("Interceptor",'dog',"M"), ("Boudica","F"), ("Anne Bonny","F"), ("Consul Incitatus",'horse',"M"), ("Hachi",'dog',"M")]
macguffins = ["Felix Klein's personal klein bottle",'Golden Apple of Hesperades',"Leonardo DaVinci's perpetual motion machine",'bezoar',"Franz Joseph Gall's prototype phrenology head", "Josef Haydn's skull", "Charles Boyle's orrery",'Stadium Events cartridge','Compsognathus skeleton','stuffed great auk','Gibson Les Paul Custom 1957 Goldtop',"Elvis Presley's Blue Armadillo rhinestone jumpsuit","a small sled called Rosebud","1966 Velvet Underground and Nico LP with Banana Sticker Fully Intact"]
random_regent = random.choice(regents)
random_macguffin = random.choice(macguffins)
bodytext = f"Unfortunately, {random_regent[0]}'s powers actually stemmed from their most prized possession, {random_macguffin}"
#print(bodytext)
# game_active = False
# player_name = input("Name your player >>")
# player = Player(player_name)
# while game_active:
#     movement = input(f"{player_name}, how do you move?")
#     validmoves = "lrudLRUD"
#     if movement not in validmoves:
#         print("Please enter a valid movement, Left, Right, Up or Down.")
#     else:
#         player.move(movement.upper())
