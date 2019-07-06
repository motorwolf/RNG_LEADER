import json, pdb, game, os, hashlib, random
from datetime import datetime
from flask import Flask, render_template, request, redirect, jsonify, session, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

@app.route('/')
def show_index():
    """Serve the index HTML"""
    if 'logged_in' not in session:
        session['logged_in'] = False
    return render_template('index.html')

############### LOGIN/LOGOUT, SIGN UP #########################

@app.route('/login')
def show_login_form():
    """ Serves the Login Form HTML."""
    return render_template('login.html')

@app.route('/login', methods=["POST"])
def user_login():
    """ Match entered credentials against user information in database."""
    email = request.form.get('email')
    pw = request.form.get('pass')
    # TODO: Need to handle if the user doesn't exist!
    user = game.User.query.filter(game.User.email == email).first()
    if(user.password != pw):
        print("YOU HAVE BEEN REJECTED")
        flash("This password did not match.")
        return "Did not work."
    else:
        session['logged_in'] = True
        session['user_id'] = str(user.user_id)
        return redirect(f'user/{user.user_id}')

@app.route('/logout')
def log_user_out():
    """ Remove user id and sets log in state to false."""
    del session['user_id']
    session['logged_in'] = False
    flash("You have logged out.")
    return redirect("/")

@app.route('/signup')
def show_signup_form():
    """ Shows the user sign up form. """
    if 'user_id' in session:
        if session['user_id'] and session['logged_in']:
            return redirect(f'/user/{session["user_id"]}')
    else: 
        return render_template('signup.html')

@app.route('/signup', methods=["POST"])
def user_sign_up():
    """ Initializes a user. """
    user_email = request.form.get('email')
    user_name = request.form.get('name')
    user_pass = request.form.get('pass')
    # get sanitizes... right??
    if game.User.query.filter(game.User.email == user_email).first() == None:
        new_user = game.User(name=user_name,email=user_email,password=user_pass)
        game.db.session.add(new_user)
        game.db.session.commit()
        # log in user
        session['logged_in'] = True
        session['user_id'] = str(new_user.user_id)
        flash("Welcome! You've signed up!")
        return redirect(f'/user/{new_user.user_id}')
    
    else:
        flash("An account already exists with this email. Log in.")
        return redirect('/login')

##########

@app.route('/user/<user_id>')
def show_user_info(user_id):
    """ Displays a user information page that will show all players that the user has created. """
    # TODO LOW : this could be cleaned up with our logged in function.
    session_id = session['user_id']
    if session['logged_in']:
        if user_id == session_id:
            user = game.User.query.filter(game.User.user_id == session_id).first()
            #players = user.players
            alive_players = []
            dead_players = []
            for player in user.players:
                if player.alive:
                    alive_players.append(player)
                if player.alive == False:
                    dead_players.append(player)
            return render_template("user.html", alive_players = alive_players,dead_players = dead_players, user_id = user_id)
        else:
            flash("You are not logged in and can't see this page.")
            return redirect("/login")
    else:
        flash("You are not logged in.")
        return redirect("/login")

@app.route('/api/create_player', methods=["POST"])
def create_player():
    """ Creates a new player based on JSON sent and adds the new player to the database. Associates based on logged in user_id. """ 
    new_player_request = request.get_json()
    name = new_player_request['name']
    player_type = new_player_request['type']
    mutation_id = random.choice(game.Mutation.query.all()).mutation_id
    player_class = game.Player_Class.query.filter(game.Player_Class.name == player_type).one(); 
    new_player = game.Player(user_id=session['user_id'],name=name,mutation_id=mutation_id,alive=True,score=0,stats=player_class.base_stats,exp=0,level=1,player_class=player_class.class_id)
    game.db.session.add(new_player)
    game.db.session.commit()
    return "" # this does return nothing, but feels weird

@app.route('/user/<user_id>/player/<player_id>')
def show_player_info(user_id, player_id):
    if session['logged_in'] == True and user_id == session['user_id']:
        player = game.Player.query.get(player_id) # this should not fail because if your session id has been assigned an id, you exist.
        collected_items = game.Collected_Item.query.filter(game.Collected_Item.player_id == player_id).all()
        
        named_items = [(item.item.name, item.item.description) for item in collected_items]
        #TODO: dump some more player info here!
        return render_template('player.html', name=player.name, collected=named_items, id=player_id) 
    else:
        flash("You are not logged in.")
        return redirect('/login') 

@app.route('/user/<user_id>/player/<player_id>/game')
def show_game_page(user_id,player_id):
    return render_template("game.html",player_id=player_id)

@app.route('/api/<player_id>/start_game')
def begin_game(player_id):
    """ Initialize the Game. Generate map, and send new game attributes to browser."""
    player = game.Player.query.get(player_id)
    if session['logged_in'] and session['user_id'] == str(player.user.user_id):
        # TODO: randomly generate regent from unexhausted pool?
        all_items = game.Item.query.filter(game.Item.name != "Future Tech").all()
        player_items = [item.item_id for item in player.collected_items]
        new_items = [item.item_id for item in all_items if item.item_id not in player_items]
        if len(new_items) != 0:
            new_item = random.choice(new_items)
        else:
            new_item = game.Item.query.filter(game.Item.name == "Future Tech").first().item_id
        random_regent = random.choice(game.Regent.query.all()).regent_id
        new_game = game.Game(regent_id=random_regent,item_id=new_item,player_id=player_id,won=False, item_collected=False)
        new_game.assign_map_attributes(16,28)
        game.db.session.add(new_game)
        game.db.session.commit()
        game_attr = new_game.game_attributes()
        story_block = game.Story_Block.query.filter(game.Story_Block.block_type == 'start').first().\
                          format_story(game_attr)
        game_attr['start_text'] = story_block
        #####
        new_story_block = game.Player_Story(player_story_id=datetime.now(), player_id=player_id,story_text = story_block, story_type = 'start')
        game.db.session.add(new_story_block)
        game.db.session.commit()
        #<== this should be bundled into a function and handled elsewhere... not on game creation. but rather entered into the db after formatted and then pulled and json-ed.
        return jsonify(game_attr)
    
    else:
        #TODO: flash you are not logged in. Therefore, how can you play a game? What is happening?
        return redirect('/login')


@app.route('/api/<player_id>/item_collected', methods=["POST"])
def item_collected(player_id):
    """ The player has collected the item. We will add it to their collection. """
    game_data = request.get_json()
    cur_game = game.Game.query.get(game_data['game_id'])
    if logged_in_and_auth(cur_game.player.user.user_id):
        collected_item = game.Collected_Item(item_id = cur_game.item.item_id, player_id = cur_game.player.player_id, date_collected = datetime.now())
        game.db.session.add(collected_item)
        modifier = len(game.Collected_Item.query.filter(game.Collected_Item.player_id == cur_game.player.player_id).all())
        if modifier == 0:
            modifier = 1;
        cur_game.player.score += 500 * modifier
        cur_game.item_collected = True
        game.db.session.commit()
    else:
        return "something went wrong."
    return "true"

@app.route('/api/game_won',methods=["POST"])
def update_game_and_win():
    """ The player has brought the item to the beginning square, and has won the game."""
    game_info = request.get_json()
    current_game = game.Game.query.get(game_info['game_id'])
    user_id = current_game.player.user.user_id
    player_id = current_game.player.player_id
    if logged_in_and_auth(user_id):
        current_game.won = True;
        modifier = len(game.Game.query.filter(game.Game.won == True and game.Game.user_id == user_id).all())
        if modifier == 0:
            modifier = 1
        current_game.player.score += 1000 * modifier
        new_story_text = game.Story_Block.query.filter(game.Story_Block.block_type == 'item_col_1').one().format_story(game_info)
        new_player_story = game.Player_Story(player_story_id = datetime.now(), player_id=player_id, story_text = new_story_text, story_type="item_col_1")
        game.db.session.add(new_player_story)
        game.db.session.commit()
    # TODO LOW: Add story block
        flash(f"You returned the item and have have won the game!")
    return jsonify(player_id) 

# @app.route('/congrats')
# def win_game():
#     return render_template('congrats.html')
# SHELVED FOR A FUTURE RELEASE

@app.route('/api/die', methods=["POST"])
def kill_player():
    """ Kill the player :( """
    flash("Tragically, your character has died.")
    game_data = request.get_json()
    if game_data['hero']['alive'] == False:
        cur_game = game.Game.query.get(game_data['game_id'])
        user_id = cur_game.player.user.user_id
        if logged_in_and_auth(user_id):
            cur_game.player.alive = False
            story_block = game.Story_Block.query.filter(game.Story_Block.block_type == 'death').one().\
                          format_story(game_data)
            new_story_block = game.Player_Story(player_story_id=datetime.now(), player_id=cur_game.player.player_id, story_text = story_block, story_type='death')
            grave = game.Grave(player_id = cur_game.player.player_id, killer = game_data['killer'], time_of_death = datetime.now())
            game.db.session.add(grave)
            game.db.session.add(new_story_block)
            game.db.session.commit()
            return jsonify(user_id)
    else:
        return ""

@app.route('/api/get_enemy', methods=["GET"])
def return_enemy():
    level = int(request.args.get('level'))
    enemy = random.choice(game.Enemy.query.filter(game.Enemy.level == level).all());
    return jsonify(enemy.enemy_attributes())

@app.route('/api/update_exp', methods=["POST"])
def update_experience():
    to_update = request.get_json()
    player_to_update = game.Player.query.get(to_update['player_id']);
    if logged_in_and_auth(player_to_update.user.user_id):
        #player_to_update.level = 1 #TEST! DELETE LATER
        #player_to_update.exp = 29 # TEST! DELETE LATER
        player_to_update.exp += to_update['enemy_exp']
        player_to_update.score += to_update['enemy_exp'] * 2
        game.db.session.commit()
        updated_stats = {}
        if player_to_update.do_i_level_up():
            new_stats = player_to_update.level_up_stats()
            updated_stats = {
                    'updated': True,
                    'stats': new_stats,
                    'level': player_to_update.level,
                    }
            game.db.session.commit()
            return jsonify(updated_stats)
        else:
            updated_stats = {'updated': False};
        return jsonify(updated_stats)
    #TODO: handle you not being logged in
    return "You are not logged in"

@app.route('/api/get_stats/<player_id>')
def deliver_stats(player_id):
    """ Gets stats from the db and delivers them to be neatly formatted."""
    player = game.Player.query.get(player_id)
    player_info = {
            'alive': player.alive,
            'name': player.name,
            'mutation': player.mutation.name,
            'score': player.score,
            'stats': player.stats,
            'level': player.level,
            'exp': player.exp,
            }
    return jsonify(player_info)

@app.route('/api/set_stats/<player_id>', methods=["POST"])
def update_stats(player_id):
    player_stats = request.get_json()
    player_to_update = game.Player.query.get(player_id)
    if logged_in_and_auth(player_to_update.user.user_id):
        player_to_update.stats = player_stats
        game.db.session.commit()
    return ""

@app.route('/grave/player/<player_id>')
def show_gravesite(player_id):
    player = game.Player.query.get(player_id)
    if player.alive:
        flash("You are still alive!")
        return redirect('/')
    else:
        story = game.Player_Story.query.filter(game.Player_Story.player_id == player_id, game.Player_Story.story_type == 'death').first()
        grave = game.Grave.query.filter(game.Grave.player_id == player_id).one()
        return render_template('grave.html', story=story, grave=grave, player=player, collected=player.collected_items)

@app.route('/get_story/<player_id>')
def return_player_stories(player_id):
    player = game.Player.query.get(player_id)
    stories = game.Player_Story.query.filter(game.Player_Story.player_id == player_id).order_by(game.Player_Story.player_story_id).all()
    story_text = list(map(lambda story: story.story_text, stories));
    json_stories = {'stories': story_text}
    return jsonify(json_stories)
    ###### 

@app.route('/graveyard')
def return_dead_players():
    graves = game.Grave.query.order_by(game.Grave.time_of_death).all()
    return render_template('graveyard.html', graves=graves)

@app.route('/leaderboard')
def return_high_scores():
    players = game.Player.query.filter(game.Player.score != 0).order_by(game.Player.score.desc()).all()
    players_and_items = list(map(lambda player: (player, len(player.collected_items)), players))
    leaders = {}
    leaders['first'], leaders['second'], leaders['third'] = players_and_items[:3]
    players_and_items = players_and_items[3:]
    return render_template('leaderboard.html', players=players_and_items, leaders=leaders)

def logged_in_and_auth(id_to_check):
    id_to_check = str(id_to_check)
    if session['user_id'] == id_to_check and session['logged_in']:
        return True
    else:
        return False

def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == '__main__':
    connect_to_db(app)
    #app.debug=True
    # Debug Toolbar!
    #DebugToolbarExtension(app)
    app.run(port=5000, host='0.0.0.0')
