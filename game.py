#import random
#import math
### BEGIN MODEL FILE IMPORT
import random, math
from flask_sqlalchemy import SQLAlchemy, orm

db = SQLAlchemy()
# creates our db model

class Regent(db.Model):
    """ Regent character information. """
    __tablename__ = "regents"

    regent_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    title = db.Column(db.String(40), nullable=True)
    species = db.Column(db.String(40), nullable=False)

    games = db.relationship("Game",
            backref=db.backref('regent')
            )

    def __repr__(self): 
        return f"<Regent {self.title} {self.name} the {self.species}>"

class Item(db.Model):
    """ Item information. """
    __tablename__ = "items"
    
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

class Game(db.Model):
    """ Game information. """

    __tablename__ = "games"

    game_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    regent_id = db.Column(db.Integer, db.ForeignKey('regents.regent_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), nullable=False)
    won = db.Column(db.Boolean, nullable=False)

    player = db.relationship("Player", backref=db.backref("game"))
    item = db.relationship("Item", backref=db.backref("game"))
    
    # trying to set up a non db class attribute

    # @orm.reconstructor
    # def __init__(self):
    #     self.test = 'test' 
    #     self.game_map = self.create_map()

    def __repr__(self):
        return f"""<Game id={self.game_id} player={self.player.name} regent={self.regent.name} item={self.item.name}>"""

    def create_map(self,length,width):
        """ Outputs terrain map represented as a multi-dimensional list. """
        totalTiles = length * width
        treePercent = random.randrange(1,4) * 0.1
        trees = math.floor(totalTiles * treePercent)
        grass = totalTiles - trees
        elements = [trees,grass]
        terrain_map = []
        terrain_row = []
        while (sum(elements)) > 0:
            if len(terrain_row) < width:
                terrain_choice = random.randrange(0,len(elements))
                elements[terrain_choice] -= 1
                terrain_row.append(terrain_choice + 1)
            else:
                terrain_map.append(terrain_row)
                terrain_row = []
        terrain_map.append(terrain_row) #loop will skip last row unless it is added after if/else conditional
        return terrain_map
    
    def assign_map_attributes(self,length,width):
        """ Creates a map, the start position, and the win position, and assigns to self."""
        self.game_map = self.create_map(length,width)
        self.start_position = [math.floor((width - 1)/2), 1]
        self.win_position =  [5,length - 1]

    def game_attributes(self):
        """ Returns a dictionary of relevant attributes to be turned into JSON. """
        game_attr_dict = {
                "start_pos": self.start_position,
                "win_pos": self.win_position,
                "terrain": self.game_map,
                "regent": f"{self.regent.title} {self.regent.name}",
                "item": self.item.name,
                "player": self.player.name,
                }
        return game_attr_dict

class User(db.Model):
    """ A user's account. The account can have many players, and the players can have many games."""
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    players = db.relationship("Player", backref=db.backref("user"))

class Player(db.Model):
    """ Player information. """
    __tablename__ = "players"
    
    player_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    collected_items = db.relationship("Collected_Item", backref = db.backref("player"))
    
    def __repr__(self):
        return f"""<Player name={self.name} user_id={self.user_id}>"""
    
    # password? story? times won? alive? mutation?
    # password is in PLAIN TEXT! EEEEEK!
    

class Collected_Item(db.Model):
    """ Represents a successfully collected item when a player wins a game. """

    collected_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), nullable=False)
    date_collected = db.Column(db.DateTime, nullable=False)

# class Mutations

def connect_to_db(app):
    """ Connect the database to our Flask app. """
    # config to use postgreSQL

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///game'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app 
    db.init_app(app)

if __name__ == '__main__':

    # this just allows us to access the app and interact with the database.

    from server import app
    connect_to_db(app)
    print("Connected to DB")

### BEGIN OLD GAME FILE

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
   





class OLD_Player():
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

class OLD_Map():

    def __init__(self,length,width):
        
        self.width = width # x coordinate
        self.length = length # y coordinate
        self.start_position = [math.floor(width/2), 1]
        self.win_position =  [5,length]
        self.map_terrain = self.create_map()
    
    def __repr__(self):
        return f"<Map width={self.width} length={self.length} start_pos={self.start_position} win_pos={self.win_position}>"

    def render_map(self):
        """ The map updates to move player every turn. """

regents = [("Iris","F"), ('Julius Caesar',"M"), ("Penelope","ghost","F"), ("Butkus Stallone",'dog',"M"), ("Little Mac",'human',"M"), ("Gaye Advert","F"), ("Interceptor",'dog',"M"), ("Boudica","F"), ("Anne Bonny","F"), ("Consul Incitatus",'horse',"M"), ("Hachi",'dog',"M")]
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
#
#END GAME FILE
