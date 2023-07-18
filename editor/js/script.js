let grid = [];
let eraser = false;
let selected = 1;
let selectedElement = "recent-1";
let tileImages = {};
let menuCheck = false;
let recent = [4, 3, 2, 1, 5, 13, 14, 15, 16, 17, 19, 18];

const tiles = [
    {
        "number": 1,
        "image": "/wall/single.png",
        "type": "terrain",
        "isDoor": false
    },
    {
        "number": 2,
        "image": "/wall/connect.png",
        "type": "terrain",
        "isDoor": false
    },
    {
        "number": 3,
        "image": "/wall/bottom.png",
        "type": "terrain",
        "isDoor": false
    },
    {
        "number": 4,
        "image": "/wall/top.png",
        "type": "terrain",
        "isDoor": false
    },
    {
        "number": 5,
        "image": "/decoration/1.png",
        "type": "terrain",
        "isDoor": false
    },
    {
        "number": 6,
        "image": "/decoration/2.png",
        "type": "terrain",
        "isDoor": false
    },
    {
        "number": 7,
        "image": "/decoration/3.png",
        "type": "terrain",
        "isDoor": false
    },
    {
        "number": 8,
        "image": "/decoration/4.png",
        "type": "terrain",
        "isDoor": false
    },
    {
        "number": 9,
        "image": "/decoration/5.png",
        "type": "terrain",
        "isDoor": false
    },
    {
        "number": 10,
        "image": "/decoration/6.png",
        "type": "terrain",
        "isDoor": false
    },
    {
        "number": 11,
        "image": "/decoration/7.png",
        "type": "terrain",
        "isDoor": false
    },
    {
        "number": 12,
        "image": "/decoration/8.png",
        "type": "terrain",
        "isDoor": false
    },
    {
        "number": 13,
        "image": "/fire/up.png",
        "type": "terrain",
        "isDoor": false
    },
    {
        "number": 14,
        "image": "/fire/down.png",
        "type": "terrain",
        "isDoor": false
    },
    {
        "number": 15,
        "image": "/fire/left.png",
        "type": "terrain",
        "isDoor": false
    },
    {
        "number": 16,
        "image": "/fire/right.png",
        "type": "terrain",
        "isDoor": false
    },
    {
        "number": 17,
        "image": "/object/yellow/door/top.png",
        "type": "gizmos",
        "isDoor": true
    },
    {
        "number": 18,
        "image": "/object/yellow/button.png",
        "type": "gizmos",
        "isDoor": false
    },
    {
        "number": 19,
        "image": "/object/yellow/key.png",
        "type": "gizmos",
        "isDoor": false
    },
    {
        "number": 20,
        "image": "/object/red/door/top.png",
        "type": "gizmos",
        "isDoor": true
    },
    {
        "number": 21,
        "image": "/object/red/button.png",
        "type": "gizmos",
        "isDoor": false
    },
    {
        "number": 22,
        "image": "/object/red/key.png",
        "type": "gizmos",
        "isDoor": false
    },
    {
        "number": 23,
        "image": "/object/blue/door/top.png",
        "type": "gizmos",
        "isDoor": true
    },
    {
        "number": 24,
        "image": "/object/blue/button.png",
        "type": "gizmos",
        "isDoor": false
    },
    {
        "number": 25,
        "image": "/object/blue/key.png",
        "type": "gizmos",
        "isDoor": false
    }
]

function preload() {
    loadTileImages();
}

function loadTileImages() {
    for (let index = 0; index < tiles.length; index++) {
        const { number, image, isDoor } = tiles[index];

        tileImages[number] = loadImage(`./img/tiles${image}`);

        if (isDoor) tileImages[`${number}⬇`] = loadImage(`./img/tiles${image.replace("top", "bottom")}`);
    }
}

function setup() {
    const canvas = createCanvas(768, 768);
    canvas.parent('editor');

    grid = Array.from({ length: 16 }, () => Array(16).fill(0));
}

function draw() {
    background(0, 0, 0);

    noStroke();
    noSmooth();

    const tileSize = width / grid.length;
    for (let i = 0; i < grid.length; i++) {
        for (let j = 0; j < grid[i].length; j++) {
            const tileX = j * tileSize;
            const tileY = i * tileSize;
            const tileValue = grid[i][j];
            if (tileImages[tileValue]) {
                if (isDoor(tileValue)) image(tileImages[`${tileValue}⬇`], tileX, tileY + tileSize, tileSize, tileSize);
                image(tileImages[tileValue], tileX, tileY, tileSize, tileSize);
            }
        }
    }

    const gx = int((mouseX - mouseX % 48) / 48);
    const gy = int((mouseY - mouseY % 48) / 48);

    if (mouseIsPressed && !menuCheck) {
        const row = floor(mouseY / (height / grid.length));
        const col = floor(mouseX / (width / grid[0].length));

        if (isValidCell(row, col)) {
            if (isDoor(selected) && (gy > 0 && grid[gy - 1][gx] !== 0)) return;
            else if ((gy < 15 && grid[gy - 1][gx] === 17) || (gy < 15 && grid[gy - 1][gx] === 20) || (gy < 15 && grid[gy - 1][gx] === 23)) return;

            grid[row][col] = eraser ? 0 : selected;
        }
    }

    if (!menuCheck) {
        fill(eraser ? 255 : 150, eraser ? 255 : 150, eraser ? 255 : 150, 100);
        rect(gx * 48, gy * 48, 48, 48);
    }
}

function isValidCell(row, col) {
    return row >= 0 && row < grid.length && col >= 0 && col < grid[row].length;
}

function isDoor(number) {
    const tile = tiles.find((tile) => tile.number === number);
    return tile && tile.isDoor;
}

function setObject(value, id) {
    selected = !isNaN(value) ? recent[value] : value;

    document.getElementById(selectedElement).classList.remove('selected');

    selectedElement = id;

    if (isNaN(value)) {
        if (!recent.includes(value)) recent.unshift(value);
        else selectedElement = `recent-${recent.indexOf(value) + 1}`;

        if (recent.length > 12) recent.pop();
    }

    refreshMenu();
    setSelected();
}

function setSelected() {
    document.getElementById(selectedElement).classList.add('selected');
}

function refreshMenu() {
    const paths = recent.map((element) => getPath(element));

    setMultipleElements("recent-", 12, (i) => {
        const imagePath = paths[i - 1];
        const element = document.getElementById(`recent-${i}`);

        element.className = "button";

        const tile = tiles.find((tile) => `./img/tiles${tile.image}` === imagePath);
        if (tile) element.classList.add(tile.type);

        return imagePath;
    });
}

function toggleEraser() {
    eraser ? document.getElementById("eraser").classList.remove("selected") : document.getElementById("eraser").classList.add("selected");

    eraser = !eraser;
}

function rotateLeft(array) {
    const rotatedArray = [];
    const numRows = array.length;
    const numCols = array[0].length;

    for (let i = 0; i < numCols; i++) {
        const newRow = [];
        for (let j = numRows - 1; j >= 0; j--) newRow.push(array[j][i]);
        rotatedArray.push(newRow);
    }

    return rotatedArray;
}

function rotateRight(array) {
    const rotatedArray = [];
    const numRows = array.length;
    const numCols = array[0].length;

    for (let i = 0; i < numCols; i++) {
        const newRow = [];
        for (let j = 0; j < numRows; j++) newRow.unshift(array[j][i]);
        rotatedArray.push(newRow);
    }

    return rotatedArray;
}

function flipHorizontal(array) {
    const flippedArray = [];
    const numRows = array.length;
    const numCols = array[0].length;

    for (let i = 0; i < numRows; i++) {
        const newRow = [];
        for (let j = numCols - 1; j >= 0; j--) newRow.push(array[i][j]);
        flippedArray.push(newRow);
    }

    return flippedArray;
}

function importRoom() {
    if (navigator.clipboard && navigator.clipboard.readText) {
        navigator.clipboard
            .readText()
            .then((clipboardData) => processData(flipHorizontal(rotateLeft(clipboardData))))
            .catch((error) => console.log('Failed to read clipboard data:', error));
    } else {
        const clipboardData = window.prompt('Please enter the data:');
        processData(clipboardData);
    }
}

function processData(clipboardData) {
    grid = flipHorizontal(rotateLeft(JSON.parse(clipboardData)));

    console.log('Data imported successfully.');
}

function exportRoom() {
    const output = JSON.stringify(flipHorizontal(rotateRight(grid)));

    console.log(output);
    navigator.clipboard.writeText(output);
}

function setElement(elementId, imagePath) {
    document.getElementById(elementId).querySelector("img").src = imagePath;
}

function setMultipleElements(elementPrefix, count, imagePathFn) {
    for (let i = 1; i <= count; i++) setElement(`${elementPrefix}${i}`, imagePathFn(i));
}

function getPath(value) {
    const tile = tiles.find((tile) => tile.number === value);
    if (tile) return `./img/tiles${tile.image}`;
    return '';
}

function toggleMenu() {
    const menuButton = document.getElementById("menuButton");
    const menu = document.getElementById("menu");

    if (menuCheck) {
        setElement("menuButton", "./img/menu/down.png");
        menuButton.classList.remove("selected");
        menu.style.display = "none";
    } else {
        setElement("menuButton", "./img/menu/up.png");
        menuButton.classList.add("selected");
        menu.style.display = "block";
    }

    menuCheck = !menuCheck;
}

document.addEventListener('keydown', (event) => event.code === 'KeyE' ? toggleEraser() : null);