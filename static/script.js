const FRAMERATE = 120;
const TICK_RATE = 10;
const COORD_SIZE= 20;
const MIN_X = 10;
const MAX_X = 30;
const MIN_Y = 1;
const MAX_Y = 10;

let snake_nodes = [];
snake_nodes.push([10, 10]);

let food_node = [30, 20];

let saved_mouseX = 0;
let saved_mouseY = 0;
let prevTime = Date.now();

function norm(dx, dy) {
    function as_incr(val) {
        if (val === 0) {
            return 0;
        }
        if (val >= 1) {
            return 1;
        } else {
            return -1;
        }    
    }

    if (Math.abs(dx) > Math.abs(dy)) {
        return [as_incr(dx), 0];
    }
    return [0, as_incr(dy)];

}

function render_nodes() {
    let food_div = document.getElementById('food');
    food_div.style.left = `${food_node[0]*COORD_SIZE}px`;
    food_div.style.top = `${food_node[1]*COORD_SIZE}px`;

    let divs = document.getElementsByClassName('snake_node');
    if (divs.length < snake_nodes.length) {
        let parent = document.getElementById('snake');
        let child = parent.children[0];
        let childCopy = child.cloneNode(true);
        parent.appendChild(childCopy);

        divs = document.getElementsByClassName('snake_node');
    }

    for (let i = 0; i < snake_nodes.length; i++) {
        let nodeX = snake_nodes[i][0] * COORD_SIZE;
        let nodeY = snake_nodes[i][1] * COORD_SIZE;
        divs[i].style.left = `${nodeX}px`;
        divs[i].style.top = `${nodeY}px`;
    }
}

function update_nodes(nodes, food_node, mouseX, mouseY) {
    let last = nodes.pop();
    let pX = null;
    let pY = null;
    let head = [null, null];

    if (nodes.length === 0) {
        pX = last[0] * COORD_SIZE;
        pY = last[1] * COORD_SIZE;
        head = [last[0], last[1]];
    } else {
        pX = nodes[0][0] * COORD_SIZE;
        pY = nodes[0][1] * COORD_SIZE;
        head = [nodes[0][0], nodes[0][1]];
    }

    let ate_food = false;
    let dx = mouseX - pX;
    let dy = mouseY - pY;
    
    let dxy = norm(dx, dy);
    if ((Math.floor(mouseX / COORD_SIZE) === Math.floor((head[0]*COORD_SIZE) / COORD_SIZE)) && (Math.floor(mouseY / COORD_SIZE) === Math.floor((head[1]*COORD_SIZE) / COORD_SIZE))) {
        dxy = [0, 0];
    }
    head = [head[0] + dxy[0], head[1] + dxy[1]];
    if ((food_node[0] === head[0]) && (food_node[1] === head[1])) {
        ate_food = true;
    }
    nodes = [head].concat(nodes);

    return [nodes, ate_food];
}

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function handle_food(nodes, phantom_tail_node, ate_food) {
    if (ate_food) {
        nodes.push(phantom_tail_node);
        return [nodes, [getRandomInt(MIN_X, MAX_X), getRandomInt(MIN_Y, MAX_Y)]];
    }
    return [nodes, food_node];

}

function frame_advance() {

    let currTime = Date.now();
    if (currTime - prevTime > FRAMERATE) {
        render_nodes();
        let mouseX = saved_mouseX;
        let mouseY = saved_mouseY;

        prevTime = currTime;
        
        let ate_food = false;
        let phantom_tail_node = [snake_nodes[snake_nodes.length-1][0], snake_nodes[snake_nodes.length-1][1]];
        let resp1 = update_nodes(snake_nodes, food_node, mouseX, mouseY);
        snake_nodes = resp1[0];
        ate_food = resp1[1];
        
        let resp2 = handle_food(snake_nodes, phantom_tail_node, ate_food);
        snake_nodes = resp2[0];
        food_node = resp2[1];
        
        render_nodes();
    }
}


function gameLoop() {
    frame_advance();
    setTimeout(gameLoop, TICK_RATE);
}

gameLoop();


document.addEventListener('mousemove', (e) => {
    const mouseX = e.clientX;
    const mouseY = e.clientY;
    saved_mouseX = mouseX;
    saved_mouseY = mouseY;
    
    let mouseX2 = mouseX - cursor.offsetWidth / 2;
    let mouseY2 = mouseY - cursor.offsetHeight / 2;

    cursor.style.left = `${mouseX2}px`;
    cursor.style.top = `${mouseY2}px`;

});

