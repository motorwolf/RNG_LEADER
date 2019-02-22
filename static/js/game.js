localStorage = window.localStorage;

let gameData = {};

const canvas = document.querySelector('#canvas');
const ctx = canvas.getContext('2d');
const spriteSheet = document.querySelector('#sprites');
spriteSheet.onload = function() {
  ctx.drawImage(spriteSheet, 0,0,32,32,50,50,32,32);
};


const gameInitButton = document.querySelector("#game");
gameInitButton.addEventListener('click', (e) => {
  const id = document.getElementById('player_id').textContent
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

const startGame = () => {
  gameStarted = true; // why?
  renderMap(gameData.terrain);
  renderPlayer(gameData.start_pos[0],gameData.start_pos[1]);
  gameData['cur_pos'] = gameData.start_pos;
  window.addEventListener('keydown', (e) => {
    switch(e.key){
      case("ArrowDown"):{
        gameData.cur_pos[1] += 1;
        renderMap(gameData.terrain);
        renderPlayer(gameData.start_pos[0],gameData.start_pos[1]);
        break;
      }
      case("ArrowUp"):{
        gameData.cur_pos[1] -= 1;
        renderMap(gameData.terrain);
        renderPlayer(gameData.start_pos[0],gameData.start_pos[1]);
        break;
      }
      case("ArrowLeft"):{
        gameData.cur_pos[0] -= 1;
        renderMap(gameData.terrain);
        renderPlayer(gameData.start_pos[0],gameData.start_pos[1]);
        break;
      }
      case("ArrowRight"):{
        gameData.cur_pos[0] += 1;
        renderMap(gameData.terrain);
        renderPlayer(gameData.start_pos[0],gameData.start_pos[1]);
        break;
      }
    }
  });
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
const renderPlayer = (x,y) => {
  console.log(x,y);
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
    alert(`HOOORAY! YOU HAVE COLLECTED ${gameData.item}`)
    const id = document.getElementById('player_id').textContent;
    fetch(`/api/${id}/item_collected`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(gameData),
    })
      .then(response => response.json())
      .then(response => console.log(response));
  }
}

