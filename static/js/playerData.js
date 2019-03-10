
const getStory = (id) => {
  fetch(`/get_story/${id}`)
    .then(response => response.json())
    .then(response => {
      outputStoryBlocks(response.stories);
    });
}
const outputStoryBlocks = (lst) => {
  if(lst.length !== 0){
    const storyBlock = document.getElementById('storyBlocks');
    storyBlock.style = "display: block";
    lst.forEach(block => {
      let textHouse = document.createElement('div');
      let p = document.createElement('p');
      let textBlock = document.createTextNode(block);
      p.appendChild(textBlock);
      textHouse.appendChild(p);
      storyBlock.appendChild(textHouse);
    });
  }
}
