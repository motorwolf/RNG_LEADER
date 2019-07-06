#import random
#import math
### BEGIN MODEL FILE IMPORT
import random, math, re, os 
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
    description = db.Column(db.String(200), nullable=True)
    attitude = db.Column(db.Integer, nullable=True)

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
    description = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Item {self.name}>"

class Game(db.Model):
    """ Game information. """

    __tablename__ = "games"

    game_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    regent_id = db.Column(db.Integer, db.ForeignKey('regents.regent_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), nullable=False)
    won = db.Column(db.Boolean, nullable=False)
    item_collected = db.Column(db.Boolean, nullable=False)

    player = db.relationship("Player", backref=db.backref("games"))
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
        # add desert squares
        des_width = random.randrange(3,math.floor(length/2))
        des_height = random.randrange(1,4)
        desert_rows = terrain_map[-(des_height + 1):]
        surrounding_land = math.floor((width - des_width)/2);
        desert_win = [random.randrange(des_width), random.randrange(des_height)]
        self.win_pos = [(surrounding_land + desert_win[0]), ((length - 1) - des_height) + desert_win[1]]
        for i, row in enumerate(desert_rows):
            winrow = False
            if des_height == i:
                break;
            # if i == win_pos[0]:
            #     winrow = True
            counter = des_width;
            for inx in range(len(row)):
                if inx < surrounding_land or counter == 0:
                    pass
                else:
                    row[inx] = 9
                    counter -= 1

        return terrain_map
    
    def assign_map_attributes(self,length,width):
        """ Creates a map, the start position, and the win position, and assigns to self."""
        self.game_map = self.create_map(length,width)
        self.start_pos = [math.floor((width - 1)/3), 1]
        #self.win_pos =  [5,length - 1]
        self.cur_pos = self.start_pos

    def game_attributes(self):
        """ Returns a dictionary of relevant attributes to be turned into JSON. """
        game_attr_dict = {
                "game_id": self.game_id,
                "start_pos": self.start_pos,
                "win_pos": self.win_pos,
                "cur_pos": self.cur_pos,
                "terrain": self.game_map,
                "regent": f"{self.regent.title} {self.regent.name}",
                "item": self.item.name,
                "name": self.player.name,
                "mutation": self.player.mutation.name,
                "stats": self.player.stats,
                "player_level": self.player.level,
                "player_class": self.player.p_class.name,
                "player_sprite": self.player.p_class.sprite_pos,
                }
        def int_lst_to_str(lst):
            """ Utility to convert a list of numbers to a joined string"""
            return (",").join([str(num) for num in lst])

        terrain_string = ",".join([str(t_unit) for t_row in self.game_map for t_unit in t_row])
        new_map = Map(game_id=self.game_id, map_data=terrain_string, map_size=len(self.game_map[0]), cur_pos=int_lst_to_str(self.cur_pos), win_pos=int_lst_to_str(self.win_pos))
        db.session.add(new_map)
        db.session.commit()
        return game_attr_dict

class Map(db.Model):
    """ A table to store the map data for every Game."""
    __tablename__ = "maps"

    map_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.game_id"), nullable=False)
    map_data = db.Column(db.Text, nullable=False)
    map_size = db.Column(db.Integer, nullable=False)
    cur_pos = db.Column(db.String(10), nullable=False)
    win_pos = db.Column(db.String(10), nullable=False)

    game = db.relationship("Game", backref=db.backref("map"))

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
    player_class = db.Column(db.Integer, db.ForeignKey('player_classes.class_id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    alive = db.Column(db.Boolean, nullable=False)
    mutation_id = db.Column(db.Integer, db.ForeignKey('mutations.mutation_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False) 
    stats = db.Column(db.JSON, nullable=False)
    exp = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False)

    collected_items = db.relationship("Collected_Item", backref = db.backref("player"))
    mutation = db.relationship("Mutation", backref = db.backref("players"))
    p_class = db.relationship("Player_Class", backref = db.backref('players'))
    

    def __repr__(self):
        return f"""<Player name={self.name} user_id={self.user_id}>"""
    
    def do_i_level_up(self):
        """ Checks to see if a player is eligible for the next level. """
        base = 15
        for level in range(1,self.level + 2):
            base *= level
        if self.exp > base:
            self.level += 1
            db.session.commit()
            # sometimes, you might have a giant exp increase where you'd level again, so we run the function again
            return True
        if self.exp < base:
            return False 

    def level_up_stats(self):
        """ Update stats after level increase. """
        # TODO : in the future I might amend these for player classes, but right now we are just incrementing as we go.
        self.score += self.level * 500
        current_stats = self.stats.copy()
        current_stats['hp_max'] += math.floor(current_stats['hp_max'] * 0.25)
        current_stats['str'] += random.randint(1,2)
        current_stats['dex'] += 1
        current_stats['arm'] += 1
        current_stats['weap'] += 1
        current_stats['hp'] = current_stats['hp_max']
        bonus_point = random.randint(1,10)
        if(bonus_point == 10):
                stats = ['str', 'dex', 'arm', 'weap']
                current_stats[random.choice(stats)] += 1
        self.stats = current_stats
        db.session.add(self)
        db.session.commit()
        return self.stats

class Player_Class(db.Model):
    """ Represents the starting stats and sprite of player and score bonuses. """

    __tablename__ = 'player_classes'

    class_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    base_stats = db.Column(db.JSON, nullable=False)
    sprite_pos = db.Column(db.Integer, nullable=False)
    bonus = db.Column(db.Integer, nullable=False)


class Collected_Item(db.Model):
    """ Represents a successfully collected item when a player wins a game. """
    __tablename__ = 'collected_items'
    
    collected_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), nullable=False)
    date_collected = db.Column(db.DateTime, nullable=False)
    
    item = db.relationship("Item",backref=db.backref("collected_items"))
    
    def __repr__(self):
        return f"<Collected Item: {self.item.name}>"

class Mutation(db.Model):
    """ A bunch of mutations. A player is randomly assigned one. """
    __tablename__ = 'mutations'

    mutation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    scale = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"<Mutation: {self.name}>"

class Story_Block(db.Model):
    """ This is the house for our generative text. Right now it is static blocks of text with slots for variables. """
    __tablename__ = 'story_blocks'

    story_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    block_type = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    
    def format_story(self,game_dict):
        """ Game dict will be a dictionary of values that match the variable slots in our story block, which is a long text string. Returns the variables plugged into the text block."""
        
        def is_string_one_word(string):
            if len(string.split(" ")) == 1:
                dictionary_value = game_dict.get(string,string)
                return dictionary_value.upper()
            else:
                return string

        formatted_block = "".join(map(is_string_one_word, self.text.split('$')))
        return formatted_block
        
        ####
        # formatted_block = " ".join(story_block.split('$').map(lambda s:
        #     if len(s.split(" ")) == 1:
        #         game_dict.get(s,s) # if string is not in our dictionary, return the string.
        #     else: 
        #         return s
        #     ))
        # return formatted_block



class Player_Story(db.Model):
    """ This table will store our various player stories. """
    __tablename__ = 'player_stories'

    player_story_id = db.Column(db.DateTime, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), nullable=False)
    story_text = db.Column(db.Text, nullable=False)
    story_type = db.Column(db.String, nullable=False)

class Enemy(db.Model):
    """ This table will contain enemy stats and names. """
    __tablename__ = 'enemies'

    enemy_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    stats = db.Column(db.JSON, nullable=False)
    exp = db.Column(db.Integer, nullable=False)
    sprite_pos = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), nullable=True)
    

    def enemy_attributes(self):
        enemy_dict = {
                'name': self.name,
                # do I need level?
                'stats': self.stats,
                'exp': self.exp,
                'desc': self.description,
                'sprite_pos': self.sprite_pos,
                }
        return enemy_dict

class Grave(db.Model):
    
    __tablename__ = "graves"

    grave_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), nullable=False)
    killer = db.Column(db.String(255), nullable=False)
    time_of_death = db.Column(db.DateTime, nullable=False)

    player = db.relationship('Player', backref=db.backref('grave'))

def connect_to_db(app):
    """ Connect the database to our Flask app. """
    # config to use postgreSQL

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    #'postgresql:///game'
    #track_modifications = app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app 
    db.init_app(app)

if __name__ == '__main__':

    # this just allows us to access the app and interact with the database.

    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY")
    connect_to_db(app)
    print("Connected to DB")
    app.run(port=5000, host='0.0.0.0')

### BEGIN OLD GAME FILE


regents = [("Iris","F"), ('Julius Caesar',"M"), ("Penelope","ghost","F"), ("Butkus Stallone",'dog',"M"), ("Little Mac",'human',"M"), ("Gaye Advert","F"), ("Interceptor",'dog',"M"), ("Boudica","F"), ("Anne Bonny","F"), ("Consul Incitatus",'horse',"M"), ("Hachi",'dog',"M")]
macguffins = ["Felix Klein's personal klein bottle",'Golden Apple of Hesperades',"Leonardo DaVinci's perpetual motion machine",'bezoar',"Franz Joseph Gall's prototype phrenology head", "Josef Haydn's skull", "Charles Boyle's orrery",'Stadium Events cartridge','Compsognathus skeleton','stuffed great auk','Gibson Les Paul Custom 1957 Goldtop',"Elvis Presley's Blue Armadillo rhinestone jumpsuit","a small sled called Rosebud","1966 Velvet Underground and Nico LP with Banana Sticker Fully Intact"]
random_regent = random.choice(regents)
random_macguffin = random.choice(macguffins)
bodytext = f"Unfortunately, {random_regent[0]}'s powers actually stemmed from their most prized possession, {random_macguffin}"
