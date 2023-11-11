const vars = new Map();
vars.set("activeTopBar", "");
vars.set("clientX", 0);
vars.set("prevTime", new Date());
vars.set("clicked", false);
vars.set("discordGPyT.png", "https://github.com/bilan604/discordGPyT");
vars.set("dataScienceAutomation.png", "https://colab.research.google.com/drive/1c_wFdg_MyLFYCHjqLVFvLqUyeQaJ5Sga");
vars.set("mlb.png", "https://github.com/bilan604/MLB-Dominance-Heirarchy/blob/main/RankingTheMLB.pdf");
vars.set("pageRank.png", "https://github.com/bilan604/GooglePagerank/blob/main/Page_Rank.pdf");


function openNewTab(url) {
  window.open(url, '_blank');
}

function hoverItem(element) {
  element.style.backgroundColor = 'rgb(16, 124, 192)';
}
function unhoverItem(element) {
  element.style.backgroundColor = '';
}
function hoverParent(id) {
	let parent = document.getElementById(id);
  parent.style.backgroundColor = 'rgb(16, 124, 192)';
}
function toInt(percent) {
	return Number(percent.slice(0, percent.length-1));
}

function onClick(e) {
  if (vars.get("clicked") === true) {
    vars.set("clicked", false);
  } else {
    vars.set("clicked", true);
  }
  vars.get("clientX", e.clientX);
}

function handleShiftImages(element) {
  let gallery = document.getElementById("gallery");
  
  let galleryItems = document.getElementsByClassName("galleryItem");
  let images = gallery.getElementsByTagName("img");
  
  let galleryContainer = document.getElementById("galleryContainer");
  let galleryContainerX = galleryContainer.getBoundingClientRect().left;
  let galleryContainerXR = galleryContainer.getBoundingClientRect().right;
  let galleryContainerWidth = galleryContainerXR - galleryContainerX;
  
  for (let i = 0; i<images.length; i++) {
    let parent = galleryItems[i];
    let image = images[i];

    let imageX = parent.getBoundingClientRect().left;
    if (parent.getBoundingClientRect().left >= galleryContainer.getBoundingClientRect().right) {
      continue;
    }
    if (parent.getBoundingClientRect().right <= galleryContainer.getBoundingClientRect().left) {
      continue;
    }
    // - (0.5 * galleryContainerWidth) because first image starts halfway
    let transformRatio = 1 - ((imageX - (galleryContainerX - (galleryContainerWidth))) / galleryContainerWidth);
    transformRatio = Math.max(0, transformRatio);
    transformRatio = Math.min(1, transformRatio);
    
    let galleryItemWidth = parent.getBoundingClientRect().right - parent.getBoundingClientRect().left;
    let maxTransform = ((image.width / galleryItemWidth) - 1) * 100;
    
    // console.log("maxTransform: width and ratio:", image.width, (parent.getBoundingClientRect().right - parent.getBoundingClientRect().left));
    // console.log("maxTransform:", maxTransform);
    image.animate(
            {transform: "translate(-" + String(0.5 * transformRatio * maxTransform) + "%, 0%)"}, 
            {duration: 5, fill: 'forwards'}
        );
    
    }
}

function handleAdditionalGalleryMovement(x, numStr) {
  let galleryLeft = document.getElementById('galleryContainer'+numStr).getBoundingClientRect().left;
  let galleryWidth = 0.7 * window.innerWidth;
  //let galleryRight = galleryLeft + gallery.width;
  
  
  // since the inverse ratio (1 - ...)
  // is inverted by the negative transform translate
  // simply use ratio
  let invRatio = ((x - galleryLeft) / galleryWidth);
  invRatio = Math.max(0, invRatio);
  invRatio = Math.min(1, invRatio);
  //console.log("invRatio", invRatio);
  
  let gallery = document.getElementById("gallery"+numStr);
  // gallery has transform range [-60, 0] on x axis* (60-ish)
  let translateX = 120 * invRatio;
  gallery.animate(
        {transform: "translate(-" + String(translateX) + "%, 0%)"}, 
        {duration: 10, fill: 'forwards'}
    )
  
  vars.set("clientX", x);
  handleShiftImages(e);
}
// redeclare because its not moving back right
function handleGalleryMovement(e) {
  // x must be set here to prevent e.clientX from updating
  const x = e.clientX;
  
  let galleryLeft = document.getElementById('galleryContainer').getBoundingClientRect().left;
  let galleryWidth = 0.7 * window.innerWidth;
  //let galleryRight = galleryLeft + gallery.width;
  
  
  // since the inverse ratio (1 - ...)
  // is inverted by the negative transform translate
  // simply use ratio
  let invRatio = ((x - galleryLeft) / galleryWidth);
  invRatio = Math.max(0, invRatio);
  invRatio = Math.min(1, invRatio);
  //console.log("invRatio", invRatio);
  
  let gallery = document.getElementById("gallery");
  // gallery has transform range [-60, 0] on x axis* (60-ish)
  // 50 is showing and 100 for a body length?
  let translateX = 70  * invRatio;
  gallery.animate(
        {transform: "translate(-" + String(translateX) + "%, 0%)"}, 
        {duration: 10, fill: 'forwards'}
    )
  
  vars.set("clientX", x);
  handleShiftImages(e);
  
}



  

function onMouseMove(e) {
  let now = new Date();
  console.log(now - vars.get("prevTime"));
  if (now - vars.get("prevTime") < 10) {
    return;
  }

  vars.set("prevTime", now);
  console.log("e.clientY > document.getElementById(", e.clientY , document.getElementsByClassName("firstPage")[0].getBoundingClientRect().bottom)
  if (e.clientY < document.getElementsByClassName("firstPage")[0].getBoundingClientRect().bottom) {
    handleGalleryMovement(e);
  } else {
    handleAdditionalGalleryMovement(e.clientX, "2");
  }
}





function init() {
    let gallery = document.getElementById("gallery");
    if (gallery.style.left === "") {
      gallery.style.left = "0%";
    }
    if (gallery.style.width === "") {
      gallery.style.width = "250%";
    }
    if (gallery.style.transform === "") {
      gallery.style.transform = "translate(0%, 0%)";
    }
}
init();

