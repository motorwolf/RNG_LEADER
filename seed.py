""" This file will seed data into our database. """
from game import Regent, Game, Player, Item, Collected_Item, Mutation, Story_Block, Enemy, connect_to_db, db
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
            }
    for row in open(file):
        if "#" not in row:
            name, level, exp, strength, dex, arm, weap, desc = row.rstrip().split("|")
            stat_schema["str"] = strength
            stat_schema["dex"] = dex
            stat_schema["arm"], stat_schema["weap"] = arm, weap
            new_enemy = Enemy(name=name, level=level, exp=exp, stats=stat_schema, description=desc)
            db.session.add(new_enemy)
    db.session.commit()
    print("ENEMIES!! =============ADDED!")

if __name__ == '__main__':
    connect_to_db(app)
    db.create_all()
    load_regents('data/regents')
    load_items('data/items')
    load_mutations('data/mutations')
    load_story_blocks('data/story_blocks')
    load_enemies('data/enemies')
