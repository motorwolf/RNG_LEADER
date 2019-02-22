
console.log('hi');
const createPlayerForm = document.querySelector('#createPlayer');
createPlayerForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const newPlayerData = {
    'name': e.target.elements.name.value,
  }
  createPlayer(JSON.stringify(newPlayerData));
});
const createPlayer = (data) => {
  fetch('/api/create_player',
    { method: "POST",
      headers: {'content-type': 'application/json'},
      body: data,
    })
    .then(response => {
      if(response.ok == true){
        location.reload();
      }
    });
}
