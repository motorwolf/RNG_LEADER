import json, pdb, game, os, hashlib
from flask import Flask, render_template, request, redirect, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

@app.route('/')
def show_index():
    """Serve the index HTML"""
    return render_template('index.html')

@app.route('/login')
def show_login_form():
    """ Serves the Login Form HTML."""
    return render_template('login.html')

@app.route('/login', methods=["POST"])
def player_login():
    """ Match entered credentials against db info."""
    email = request.form.get('email')
    pw = request.form.get('pass')
    player = game.Player.query.filter(game.Player.email == email).first()
    if(player.password != pw):
        print("YOU HAVE BEEN REJECTED!")
        return "Did not work."
    else:
        session['logged_in'] = True
        session['player_id'] = str(player.player_id)
        return redirect(f'player_detail/{player.player_id}')

@app.route('/signup')
def show_signup_form():
    return render_template('signup.html')
@app.route('/signup', methods=["POST"])
def player_sign_up():
    """ Initializes a player. """
    player_email = request.form.get('email')
    player_name = request.form.get('name')
    player_pass = request.form.get('pass')
    # get sanitizes... right??
    if game.Player.query.filter(game.Player.email == player_email).first() == None:
        new_player = game.Player(name=player_name,email=player_email,password=player_pass)
        game.db.session.add(new_player)
        game.db.session.commit()
        # TODO: flash you've been added
        return redirect(f'/player_detail/{new_player.player_id}')
    
    else:
        # TODO: an account already exists with this email.
        return redirect('/login')

@app.route('/player_detail/<player_id>')
def show_player_info(player_id):
    if session['logged_in'] == True and player_id == session['player_id']:
        player = game.Player.query.get(player_id) # this should not fail because if your session id has been assigned an id, you exist.
        collected_items = game.Collected_Item.query.filter(game.Collected_Item.player_id == player_id).all()
        #TODO: dump some player info here!
        breakpoint()
        return render_template('player.html', name=player.name, collected=collected_items) 
    else:
        #TODO: flash you failed criteria to see this page
        return redirect('/login') 



@app.route('/player_login', methods=["POST"])
def player_login_old():
    """ Login the player if they exist, else create player."""
    #TODO: Right now this just creates a player, doesn't check if they exist. Just to test other functions.
    player_login_info = request.get_json()
    player_name = player_login_info['name']
    new_player = game.Player(name=player_name)
    #breakpoint()
    game.db.session.add(new_player)
    game.db.session.commit()
    # in the real world we would have a new game button, but right now I'm just testing functionality.
    new_game = game.Game(regent_id=1,item_id=1,player_id=new_player.player_id,won=False)
    new_game.assign_map_attributes(20,20)
    game.db.session.add(new_game)
    game.db.session.commit()
    return jsonify(new_game.game_attributes())

@app.route('/start_game')
def show_game_page():
    return render_template("game.html")

@app.route('/api/start_game')
def begin_game():
    """ Initialize the Game. """
    if session['logged_in']:
        new_game = game.Game(regent_id=1,item_id=1,player_id=session['player_id'],won=False)
        new_game.assign_map_attributes(20,20)
        game.db.session.add(new_game)
        game.db.session.commit()
        return jsonify(new_game.game_attributes())
    else:
        #TODO: flash you are not logged in. Therefore, how can you play a game? What is happening?
        return redirect('/login')

#    player_map_json = jsonify({**player_info, **map_data}) SAVED so i remember this quick dictionary concat shorthand

if __name__ == '__main__':
    game.connect_to_db(app)
    app.debug=True
    # Debug Toolbar!
    DebugToolbarExtension(app)
    app.run(port=5000, host='0.0.0.0')
