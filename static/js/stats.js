
const getStats = (player_id) => {
  fetch(`/api/get_stats/${player_id}`)
    .then(response => response.json())
    .then(response => {
      outputStats(response);
    });
}

const outputStats = (stats) => {
  for(const stat in stats){
    if(stat == 'stats'){
      // we will need to loop through specially
      for(let inner_stat in stats[stat]){
        const id = "stat_" + inner_stat;
        let target = document.getElementById(id);
        target.textContent = stats[stat][inner_stat];
      }
    }
    else {
      let target = document.getElementById(stat);
      target.textContent = stats[stat];
    }
  }
}
