import json, pdb, game, os, hashlib
from datetime import datetime
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
def user_login():
    """ Match entered credentials against user information in database."""
    email = request.form.get('email')
    pw = request.form.get('pass')
    # TODO: Need to handle if the user doesn't exist!
    user = game.User.query.filter(game.User.email == email).first()
    if(user.password != pw):
        print("YOU HAVE BEEN REJECTED!")
        return "Did not work."
    else:
        session['logged_in'] = True
        session['user_id'] = str(user.user_id)
        return redirect(f'user/{user.user_id}')

@app.route('/signup')
def show_signup_form():
    """ Shows the user sign up form. """
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
        # TODO: flash you've been added
        # TODO: log in user
        return redirect(f'/user/{new_user.user_id}')
    
    else:
        # TODO: an account already exists with this email.
        return redirect('/login')

@app.route('/user/<user_id>')
def show_user_info(user_id):
    #TODO: MAKE USER ID PAGE.
    session_id = session['user_id']
    if session['logged_in']:
        if user_id == session_id:
            user = game.User.query.filter(game.User.user_id == session_id).first()
            players = user.players
            return render_template("user.html", players = players, user_id = user_id)
        else:
            #TODO : You can't see this page.
            return redirect("/login")
    else:
        #TODO: message: you are not logged in.
        return redirect("/login")

@app.route('/api/create_player', methods=["POST"])
def create_player():
    new_player_request = request.get_json()
    name = new_player_request['name']
    new_player = game.Player(user_id=session['user_id'],name=name)
    game.db.session.add(new_player)
    game.db.session.commit()
    return 'hey'

@app.route('/user/<user_id>/<player_id>')
def show_player_info(user_id, player_id):
    if session['logged_in'] == True and user_id == session['user_id']:
        player = game.Player.query.get(player_id) # this should not fail because if your session id has been assigned an id, you exist.
        collected_items = game.Collected_Item.query.filter(game.Collected_Item.player_id == player_id).all()
        #TODO: dump some player info here!
        return render_template('player.html', name=player.name, collected=collected_items, id=player_id) 
    else:
        #TODO: flash you failed criteria to see this page
        return redirect('/login') 

@app.route('/<player_id>/game')
def show_game_page(player_id):
    return render_template("game.html",player_id=player_id)

@app.route('/api/<player_id>/start_game')
def begin_game(player_id):
    """ Initialize the Game. """
    if session['logged_in']:
        # TODO: randomly generate regent and item from unexhausted pool
        new_game = game.Game(regent_id=1,item_id=1,player_id=player_id,won=False)
        new_game.assign_map_attributes(20,20)
        game.db.session.add(new_game)
        game.db.session.commit()
        return jsonify(new_game.game_attributes())
    else:
        #TODO: flash you are not logged in. Therefore, how can you play a game? What is happening?
        return redirect('/login')


@app.route('/api/<player_id>/item_collected', methods=["POST"])
def item_collected(player_id):
    """ The player has collected the item. We will add it to their collection. """
    game_data = request.get_json()
    print(game_data)
    cur_game = game.Game.query.get(game_data['game_id'])
    if str(cur_game.player.user.user_id) == session['user_id'] and session['logged_in']:
        collected_item = game.Collected_Item(item_id = cur_game.item.item_id, player_id = cur_game.player.player_id, date_collected = datetime.now())
        game.db.session.add(collected_item)
        game.db.session.commit()
    return 'hey'

if __name__ == '__main__':
    game.connect_to_db(app)
    app.debug=True
    # Debug Toolbar!
    DebugToolbarExtension(app)
    app.run(port=5000, host='0.0.0.0')
