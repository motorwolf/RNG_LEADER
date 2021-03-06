localStorage = window.localStorage;

let gameData = {
};

const hasRelevantSave = () =>{
  if(localStorage.savedGame == 'true'){
    // TODO : Fix this later. Find out why localStorage doesn't save this as a real bool. For now it works....
    const id = document.getElementById('player_id').textContent;
    game_info = JSON.parse(localStorage.gameData);
    if(game_info.player_id == parseInt(id)){
      gameData = game_info;
      return true;
    }
  }
  return false;
}

const canvas = document.querySelector('#canvas');
const ctx = canvas.getContext('2d');
//spriteSheet.onload = function() {
//  ctx.drawImage(spriteSheet, 0,0,32,32,50,50,32,32);
//};

const storeGame = (gameData) => {
  localStorage.setItem('savedGame', true);
  localStorage.setItem('gameData', JSON.stringify(gameData));
}

const importantMessage = (msg) => {
  const overlay = document.getElementById('overlay');
  const dialog = document.getElementById('dialog');
  overlay.style = 'display: block';
  dialog.textContent = msg;
  const button = document.createElement('button');
  const buttonText = document.createTextNode('OK');
  button.appendChild(buttonText);
  overlay.appendChild(button);
  const hideWindow = (target) => {
    target.style = 'display: none';
  }
  button.addEventListener('click', () => {
    overlay.style = 'display: none';
    button.remove();
  });
}

const gameInitButton = document.querySelector("#game");
gameInitButton.addEventListener('click', (e) => {
  if(!hasRelevantSave()){
    const id = document.getElementById('player_id').textContent;
    fetch(`/api/${id}/start_game`)
      .then(response => response.json())
      .then(response => {
        gameData = response;
        gameData.hero = new Hero(gameData);
        storeGame(gameData);
        startNewGame();
      });
  }
  else {
    // TODO: handle this -- although the button should not be there if there is a game in progress.
    console.log("A game is already in progress.");
    startGame();
  }
  gameInitButton.style = 'display:none';
});

const logToBox = (html,vip=false) => {
  const textBox = document.getElementById('textBox');
  if(!vip){
    textBox.innerHTML = textBox.innerHTML.concat(`<p>${html}<p>`);
  }
  if(vip){
    textBox.innerHTML = textBox.innerHTML.concat(`<p style="color:cyan">${html}</p>`);
  }
  textBox.scrollTop = textBox.scrollHeight;
}

const updateWindowPosition = (coords,condition) => {
  const gameWindow = document.getElementById('gameContainer');
  const blockSize = 64;
  
  if(condition == "battle"){
    const scrollX = "0";
    const scrollY = "96";
    
    gameWindow.scrollLeft = scrollX;
    gameWindow.scrollTop = scrollY;
  }
  if(condition == "center"){
    const scrollX = (coords[0] * blockSize) -(blockSize * 6);
    const scrollY = (coords[1] * blockSize) -(blockSize * 6);
  
    gameWindow.scrollLeft = scrollX;
    gameWindow.scrollTop = scrollY;
  }
  if(condition == "movedX"){
    const scrollX = (coords[0] * blockSize) - (blockSize * 6);
    gameWindow.scrollLeft = scrollX;
  }

  if(condition == "movedY"){
    const scrollY = (coords[1] * blockSize) - (blockSize * 6);
    gameWindow.scrollTop = scrollY;
  }
}

const outputPlayerStatus = (gameData) => {
  // I am thinking this will be a utility function to output player status.
  const statusBox = document.getElementById("statusBox");
  const name = statusBox.getElementById("name");
}

const isBattleTime = (percent) => {
  const number = Math.floor(Math.random() * 100);
  if(number > percent){
    return false;
  }
  else{
    ///// TESTING ON! OTHERWISE THIS SHOULD BE TRUE
    return true;
  }
}



const movePlayer = (dir,currentPosition) => {
  // Interprets player direction, renders map, renders the starting position sprite, updates the player position and renders the player sprite.
  gameData['turn_count']++;
  if(gameData['turn_count'] % 5 == 0){
    if(dir == 'left' || dir == 'right'){
      updateWindowPosition(gameData.cur_pos, 'movedX');
    }
    if(dir == 'up' || dir == 'down'){
      updateWindowPosition(gameData.cur_pos, 'movedY');
    }
  }
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
    
  if(currentPosition[0] == gameData.win_pos[0] && currentPosition[1] == gameData.win_pos[1]){
    if(!gameData.item_collected){
      getEnemy('boss');
    }
  }
  
  if(currentPosition[0] == gameData.start_pos[0] && currentPosition[1] == gameData.start_pos[1]){
    if(gameData['turn_count'] !== 0){
      gameData.hero.heal();
    }
    if(gameData.item_collected){
        localStorage.setItem('savedGame', false);
        logToBox('<p>YES! You delivered the thing!</p>');
        fetch(`/api/game_won`,{
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(gameData),
        })
        .then(response => response.json())
        .then(response => {
          console.log(response);
          window.location.href = `../${response}`;
        });
      }
    }
  
  if(isBattleTime(10)){
    const diceRoll = Math.floor(Math.random() * 10);
    let offset = 0;
    if(diceRoll === 1){
      offset += 1;
    }
    if(diceRoll === 2){
      offset -= 1;
    }
    let enemyLevel = gameData.hero.level + offset;
    if(enemyLevel < 1){
      enemyLevel = 1;
    }
    getEnemy(1);
  }
}

const getEnemy = (level) => {
  if(level !== 'boss'){
    fetch(`/api/get_enemy?level=${level}`)  //${enemyLevel}`) TODO after making enemies for other levels...
      .then(response => response.json())
      .then(response => {
        startBattle(response,gameData.hero);
      });
  }
  else{
    fetch(`/api/get_enemy?level=99`)  
      .then(response => response.json())
      .then(response => {
        const curLevel = gameData.hero.level; 
        if(curLevel > 1){
          response.exp * curLevel;
          for(let stat in response.stats){
            switch(stat){
              case("hp"):
                response.stats['hp'] += response.stats['hp'] * 0.2;
                break;
              case("hp_max"):
                response.stats['hp_max'] += response.stats['hp_max'] * 0.2;
                break;
              default:
                response.stats[stat] += (curLevel * 2);
            }
          }
        }
        startBattle(response,gameData.hero,bossFlag = true);
      });
  }
}

const collectItem = () => {
    if(!gameData['boss_alive']){
      logToBox(`HOORAY! YOU HAVE COLLECTED ${gameData.item}!`,true);
      const id = document.getElementById('player_id').textContent;
      fetch(`/api/${id}/item_collected`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(gameData),
      })
        .then(response => {
          if(response.ok){
            gameData.item_collected = true;
            storeGame(gameData);
          }
        });
    }
}

const startNewGame = () => {
  const veil = document.getElementById('veil');
  veil.classList.remove('hideme');
  gameData['active_game'] = true;
  gameData['item_collected'] = false;
  gameData['turn_count'] = 0;
  gameData['battle'] = false;
  gameData['boss_alive'] = true;
  gameData['player_id'] = parseInt(document.getElementById('player_id').textContent);
  getStats(gameData['player_id']);
  logToBox(gameData.start_text);
  addKeyMap();
  renderMap(gameData.terrain);
  renderStartPos(gameData.start_pos);
  renderPlayer(gameData.start_pos[0],gameData.start_pos[1]);
  gameData['cur_pos'] = [...gameData.start_pos];
  updateWindowPosition(gameData.cur_pos,'center');
  storeGame(gameData);
}

const startGame = () => {

  updateWindowPosition(gameData.cur_pos,'center');
  const veil = document.getElementById('veil');
  veil.classList.remove('hideme');
  getStats(gameData['player_id']);
  gameData.hero = new Hero(gameData);
  logToBox("You return to your game...");
  addKeyMap();
  renderMap(gameData.terrain);
  renderStartPos(gameData.start_pos);
  renderPlayer(...gameData['cur_pos']);
  storeGame(gameData);
}

const addKeyMap = () => {

  window.addEventListener('keydown', (e) => {
    if(!gameData.battle){
      switch(e.key){
        case("ArrowDown"):{
          e.preventDefault(); // NOTE : This has to be AFTER the keypress! or all keeb shortcuts are USELESS!
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
  const spriteSheet = document.querySelector('#terrain');
  const unitSize = 64; // icon size, in pixels
  sizeCanvas(unitSize,coords[0].length,coords.length);

  let sx = 0; // x axis coordinate - source
  let sy = 0; // y axis coordinate - source
  let sWidth = 64; // width of source rect
  let sHeight = 64; // height of source rect
  let dx = 0; // x axis coord - destination
  let dy = 0; // y axis coord - destination
  let dWidth = unitSize; // width of destination rect
  let dHeight = unitSize; // height of destination rect
  const terrainMap = {
    1: 'grass',
    2: 'trees',
    9: 'desert',
  };
  const terrainCoords = {
    // x,y
    'trees': [192,0],
    'grass': [0,0],
    'desert': [64,0],
  }
  for(let r = 0; r < coords.length; r++){
    for(let c = 0; c < coords[r].length; c++){
      const blockType = terrainMap[coords[r][c]];
      const blockCoords = terrainCoords[blockType];
      sx = blockCoords[0];
      sy = blockCoords[1];
      dx = dWidth * c;
      dy = dHeight * r;
      ctx.drawImage(spriteSheet, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight);
    }
  }

  return coords;
}

const renderStartPos = (coord) => {
  
  const spriteSheet = document.querySelector('#terrain');
  const x = coord[0]; 
  const y = coord[1];
  const unitSize = 64; // unit size should be more global........ ugh
  let sx = 128; // x axis coordinate - source
  let sy = 0; // y axis coordinate - source
  let sWidth = 64; // width of source rect
  let sHeight = 64; // height of source rect
  let dx = x * unitSize; // x axis coord - destination
  let dy = y * unitSize; // y axis coord - destination
  let dWidth = unitSize; // width of destination rect
  let dHeight = unitSize; // height of destination rect
  ctx.drawImage(spriteSheet, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight);
}
const renderPlayer = (x,y) => {
  // This function updates the player position, renders the player sprite, and checks whether or not the player position is on the winning square.
  

  const spriteSheet = document.querySelector('#players');
  const unitSize = 64;
  let sx = gameData.player_sprite; // x axis coordinate - source
  let sy = 0; // y axis coordinate - source
  let sWidth = 383; // width of source rect
  let sHeight = 383; // height of source rect
  let dx = x * unitSize; // x axis coord - destination
  let dy = y * unitSize; // y axis coord - destination
  let dWidth = unitSize; // width of destination rect
  let dHeight = unitSize; // height of destination rect
  ctx.drawImage(spriteSheet, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight);
  if(x == gameData.win_pos[0] && y == gameData.win_pos[1]){
    if(!gameData['boss_alive'] && !gameData['item_collected']){
      collectItem();
    }
  }
}

const updateExperience = (player_id,enemy_exp) => {
  let to_update = {
    player_id: player_id.textContent,
    enemy_exp: enemy_exp,
  }
  fetch('/api/update_exp',{
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(to_update),
  })
  .then(response => response.json())
  .then(response => {
    if(response['updated']){
      logToBox(`YOU HAVE ADVANCED TO LEVEL ${response.level}!! YOUR STATS HAVE GONE UP!`,true);
      for(stat in gameData.hero.stats){
        // TODO LOW: it might be nice to spell out STRENGTH, DEXTERITY, etc, rather than using the abbrs.
        const difference = response.stats[stat] - gameData.hero.stats[stat];
        if (difference !== 0 && stat !== "hp"){
          logToBox(`Your ${stat.toUpperCase()} has increased by ${difference}.`);
        }
      }
      gameData.hero.stats = response.stats;
    }
  });
  getStats(gameData['player_id']);
}

const die = (enemy) => {
  localStorage.setItem('savedGame', false);
  gameData['active_game'] = false;
  gameData['killer'] = enemy.name;
  fetch('/api/die', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(gameData),
  })
  .then(response => response.json())
  .then(response => {
    window.location.href = `/user/${response}`;
  })
}

const updateHP = () => {
  const hp = document.getElementById('stat_hp');
  const newHP = gameData.hero.stats.hp;
  if(parseInt(hp.textContent) !== newHP){
    hp.textContent = newHP;
  }
}


const setStats = (player_id) => {
  fetch(`/api/set_stats/${player_id}`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(gameData.hero.stats),
  });
}

class Player {
  constructor(data){
    this.name = data.name;
    this.stats = data.stats;
    this.alive = true;
  }

  attack(target) {
    let hitSuccess;
    let damage;
    let hitChance = Math.floor(Math.random() * (parseInt(this.stats.dex) + 20)); 
    if(hitChance > 2){
      hitSuccess = true;
    } // to hit chance
    if(hitSuccess){
      let baseDamage = Math.floor(this.stats.weap + (this.stats.str/2));
      let damage = (Math.floor(Math.random() * (baseDamage * 2)) + baseDamage) - target.stats.arm;
      if(damage < 0){
        damage = 1;
      }
      logToBox(`${this.name.toUpperCase()} hits for ${damage} damage!`);
      target.stats.hp -= damage;
      if(target.stats.hp < 0){
        logToBox('The death blow has been delivered.')
        target.alive = false;
      }
    }
    else {
      logToBox(`${this.name} MISSES!`);
    }
    updateHP();
    }
}
class Hero extends Player {
  constructor(data){
    // TODO: current position might make sense here.
    super(data);
    this.mutation = data.mutation; // this is the mutation name only right now, for cosmetic reasons. One day it will do stuff?
    this.level = data.player_level;
  }
  heal(){
    this.stats.hp = this.stats.hp_max;
    updateHP();
    logToBox(`You return to ${gameData.regent}'s castle. They summon their remaining powers to heal you.`);
    // TODO LOW: this could be affected by regent attitude, with cha being an offset.
  }
}

class Enemy extends Player {
  constructor(data){
      super(data);
      this.exp = data.exp;
      this.desc = data.desc;
  }
}
const renderEnemyDialog = () => {
  
  const spriteSheet = document.querySelector('#background');
  let sx = 0; // x axis coordinate - source
  let sy = 0; // y axis coordinate - source
  let sWidth = 448; // width of source rect
  let sHeight = 448; // height of source rect
  let dx = 0; // x axis coord - destination
  let dy = 0; // y axis coord - destination
  let dWidth = 960; // width of destination rect
  let dHeight = 900; // height of destination rect
  ctx.drawImage(spriteSheet, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight);
  const enemyDialog = document.getElementById("enemyDialog");
  enemyDialog.style = "display:block";
}

const renderEnemy = (spritePos) => {
  const spriteSheet = document.querySelector('#enemies');
  let sx = spritePos; // x axis coordinate - source (WILL BE DEFINED DIFFERENTLY FOR EACH ENEMY...)
  let sy = 0; // y axis coordinate - source
  let sWidth = 640; // width of source rect
  let sHeight = 640; // height of source rect
  let dx = 180; // x axis coord - destination
  let dy = 200; // y axis coord - destination
  let dHeight = 600;
    //canvas.height * 0.55; // height of destination rect
  
  let dWidth = dHeight;//canvas.width * 0.55; // width of destination rect
  ctx.drawImage(spriteSheet, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight);
}


const startBattle = (enemyData, hero, bossFlag = false) => {
  updateWindowPosition([0,3],'battle');
  let attackSequence = false;
  gameData.battle = true;
  const enemy = new Enemy(enemyData);
  logToBox(`A ${enemy.name.toUpperCase()} draws near.`);
  logToBox(`${hero.name}'s compendium reads: ${enemy.desc}`);
  renderEnemyDialog();
  renderEnemy(enemyData.sprite_pos);
  enemyDialog.style = 'display:block';
  const attack = document.getElementById('attack');
  const run = document.getElementById('run');
  const functionList = [() => startAttackSequence('attack',enemy),() => startAttackSequence('run',enemy)];
  if(!attackSequence) { attack.addEventListener('click', functionList[0]) };
  if(!attackSequence) { run.addEventListener('click', functionList[1]);}
  
  const startAttackSequence = (type, enemy) => {
    let successfullyRan = false;
    attackSequence = true;
    attack.disabled = true;
    run.disabled = true;
    let enemyFaster;
    if(enemy.stats.dex > hero.stats.dex){
      enemyFaster = true;
    } 
    else {
      enemyFaster = false;
    }
    if(type === "attack"){
      if((Math.floor(Math.random() * 10)) === 1){
        enemyFaster = !enemyFaster;
      }
      if(enemyFaster){
        enemy.attack(hero);
        updateHP();
        if(hero.alive){
          hero.attack(enemy);
        }
        else{
          logToBox("You are dead.");
          gameData.battle = false;
          die(enemy);
        }
        // TODO: instead of logging here, I'll probably do something.
      } 
      else { 
        hero.attack(enemy);
        if(enemy.alive){
          enemy.attack(hero);
          updateHP();
        }
        else {
          logToBox("The enemy is dead.");
          gameData.battle = false;
          const id = document.getElementById('player_id');
          updateExperience(id,enemy.exp);
        }
        // TODO: do something other than log
      }
      if(!enemy.alive){
        //debugger;
        logToBox(`YOU HAVE DEFEATED THE ${enemy.name.toUpperCase()}!`,true);
        gameData.battle = false;
        // TODO: Something should happen here.
      }
      if(!hero.alive){
        logToBox(`OH NO! You are dead.`);
        gameData.battle = false;
        if(gameData['active_game']){
          die(enemy);
        }
      }
    }
    if(type === "run"){
      const diceRoll = Math.floor(Math.random() * 10);
      if(enemyFaster){
        if(diceRoll === 1){
          logToBox("You've run away.");
          successfullyRan = true;
          gameData.battle = false;
        }
        else{
          logToBox("You couldn't run away!");
          enemy.attack(hero);
          updateHP();
          if(!hero.alive){
            die(enemy);
          }
        }
      }
      else {
        if(diceRoll < 3){
          logToBox("You've run away!");
          successfullyRan = true;
          gameData.battle = false;
        }
        else{
          logToBox("You couldn't run away!");
          enemy.attack(hero);
          updateHP();
          if(!hero.alive){
            die(enemy);
          }
        }
      }
    }
    if(!hero.alive && gameData['active_game']){
      die(enemy);
    }
    updateHP();
    setStats(gameData['player_id']);
    getStats(gameData['player_id']); 
    attackSequence = false;
    attack.disabled = false;
    run.disabled = false;
    if(!gameData.battle){
      if(bossFlag){
        if(!successfullyRan){
          gameData['boss_alive'] = false;
        }
      }
      enemyDialog.style = "display:none";
      renderMap(gameData.terrain);
      renderStartPos(gameData.start_pos);
      renderPlayer(gameData.cur_pos[0],gameData.cur_pos[1]);
      attack.removeEventListener('click', functionList[0]);
      run.removeEventListener('click', functionList[1]);

      updateWindowPosition(gameData.cur_pos,'center');
      storeGame(gameData);
    }
  }
}

