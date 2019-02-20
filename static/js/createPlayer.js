
const createPlayerForm = document.querySelector('#createPlayer');
createPlayerForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const newPlayerData = {
    'name': e.target.elements.name.value,
  }
  createPlayer(JSON.stringify(newPlayerData));
});
const createPlayer = (data) => {
  // makes an API call to create a player and fetches the data.
  // someday you shall fetch()
  fetch('/api/create_player',
    { method: "post",
      headers: {'content-type': 'application/json'},
      body: data,
    })
  //.then(response => response.json())
    .then(response => console.log(response));
}
