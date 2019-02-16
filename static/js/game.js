localStorage = window.localStorage;


const gameStartForm = document.querySelector('#start');
const canvas = document.querySelector('#canvas');
const ctx = canvas.getContext('2d');
const spriteSheet = document.querySelector('#sprites');
spriteSheet.onload = function() {
  ctx.drawImage(spriteSheet, 0,0,32,32,50,50,32,32);
};


// window.addEventListener('keyup', (e) => {
//   console.log(e);
// });
//

// player form handler.
const playerLoginForm = document.querySelector("#login");
playerLoginForm.addEventListener('submit', (e) => {
  e.preventDefault();
  console.log(e);
  playerName = e.target.elements.name.value;
  console.log(playerName);
  // ignore password right now.
  fetch("/player_login", 
    {
      method: 'POST',
      headers: {
        'Accept': 'application/json, text/plain',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({'name': playerName}),
    })
    .then(response => response.json())
    .then(response => {
      console.log(response);
      // TODO: DO SOMETHING OTHER THAN LOG!
    });
});


let gameData = {}
gameStartForm.addEventListener('submit', (e) => {
  e.preventDefault();
  name = e.target[0].value;
  fetch('/start_game',
    {
      method: 'POST',
      headers: {
          'Accept': 'application/json, text/plain',
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({'name': name}),
    }).then(response => 
      response.json())
      .then(response => {
        gameData = response;
        localStorage.setItem('gameData',JSON.stringify(response));
        console.log(response);
        renderMap(gameData.terrain);
        renderPlayer(gameData.start_pos[0],gameData.start_pos[1]);
      });
});
const sizeCanvas = (unitSize, width, height) => {
  const canvas = document.querySelector('#canvas');
  canvas.setAttribute('width', (unitSize * width));
  canvas.setAttribute('height', (unitSize * height));
}
const renderMap = (coords) => {
  // This method eats our multidimensional array and spits out beautiful sprites.
  const unitSize = 32; // icon size, in pixels
  sizeCanvas(unitSize,coords[0].length,coords.length);
  // HELP: Could these, should these be in a global dictionary? Saves repitition, but then things become less modular and easy to read?

  let sx = 0; // x axis coordinate - source
  let sy = 0; // y axis coordinate - source
  let sWidth = 32; // width of source rect
  let sHeight = 32; // height of source rect
  let dx = 0; // x axis coord - destination
  let dy = 0; // y axis coord - destination
  let dWidth = 32; // width of destination rect
  let dHeight = 32; // height of destination rect
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
  let dx = x * 32; // x axis coord - destination
  let dy = y * 32; // y axis coord - destination
  let dWidth = 32; // width of destination rect
  let dHeight = 32; // height of destination rect
  ctx.drawImage(spriteSheet, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight);
}
    // const move = () => {
    //   fetch('/move',{
    //     method: 'POST',
    //     headers: {
    //       'Accept': 'application/json, text/plain',
    //       'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify({x:1, y:1})
    //     })
    //     .then(response => response.json()
    //     )
    //     .then(response => console.log(response));
    // }

