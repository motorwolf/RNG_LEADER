localStorage = window.localStorage;

let gameData = {
};

const canvas = document.querySelector('#canvas');
const ctx = canvas.getContext('2d');
const spriteSheet = document.querySelector('#sprites');
spriteSheet.onload = function() {
  ctx.drawImage(spriteSheet, 0,0,32,32,50,50,32,32);
};


const gameInitButton = document.querySelector("#game");
gameInitButton.addEventListener('click', (e) => {
  const id = document.getElementById('player_id').textContent;
  console.log(id);
  fetch(`/api/${id}/start_game`)
    .then(response => response.json())
    .then(response => {
      gameData = response;
      localStorage.setItem('gameData',JSON.stringify(response));
      console.log(response);
      startGame();
    });
});

const logToBox = (html) => {
  const textBox = document.getElementById('textBox');
  textBox.innerHTML = textBox.innerHTML.concat(`<p>${html}<p>`);
  textBox.scrollTop = textBox.scrollHeight;
}

const outputPlayerStatus = (gameData) => {
  // I am thinking this will be a utility function to output player status.
  const statusBox = document.getElementById("statusBox");
  const name = statusBox.getElementById("name");
}

const movePlayer = (dir,currentPosition) => {
  // Interprets player direction, renders map, renders the starting position sprite, updates the player position and renders the player sprite.
  const directions = {
    "down": {"axis": 1,"delta": 1},
    "up": {"axis": 1,"delta":-1},
    "left": {"axis":0,"delta":-1},
    "right": {"axis":0,"delta":1},
  }
  const targetDirection = directions[dir];
  const delta = targetDirection.delta;
  currentPosition[targetDirection.axis] +=delta;
  renderMap(gameData.terrain);
  renderStartPos(gameData.start_pos);
  renderPlayer(currentPosition[0], currentPosition[1]);
}

const isBattleTime = (percent) => {
  const number = Math.floor(Math.random() * 100);
  if(number > percent){
    return false;
  }
  else{
    return true;
  }
}

const startGame = () => {
  gameData['item_collected'] = false;
  logToBox(gameData.start_text);
  console.log(statusBox);
  renderMap(gameData.terrain);
  renderStartPos(gameData.start_pos);
  renderPlayer(gameData.start_pos[0],gameData.start_pos[1]);
  gameData['cur_pos'] = [...gameData.start_pos];
  window.addEventListener('keydown', (e) => {
    switch(e.key){
      case("ArrowDown"):{
        e.preventDefault();
        movePlayer("down", gameData.cur_pos);
        break;
      }
      case("ArrowUp"):{
        e.preventDefault();
        movePlayer("up", gameData.cur_pos);
        break;
      }
      case("ArrowLeft"):{
        e.preventDefault();
        movePlayer("left", gameData.cur_pos);
        break;
      }
      case("ArrowRight"):{
        e.preventDefault();
        movePlayer("right", gameData.cur_pos);
        break;
      }
    }
  });
  const textBox = document.getElementById('textBox');
   
}

const sizeCanvas = (unitSize, width, height) => {
  const canvas = document.querySelector('#canvas');
  canvas.setAttribute('width', (unitSize * width));
  canvas.setAttribute('height', (unitSize * height));
}

const renderMap = (coords) => {
  // This method eats our multidimensional array and spits out beautiful sprites.
  //const height = document.documentElement.clientHeight; =>>> this could be one day used to responsively output block size!
  // could this function actually call the other function? That way we could pass it unitSize rather than redeclaring it.
  const unitSize = 32; // icon size, in pixels
  sizeCanvas(unitSize,coords[0].length,coords.length);

  let sx = 0; // x axis coordinate - source
  let sy = 0; // y axis coordinate - source
  let sWidth = 32; // width of source rect
  let sHeight = 32; // height of source rect
  let dx = 0; // x axis coord - destination
  let dy = 0; // y axis coord - destination
  let dWidth = unitSize; // width of destination rect
  let dHeight = unitSize; // height of destination rect
  const terrainMap = {
    1: 'grass',
    2: 'trees',
  };
  const terrainCoords = {
    // x,y
    'trees': [32,0],
    'grass': [0,0],
  }
  for(let r = 0; r < coords.length; r++){
    for(let c = 0; c < coords[r].length; c++){
      const blockType = terrainMap[coords[r][c]];
      const blockCoords = terrainCoords[blockType];
      sx = blockCoords[0];
      sy = blockCoords[1];
      dx = sWidth * c;
      dy = sHeight * r;
      ctx.drawImage(spriteSheet, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight);
    }
  }

  return coords;
}

const renderStartPos = (coord) => {
  // renders the start square sprite on the start square. should possibly be chained to the map rendering function?
  const x = coord[0]; 
  const y = coord[1];
  const unitSize = 32; // unit size should be more global........ ugh
  let sx = 128; // x axis coordinate - source
  let sy = 0; // y axis coordinate - source
  let sWidth = 32; // width of source rect
  let sHeight = 32; // height of source rect
  let dx = x * unitSize; // x axis coord - destination
  let dy = y * unitSize; // y axis coord - destination
  let dWidth = unitSize; // width of destination rect
  let dHeight = unitSize; // height of destination rect
  ctx.drawImage(spriteSheet, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight);
}
const renderPlayer = (x,y) => {
  // This function updates the player position, renders the player sprite, and checks whether or not the player position is on the winning square.
  const unitSize = 32;
  let sx = 96; // x axis coordinate - source
  let sy = 0; // y axis coordinate - source
  let sWidth = 32; // width of source rect
  let sHeight = 32; // height of source rect
  let dx = x * unitSize; // x axis coord - destination
  let dy = y * unitSize; // y axis coord - destination
  let dWidth = unitSize; // width of destination rect
  let dHeight = unitSize; // height of destination rect
  ctx.drawImage(spriteSheet, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight);
  if(x == gameData.win_pos[0] && y == gameData.win_pos[1]){
    if(!gameData.item_collected){
      logToBox(`<p>HOORAY! YOU HAVE COLLECTED ${gameData.item}!</p>`);
      const id = document.getElementById('player_id').textContent;
      fetch(`/api/${id}/item_collected`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(gameData),
      })
        .then(response => {
          if(response.ok){
            gameData.item_collected = true;
          }
        });
    }
  }
  
  if(x == gameData.start_pos[0] && y == gameData.start_pos[1]){
    if(gameData.item_collected){
        // Do something. Namely, you will return the item to your regent.
        logToBox('<p>YES! You delivered the thing!</p>');
        fetch(`/api/game_won`,{
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(gameData),
        })
        .then(response => {
          if(response.ok){
            console.log(response);
          }
        });
      }
    }
  else if(isBattleTime(10)){
    logToBox('A battle was initiated.');
    startBattle();
  };
}

const startBattle = () => {
  // Take player stats and battle. 

}

