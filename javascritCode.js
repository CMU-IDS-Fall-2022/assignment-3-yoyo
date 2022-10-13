//intital parameters
var play = true

let windowWidth = 500
let windowHeight = 500
roomSizes = roomSizes.sort().reverse()
let initialSquareSize = [350, 350]
var layout = [[0, 1, 0, 1]];
let depth = 1;
let mode;




function convertToPercentages(l) {
    const reducer = (accumulator, curr) => accumulator + curr;
    sum = l.reduce(reducer)
    result = []
    l.forEach(x => {
        perc = x / sum * 100
        result.push(perc)
    })
    return result
}

function getRandomArbitrary(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}

class vertice {
    constructor(x, y, name, color) {
        this.x = x
        this.y = y
        this.color = color
        this.name = name
        this.radious = 7
        this.around = 25
        this.moving = false
    }
}

function create_treemap() {
    let interval = [0, 1, 0, 1]
    let queue = [[0, interval]]
    let solution = []
    let counter = 0 // this is a counter that sets a limit of iterations
    let limit = 1000
    while (queue.length > 0 && counter < limit) {

        elem = queue.pop()
        d = elem[0]
        interval = elem[1]
        if (d >= depth) {
            solution.push(interval)
        }
        else {
            p = Math.random()

            while (0.3 > p || p > 0.7) {
                p = Math.random()
            }
            vertical = Math.random() //will decide if vertical or horizontal

            if (vertical < 0.5) {
                x0 = interval[2]
                x1 = interval[3]
                xp = p * (x1 - x0) + x0
                int1 = [interval[0], interval[1], x0, xp]
                int2 = [interval[0], interval[1], xp, x1]
            }
            else {
                x0 = interval[0]
                x1 = interval[1]
                xp = p * (x1 - x0) + x0
                int1 = [x0, xp, interval[2], interval[3]]
                int2 = [xp, x1, interval[2], interval[3]]
            }
            queue.push([d + 1, int1])
            queue.push([d + 1, int2])
        }

    }
    layout = solution
    return solution
}

function worst(row, w) {

    const reducer = (accumulator, curr) => accumulator + curr;
    sum = row.reduce(reducer)
    rMax = Math.max(...row)
    rMin = Math.min(...row)
    m1 = ((w ** 2) * rMax) / (sum ** 2)
    m2 = (sum ** 2) / ((w ** 2) * rMin)
    result = Math.max(m1, m2)
    return result

}
function divideIntervalVertical(row, interval) {
    let int1, int2, p, xp, sum, x0, x1
    let result = []
    const reducer = (accumulator, curr) => accumulator + curr;


    for (let i = 0; i < row.length; i++) {
        sum = row.slice(i, row.length).reduce(reducer)
        p = row[i] / sum
        x0 = interval[2]
        x1 = interval[3]
        xp = p * (x1 - x0) + x0

        int1 = [interval[0], interval[1], x0, xp]
        int2 = [interval[0], interval[1], xp, x1]

        result.push(int1)
        interval = int2
    }
    return result

}
function divideIntervalHorizontal(row, interval) {
    let int1, int2, p, xp, sum, x0, x1
    let result = []
    const reducer = (accumulator, curr) => accumulator + curr;

    for (let i = 0; i < row.length; i++) {
        sum = row.slice(i, row.length).reduce(reducer)
        p = row[i] / sum
        x0 = interval[0]
        x1 = interval[1]
        xp = p * (x1 - x0) + x0
        int1 = [x0, xp, interval[2], interval[3]]
        int2 = [xp, x1, interval[2], interval[3]]



        result.push(int1)

        interval = int2
    }
    return result

}
function squarify(children, row, subdivision, interval, result) {
    mode = 'squarify'
    const reducer = (accumulator, curr) => accumulator + curr;

    let w = Math.min(subdivision[0], subdivision[1])
    let c = children[0]
    //print(c)


    if (children.length == 0) {
        let oo = result
        baul = result
        return oo
    }
    else {

        if (worst(row, w) >= worst(row.concat(c), w)) {
            row = row.concat(c)
            children = children.slice(1, children.length)
            squarify(children, row, subdivision, interval, result)
        }
        else {

            sumRow = row.reduce(reducer)
            sumChildren = children.reduce(reducer)
            p = sumRow / (sumRow + sumChildren)
            if (subdivision[0] >= subdivision[1]) {

                //vertical
                subdivision[0] = subdivision[0] * (1 - p)
                x0 = interval[0]
                x1 = interval[1]
                xp = p * (x1 - x0) + x0
                int1 = [x0, xp, interval[2], interval[3]]
                int1 = divideIntervalVertical(row, int1)
                result = result.concat(int1)
                int2 = [xp, x1, interval[2], interval[3]]
                interval = int2
            }
            else {

                //horizontal
                subdivision[1] = subdivision[1] * (1 - p)
                x0 = interval[2]
                x1 = interval[3]
                xp = p * (x1 - x0) + x0
                int1 = [interval[0], interval[1], x0, xp]
                int1 = divideIntervalHorizontal(row, int1)
                //print('int1 horizontal',int1)
                result = result.concat(int1)
                //print('result so far in 2:',result)

                int2 = [interval[0], interval[1], xp, x1]
                //print('int2 horzl',int2)
                interval = int2

            }
            // result.push(result)
            //print('result so far:',result)
            //print('new subdivision',subdivision)
            row = [children[0]]
            children = children.slice(1, children.length)
            squarify(children, row, subdivision, interval, result)

        }
    }
}
let baul = [];
function normalized(rooms, initialSquareSize) {
    const reducer = (accumulator, curr) => accumulator + curr;
    //print('normalizing areas: rooms',rooms,'intialSquareSize',initialSquareSize)
    let totalArea = initialSquareSize[0] * initialSquareSize[1]
    let totalRoomsArea = rooms.reduce(reducer)
    //print('total area',totalArea,'totalroomsarea',totalRoomsArea)
    let ratio = totalArea / totalRoomsArea
    //print('ratio',ratio)
    normalizedAreas = rooms.map(function (x) { return x * ratio; });
    //print('normalizedAreas',normalizedAreas)
    return normalizedAreas
}
function create_layout_squarify() {
    rooms = roomSizes.sort().reverse()
    queue = normalized(rooms, initialSquareSize)
    let subdivision = initialSquareSize
    let w = Math.min(subdivision[0], subdivision[1])
    let h = Math.max(subdivision[0], subdivision[1])
    let row = [queue[0]]
    let children = queue.slice(1, queue.length)

    squarify(children, row, subdivision, [0, 1, 0, 1], [])

    layout = baul
    return baul

}

//some operations
let p1 = new vertice(windowWidth / 2 - initialSquareSize[0] / 2, windowHeight / 2 - initialSquareSize[1] / 2, 'p1', [255, 255, 0]);
let p2 = new vertice(windowWidth / 2 + initialSquareSize[0] / 2, windowHeight / 2 + initialSquareSize[1] / 2, 'p2', [255, 0, 255]);

let rooms = roomSizes
let plan = [p1.x, p1.y, p2.x, p2.y]
let roomString = '[' + rooms.join(',') + ']'
let toptext = 'This program generates a layout plan for roomsizes of ' + roomString

// draw rectanle given x0,y0,x1,y1
function drawRectangle(plan, layout, song) {
    let a = (layout[1] - layout[0]) * (plan[2] - plan[0]) * (layout[3] - layout[2]) * (plan[3] - plan[1]) / (350 * 350)
    fill(255, 255, 255, Math.floor(255 * a * 2.5));
    rect(plan[0] + layout[0] * (plan[2] - plan[0]), plan[1] + layout[2] * (plan[3] - plan[1]), (layout[1] - layout[0]) * (plan[2] - plan[0]), (layout[3] - layout[2]) * (plan[3] - plan[1]))

}
// given a layout list, //print the reectangles
function drawLayout(plan, rectangles) {
    noFill()
    rect(75, 75, 350, 350)
    strokeWeight(1)
    noFill()

    for (let i = 0; i < rectangles.length; i++) {

        drawRectangle(plan, rectangles[i], songs[i])
        var lastLayout = rectangles[i]
        var r = i

    }

}

function setup() {
    create_layout_squarify()

    r = p1.radious
    createCanvas(windowWidth, windowHeight);
    textAlign(CENTER);
    background(0, 0, 0);
    fill('white')


    strokeWeight(1)
    plan = [p1.x, p1.y, p2.x, p2.y]
    initialSquareSize = [p2.x - p1.x, p2.y - p1.y]
    fill(0)
    hor = parseInt(initialSquareSize[0])
    ver = parseInt(initialSquareSize[1])
    drawLayout(plan, layout)

}

function draw() {
    create_layout_squarify()
    r = p1.radious
    background(50, 50, 50);
    fill('white')
    strokeWeight(1)
    stroke(255, 255, 255);
    plan = [p1.x, p1.y, p2.x, p2.y]
    initialSquareSize = [p2.x - p1.x, p2.y - p1.y]
    fill(0)
    hor = parseInt(initialSquareSize[0])
    ver = parseInt(initialSquareSize[1])
    drawLayout(plan, layout)
}