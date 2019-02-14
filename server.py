import json, pdb, game, os
from flask import Flask, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

position = {
        'x': 1,
        'y': 1,
        'something': 'else'
        }
thing = 'hello'

@app.route('/')
def show_index():
    """Serve the index HTML"""
    return render_template('game.html')

@app.route('/getPos')
def return_position():
    return 'hello'

@app.route('/move',methods=["POST"])
def handle_movement():
    """Receives move coordinates"""
    coords = request.get_json()
    position['x'] = coords['x']
    position['y'] = coords['y']
    #breakpoint()
    return jsonify(position)

@app.route('/start_game', methods=["POST"])
def begin_game():
    """ Initialize the Game. """
    player_name = request.get_json()
    #game.print_test(player_name['name'])
    game_map, player, player_info, map_data = game.start_game(player_name['name'])
    #breakpoint()
    player_map_json = jsonify({**player_info, **map_data})
    return player_map_json 

if __name__ == '__main__':
    app.debug=True
    # Debug Toolbar!
    DebugToolbarExtension(app)
    app.run(port=8000, host='0.0.0.0')
