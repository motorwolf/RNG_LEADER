# RNG_LEADER by Kristen Payne

![RNG_LEADER intro](https://raw.githubusercontent.com/motorwolf/RNG_LEADER/master/docs/intro.gif)

RNG Leader is a collection exploration browser game with roguelike elements. Can you stay alive long enough to collect all the things?

![RNG_LEADER gameplay](https://raw.githubusercontent.com/motorwolf/RNG_LEADER/master/docs/gameplay.gif)
The world map is generated randomly to output trees or grass and displayed on an HTML5 canvas. The game engine was designed by the author from scratch, using no external libraries in an effort to fully understand the mechanics. The sprites were also drawn by the author. As the player travels through the game world, they have battle encounters that increase their score and points.

![RNG_LEADER intro](https://raw.githubusercontent.com/motorwolf/RNG_LEADER/master/docs/player-detail.png)

The object of the game is to collect items, which are hidden in a randomly generated desert square. When the target square is found, a boss battle is initialized. If the player wins, they obtain the item, and if they bring it back to the castle, they win the game and many score bonuses.

![RNG_LEADER intro](https://raw.githubusercontent.com/motorwolf/RNG_LEADER/master/docs/item-won.png)

In the game, death is permanent and frequent! However you will be in good company in the player graveyard, which shows every player death and their manner of death. You can click to see that player's story, score, and achievements.

![RNG_LEADER intro](https://raw.githubusercontent.com/motorwolf/RNG_LEADER/master/docs/graveyard.png)

Perhaps you will avoid this dire fate and wind up on our leaderboard, which celebrates the greatest collectors and survivors.

![RNG_LEADER intro](https://raw.githubusercontent.com/motorwolf/RNG_LEADER/master/docs/leaderboard.png)

## Built With

RNG_leader was built on a Python/Flask framework where the maps and game elements are randomly generated and stored in a database. RNG_leader uses Javascript ES6 to handle the rendering and the game logic.

