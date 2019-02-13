localStorage = window.localStorage;


const gameStartForm = document.querySelector('#start');
const canvas = document.querySelector('#canvas');
const ctx = canvas.getContext('2d');
const imageBg = document.querySelector('#sprites');
imageBg.onload = function() {
  ctx.drawImage(imageBg, 192,0,64,64,128,320,64,64);
};


// window.addEventListener('keyup', (e) => {
//   console.log(e);
// });

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

