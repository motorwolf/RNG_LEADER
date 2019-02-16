""" This file will seed data into our database. """
from game import Regent, Game, Player, Item, Collected_Item, connect_to_db, db
from server import app

def load_regents(file):
    
    # if it exists already, delete it
    Regent.query.delete()

    for row in open(file):
        name, title, species = row.rstrip().split("|")
        regent = Regent(name=name,title=title,species=species)
        db.session.add(regent)
    db.session.commit()
    
    print("Regents=========ADDED")
def load_items(file):
    
    # delete existing items table rows
    Item.query.delete()
    for row in open(file):
        name = row.rstrip().split('|')
        item = Item(name = name)
        db.session.add(item)
    db.session.commit()
    print("Items===========ADDED")
        

if __name__ == '__main__':
    connect_to_db(app)
    db.create_all()
    load_regents('data/regents')
    load_items('data/items')
#
