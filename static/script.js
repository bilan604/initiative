function onMouseUp(e) {
}
function onMouseDown(e) {
    let gallery = document.getElementById("gallery");
    if (gallery.mouseInside) {
        gallery.clickedInside = !gallery.clickedInside;
    }
}
function onMouseEnter(e) {
    if ((e.fromElement === null) || (e.toElement === null)) {
        return;
    }
    if ((e.fromElement.id === "body" || e.toElement.id === "intro") && (e.toElement.id === "gallery")) {
        console.log("Entered gallery from bod!");
        let gallery = document.getElementById("gallery");
        gallery.mouseInside = true;
        gallery.prevX = e.clientX;
        gallery.startRatio = e.clientX / window.innerWidth;
        gallery.startTime = Date.now();
    }
}
function onMouseOut(e) {
    if ((e.fromElement === null) || (e.toElement === null)) {
        return;
    }
    if ((e.fromElement.id === "gallery") && (e.toElement.id === "body" || e.toElement.id === "intro")) {
        console.log("Exited gallery!");
        let gallery = document.getElementById("gallery");
        gallery.mouseInside = false;
        gallery.prevX = e.clientX;
        gallery.startTime = Date.now();
    }
}
function onMouseMove(e) {
    let gallery = document.getElementById("gallery");
    if (gallery.mouseInside) {
        if (gallery.clickedInside) {
            console.log("Clicked to freeze");
            return;
        }
        if (Date.now() - gallery.startTime < 10) {
            return;
        }
        let u = e.clientX;
        let dx = u - gallery.prevX;
        let prevRatio = 100 * (gallery.prevX / window.innerWidth);
        let newRatio = 100 * (dx / window.innerWidth) + prevRatio;
        gallery.prevX = u;
        gallery.startTime = Date.now();
        gallery.animate(
            {transform: 'translate(-' + Math.min(100, Math.max(0, newRatio)) +'%, -50%)'}, 
            {duration: 10, fill: 'forwards'}
        );
        moveImages(e);
        
    }    
}
function moveImages(e) {
    let gallery = document.getElementById("gallery");
    let dwindowratio = (e.clientX - gallery.prevX) / window.innerWidth;
    let newratio = 100 * dwindowratio;
    let offsetX = newratio;
    let newPos = newratio + (100 * (gallery.prevX / window.innerWidth));
    gallery.animate(
        {transform: 'translate(-' + Math.min(100, Math.max(0, newPos)) +'%, -50%)'}, 
        {duration: 1200, fill: 'forwards'}
    );

    let np = Math.min(100, Math.max(0, (100-(1.5*newPos.toFixed(0)))));
    let images = gallery.getElementsByClassName("gallery_image");
    for (let i = 0; i < images.length; i++) {
        if (images[i].getBoundingClientRect().left > window.innerWidth) {
            continue;    
        }
        if (images[i].getBoundingClientRect().right < 0) {
            continue;    
        }
        images[i].animate(
            {objectPosition: np + '% 50%'},
            {duration: 1200, fill: 'forwards'}
        );
    }
}

