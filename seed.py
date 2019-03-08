""" This file will seed data into our database. """
from game import Regent, Game, Player, Item, Collected_Item, Mutation, Story_Block, Enemy, Player_Class, connect_to_db, db
from server import app

def load_regents(file):
    
    # if it exists already, delete it
    Regent.query.delete()

    for row in open(file):
        name, title, species, description, attitude = row.rstrip().split("|")
        regent = Regent(name=name,title=title,species=species,description=description,attitude=attitude)
        db.session.add(regent)
    db.session.commit()
    
    print("Regents=========ADDED")
def load_items(file):
    
    # delete existing items table rows
    Item.query.delete()
    for row in open(file):
        name, description = row.rstrip().split("|")
        item = Item(name = name, description = description)
        db.session.add(item)
    db.session.commit()
    print("Items===========ADDED")
        

def load_mutations(file):
    Mutation.query.delete()
    for line in open(file):
        name, description,scale = line.rstrip().split("|")
        mutation = Mutation(name=name, description=description, scale=scale)
        db.session.add(mutation)
    db.session.commit()
    print("Mutations..........ADDED!")

def load_story_blocks(file):
    
    Story_Block.query.delete()
    for row in open(file):
        block_type, text = row.rstrip().split("|")
        story_block = Story_Block(block_type=block_type, text=text)
        db.session.add(story_block)
    db.session.commit()
    print("STORY blocks==========ADDED!")

def load_enemies(file):

    Enemy.query.delete()
    stat_schema = {
            "str": 0,
            "dex": 0,
            "arm": 0,
            "weap": 0,
            "hp": 0,
            "hp_max": 0,
            }
    for row in open(file):
        if "#" not in row:
            name, level, exp, strength, dex, arm, weap, hp, hp_max, sprite_pos, desc = row.rstrip().split("|")
            stat_schema["str"], stat_schema["dex"], stat_schema["arm"], stat_schema["weap"], stat_schema["hp"], stat_schema["hp_max"] = int(strength), int(dex), int(arm), int(weap), int(hp), int(hp_max)
            new_enemy = Enemy(name=name, level=level, exp=exp, stats=stat_schema, sprite_pos=sprite_pos, description=desc)
            db.session.add(new_enemy)
    db.session.commit()
    print("ENEMIES!! =============ADDED!")

def load_classes(file):

    Player_Class.query.delete()
    
    stat_schema = {
            "str": 0,
            "dex": 0,
            "arm": 0,
            "weap": 0,
            "hp": 0,
            "hp_max": 0,
            "int": 0,
            "cha": 0,
            }

    for row in open(file):
        if "#" not in row:
            name, strength, dex, arm, weap, hp, hp_max, intel, cha, sprite_pos, bonus = row.rstrip().split("|")
            stat_schema["str"], stat_schema["dex"], stat_schema["arm"], stat_schema["weap"], stat_schema["hp"], stat_schema["hp_max"], stat_schema['int'], stat_schema['cha'] = int(strength), int(dex), int(arm), int(weap), int(hp), int(hp_max), int(intel), int(cha)
            
            new_class = Player_Class(name=name,base_stats=stat_schema.copy(),sprite_pos=sprite_pos,bonus=bonus)
            db.session.add(new_class)
    db.session.commit()
    print("CLASSES...........ADDED!")


if __name__ == '__main__':
    connect_to_db(app)
    db.create_all()
    load_regents('data/regents')
    load_items('data/items')
    load_mutations('data/mutations')
    load_story_blocks('data/story_blocks')
    load_enemies('data/enemies')
    load_classes('data/class')
