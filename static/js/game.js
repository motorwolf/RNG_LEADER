localStorage = window.localStorage;


const gameStartForm = document.querySelector('#start');
const canvas = document.querySelector('#canvas');
//canvas.color
const ctx = canvas.getContext('2d');
const imageBg = document.querySelector('#sprites');
imageBg.onload = function() {
  ctx.drawImage(imageBg, 192,0,64,64,128,320,64,64);
};
//console.log(imageAtlas);
// this draws at 128, 320 the tile from 
//const playerPos = ctx.fillRect(0,0,32,32)

// const canvas = document.getElementById('canvas');
// const ctx = canvas.getContext('2d');
// const image = document.getElementById('source');
// image.onload = function() {

//     // At this point, the image is fully loaded
//     // So do your thing!
  
//   ctx.drawImage(image, 33, 71, 104, 124, 21, 20, 87, 104);
// };


window.addEventListener('keyup', (e) => {
  console.log(e);
});
gameStartForm.addEventListener('submit', (e) => {
  e.preventDefault();
  name = e.target[0].value;
  //gameData.clear();
  //gameData.setItem('name',name);
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
        localStorage.setItem('gameData',JSON.stringify(response));
        console.log(response)
      });
});
    const receiveCoords = () => {
    }
  
    const move = () => {
      fetch('/move',{
        method: 'POST',
        headers: {
          'Accept': 'application/json, text/plain',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({x:1, y:1})
        })
        .then(response => response.json()
        )
        .then(response => console.log(response));
    }

//console.log(gameData);
