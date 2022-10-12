
//intital parameters
var play = true

let windowWidth = 500
let windowHeight = 500
////console.log('windowWidth,windowHeight',windowWidth,windowHeight)
roomSizes=roomSizes.sort().reverse()
let initialSquareSize = [350, 350]
var layout = [[0, 1, 0, 1]];
let depth = 1;
let mode;




function convertToPercentages(l) {
    const reducer = (accumulator, curr) => accumulator + curr;
    sum = l.reduce(reducer)
    // ////console.log(sum)
    result = []
    l.forEach(x => {
        perc = x / sum * 100
        //////console.log(x,perc)
        result.push(perc)
    })
    console.log("CONVERTED", l, "INTO", result)
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

    draw() {
        if (this.moving) {
            this.x = mouseX
            this.y = mouseY
            //print('moving', this.name)
            fill('red')
            ellipse(this.x, this.y, this.radious * 2, this.radious * 2)


        }
        else {

            fill(this.color[0], this.color[1], this.color[2])
            ellipse(this.x, this.y, this.radious, this.radious)
        }

    }

    clicked(x, y) {
        let d = dist(x, y, this.x, this.y)
        if (d < this.around) {

            this.moving = !this.moving
        }
    }
}

function create_treemap() {
    ////console.log('Recalculating floor plan with treemap d=' + str(depth))
    let interval = [0, 1, 0, 1]
    let queue = [[0, interval]]
    // ////console.log(queue[0])
    let solution = []
    let counter = 0 // this is a counter that sets a limit of iterations
    let limit = 1000
    while (queue.length > 0 && counter < limit) {

        elem = queue.pop()
        d = elem[0]
        interval = elem[1]
        // ////console.log('elem',elem)
        // ////console.log('actual depth', d)
        // ////console.log('interval',interval)

        if (d >= depth) {
            solution.push(interval)

        }
        else {
            p = Math.random()

            while (0.3 > p || p > 0.7) {
                // ////console.log('recalculating p',p)
                p = Math.random()

            }
            // ////console.log('final p',p)
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


    // //print('solution',solution)
    layout = solution
    return solution
}

function worst(row, w) {
    
    const reducer = (accumulator, curr) => accumulator + curr;
    sum = row.reduce(reducer)
    rMax = Math.max(...row)
    rMin = Math.min(...row)
    // //print(row)
    // //print(sum, rMax, rMin)
    m1=((w ** 2) * rMax) / (sum ** 2)
    m2=(sum ** 2) / ((w ** 2)* rMin)
    result=Math.max(m1, m2)
    // result= Math.max(((width ** 2) * rowMax) / (sum ** 2), (sum ** 2) / ((width ** 2) * rowMin));
    //print('calculating worst with row, w,rmax,rmin,sum,m1,m2:',row,w,rMax,rMin,sum,m1,m2,'result=',result)
    return result

}
function divideIntervalVertical(row, interval) {
    let int1,int2,p,xp,sum,x0,x1
    //print('in divideIntervalVertical row,interval',row,interval)
    let result = []
    const reducer = (accumulator, curr) => accumulator + curr;
    
    
    for (let i = 0; i < row.length; i++) {
        sum = row.slice(i,row.length).reduce(reducer)
        //print('row[i],sum',row[i],sum)
        p=row[i]/sum
        x0 = interval[2]
        x1 = interval[3]
        xp = p * (x1 - x0) + x0
        
        int1 = [interval[0], interval[1], x0, xp]
        int2 = [interval[0], interval[1], xp, x1]
        
        //print('p,x0,x1,xp',p,x0,x1,xp)
        //print('int1,int2',int1,int2)
        // if()
        result.push(int1)
        interval=int2
    }
    return result

}
function divideIntervalHorizontal(row, interval) {
    let int1,int2,p,xp,sum,x0,x1
    //print('in divideIntervaHrozontl row,interval',row,interval)
    let result = []
    const reducer = (accumulator, curr) => accumulator + curr;
   
    for (let i = 0; i < row.length; i++) {
        sum = row.slice(i,row.length).reduce(reducer)
        //print('row[i],sum',row[i],sum)
        p=row[i]/sum
        x0 = interval[0]
        x1 = interval[1]
        xp = p * (x1 - x0) + x0
        int1 = [x0, xp, interval[2], interval[3]]
        int2 = [xp, x1, interval[2], interval[3]]
        
        //print('p,x0,x1,xp',p,x0,x1,xp)
        //print('int1,int2',int1,int2)
         
        result.push(int1)
        
        interval=int2
    }
    return result

}
function squarify(children, row, subdivision, interval, result) {
    mode='squarify'
    
    //print('in function squarify: children,, row, subdivision, interval, result',children,row, subdivision, interval, result)
    const reducer = (accumulator, curr) => accumulator + curr;

    let w = Math.min(subdivision[0], subdivision[1])
    let c = children[0]
    //print(c)

    ////print(worst(childer_area,w))
    if (children.length == 0) {
        //print('base case squarify!!! Result:',result)
        // result=result.push(interval)
        let oo=result
        baul=result
        //print('base case squarify!!! Result baul:',baul)
        return oo
    }
    else {

        if (worst(row, w) >= worst(row.concat(c), w)) {
            //print('in 1: row,children',row,children)
            row = row.concat(c)
            children = children.slice(1, children.length)
            squarify(children, row, subdivision, interval, result)
        }
        else {
            //print('in 2: row,children',row,children)
            // if (row.length=1){
            //     sumRow=row[0]
            // }
            sumRow = row.reduce(reducer)
            //print('sumRow',sumRow)
            //print('interval',interval)
            sumChildren = children.reduce(reducer)
            p = sumRow / (sumRow + sumChildren)
            //print('p = sumRow / (sumRow + sumChildren)',p ,sumRow ,sumChildren)
            if (subdivision[0] >= subdivision[1]) {
                //print('-\n-\n-\n-> vertical')
                //vertical
                subdivision[0]=subdivision[0]*(1-p)
                x0 = interval[0]
                x1 = interval[1]
                xp = p * (x1 - x0) + x0
                int1 = [x0, xp, interval[2], interval[3]]
                int1 = divideIntervalVertical(row, int1)
                //print('int1 vertical',int1)
                result = result.concat(int1)
                //print('result so far in 2:',result)
                int2 = [xp, x1, interval[2], interval[3]]
                //print('int2 vertical',int2)
                interval = int2
            }
            else {
                //print('-\n-\n-\n-> horizontal')
                //horizontal
                subdivision[1]=subdivision[1]*(1-p)
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
let baul=[];
function normalized(rooms,initialSquareSize){
    const reducer = (accumulator, curr) => accumulator + curr;
    //print('normalizing areas: rooms',rooms,'intialSquareSize',initialSquareSize)
    let totalArea=initialSquareSize[0]*initialSquareSize[1]
    let totalRoomsArea=rooms.reduce(reducer)
    //print('total area',totalArea,'totalroomsarea',totalRoomsArea)
    let ratio=totalArea/totalRoomsArea
    //print('ratio',ratio)
    normalizedAreas=rooms.map(function(x) { return x * ratio; });
    //print('normalizedAreas',normalizedAreas)
    return  normalizedAreas
}
function create_layout_squarify() {
    rooms=roomSizes.sort().reverse()
    // NORMALIZE AREAS!!!
    ////console.log('Recalculating floor plan with squarify')
    queue = normalized(rooms,initialSquareSize)
    ////console.log(queue)
    let subdivision = initialSquareSize
    let w = Math.min(subdivision[0], subdivision[1])
    let h = Math.max(subdivision[0], subdivision[1])
    let row = [queue[0]]
    let children = queue.slice(1, queue.length)

    //console.log('rooms',rooms)
    //console.log('row',row)
    //console.log('children',children)
    //console.log('w',w)

    squarify(children, row, subdivision, [0,1,0,1], [])

    //print('_______FINAL RESULT______',baul)
    layout=baul
    //print('solution=', baul)
    return baul

}

//some operations
let p1 = new vertice(windowWidth / 2 - initialSquareSize[0] / 2, windowHeight / 2 - initialSquareSize[1] / 2, 'p1', [255, 255, 0]);
let p2 = new vertice(windowWidth / 2 + initialSquareSize[0] / 2, windowHeight / 2 + initialSquareSize[1] / 2, 'p2', [255, 0, 255]);

let rooms = roomSizes
////console.log('converted room sizes', roomSizes, 'into percentages', rooms)
let plan = [p1.x, p1.y, p2.x, p2.y]
let roomString = '[' + rooms.join(',') + ']'
let toptext = 'This program generates a layout plan for roomsizes of ' + roomString
//console.log(toptext)

// draw rectanle given x0,y0,x1,y1
function drawRectangle(plan, layout,song) {
    // print('->drawing rectangle for',song)
    let a =(layout[1] - layout[0]) * (plan[2] - plan[0])* (layout[3] - layout[2]) * (plan[3] - plan[1])/(350*350)
    console.log('width height',(layout[1] - layout[0]) * (plan[2] - plan[0]),(layout[3] - layout[2]) * (plan[3] - plan[1]),a)
    console.log('fill',0,255,Math.floor(a*100),Math.floor(255*a))
    fill(255,75,75,Math.floor(255*a*2.5));
    rect(plan[0] + layout[0] * (plan[2] - plan[0]), plan[1] + layout[2] * (plan[3] - plan[1]), (layout[1] - layout[0]) * (plan[2] - plan[0]), (layout[3] - layout[2]) * (plan[3] - plan[1]))
    
}

// given a layout list, //print the reectangles
function drawLayout(plan, rectangles) {
    ////console.log('plan', plan)
    noFill()
    rect(75,75,350,350)
    strokeWeight(1)
    noFill()
    
    for (let i = 0; i < rectangles.length; i++) {

       
        // //console.log(i, ':(', rectangles[i][0] * 100, rectangles[i][2] * 100, ')(', rectangles[i][1] * 100, rectangles[i][3] * 100)
        drawRectangle(plan, rectangles[i],songs[i])
        var lastLayout=rectangles[i]
        var r=i
        
    }
        
}



function setup() {
    create_layout_squarify()
    //  background(155);
    // text(toptext,10,10,50,50);
    r = p1.radious
    // changeValue()
    createCanvas(windowWidth, windowHeight);
    textAlign(CENTER);
    background(250);
    fill('black')
    // text(toptext,20,windowHeight-40,500,windowHeight-10);
    
    strokeWeight(1)
    // p1.draw()
    // p2.draw()
    plan = [p1.x, p1.y, p2.x, p2.y]
    initialSquareSize=[p2.x-p1.x,p2.y-p1.y]
    fill(0)
    hor=parseInt(initialSquareSize[0])
    ver=parseInt(initialSquareSize[1])
    // changeValue()
    // text('[ '+str(hor)+', '+str(ver)+' ]', 0, windowHeight-30, windowWidth, windowHeight);
    // textAlign(CENTER)
    print(plan)
    print(layout)
    drawLayout(plan, layout)
    
}

// function draw() {
//     create_layout_squarify()
//     //  background(155);
//     // text(toptext,10,10,50,50);
//     r = p1.radious
//     // changeValue()
//     // createCanvas(windowWidth, windowHeight);
//     // textAlign(CENTER);
//     background(250);
//     fill('black')
//     // text(toptext,20,windowHeight-40,500,windowHeight-10);
    
//     strokeWeight(1)
//     // p1.draw()
//     // p2.draw()
//     plan = [p1.x, p1.y, p2.x, p2.y]
//     initialSquareSize=[p2.x-p1.x,p2.y-p1.y]
//     fill(0)
//     hor=parseInt(initialSquareSize[0])
//     ver=parseInt(initialSquareSize[1])
//     // changeValue()
//     // text('[ '+str(hor)+', '+str(ver)+' ]', 0, windowHeight-30, windowWidth, windowHeight);
//     // textAlign(CENTER)
//     // // print(roomSizes)
//     drawLayout(plan, layout)
// }
//     // //print('drawing')
//     background(250);
//     fill('black')
//     // text(toptext,20,windowHeight-40,500,windowHeight-10);
    
//     strokeWeight(1)
//     // p1.draw()
//     // p2.draw()
//     plan = [p1.x, p1.y, p2.x, p2.y]
//     initialSquareSize=[p2.x-p1.x,p2.y-p1.y]
//     fill(0)
//     hor=parseInt(initialSquareSize[0])
//     ver=parseInt(initialSquareSize[1])
//     // changeValue()
//     text('[ '+str(hor)+', '+str(ver)+' ]', 0, windowHeight-30, windowWidth, windowHeight);
//     textAlign(CENTER)
//     // ////console.log(plan)
//     if (play) {
//         // text('Play=True!', width / 2, height / 2);

//         // rectangles=  [[0, 1, 0, 0.5], [0, 1, 0.5, 1]]
//         drawLayout(plan, layout)
//         // play = false
//         // text(toptext,10,10,50,50);
//         text(toptext, 10, 20, 500, 500);
//     }
//     else {

//         noFill();

//         // text('Play=False!', width / 2, height / 2);

//     }
//     // text(toptext,10,10,50,50);

// }

