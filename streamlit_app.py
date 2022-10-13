import streamlit as st
import pandas as pd
import altair as alt


from altair import Color,Scale
from streamlit.components.v1 import html
import numpy as np
from streamlit.elements.image import image_to_url

# Claim the color #
colorOliva='93,92,25'
B = "#4001F4"
G = "#4b917d"
R = "#f037a5"
YG = "#cdf564"
O = "#ff5500"
Y = "#ffa51e"



# Get slides#
def get_slide_data_tomas(df,artists,albums):
    labels = pd.Series([1] * len(df), index=df.index)

    if artists:
        labels &= df['artist'].isin(artists)
    if albums:
        labels &= df['album'].isin(albums)
    
    return labels



# Start#
st.title("Let's analyze some Spotify Data🎤🧑🏻‍🎤📊.")


# Load Data #
@st.cache(allow_output_mutation=True)  # add caching so we load the data only once
def load_data():
    data_path = "spotify_data.csv"
    return pd.read_csv(data_path)


df = load_data()
# Add one colum for listen duration #
df["listen_duration"] = (df["playcount"] * df["duration"]).div(60000)
ourArtist=['Bad Bunny', 'Drake', 'Ed Sheeran', 'keshi', 'ROSALÍA'] #we are only interested in songs of this 5 artists
df=df[df['artist'].isin(ourArtist)]


st.write("Let's look at raw data in the Pandas Data Frame.")

st.write(df)

st.write("Which are the top played songs of the most streamed artists on spotify? ")

# selection
artist_brush = alt.selection_multi(fields = ["artist"])


#selection.multi
artist_chart = alt.Chart(df).mark_bar().encode(
  Color('artist:O',
          scale = Scale(domain=['Bad Bunny', 'Drake', 'Ed Sheeran', 'keshi', 'ROSALÍA'],
                      range=[B, R, YG, O, Y])),
    x = "sum(playcount)",
    y = alt.Y("artist",sort='-x'),
    
).add_selection(artist_brush)

album_chart = alt.Chart(df).mark_bar().encode(
  Color('artist:O',
          scale = Scale(domain=['Bad Bunny', 'Drake', 'Ed Sheeran', 'keshi', 'ROSALÍA'],
                      range=[B, R, YG, O, Y])),
    x = "count()",
    y = alt.Y("album"),
    
).transform_filter(artist_brush)

st.write(artist_chart&album_chart)



cols=st.columns(2)

st.write('Filter dataset by artists and album:')
with cols[0]:
    artists=st.multiselect('artist',df[df['artist'].isin(ourArtist)]['artist'].unique(),default=["ROSALÍA"]) # we add a default so we can plot an initial chart
with cols[1]:
    albums=st.multiselect('album',df[df['artist'].isin(artists)]['album'].unique())

slice_labels=get_slide_data_tomas(df,artists,albums)
st.write("The filtered dataset contains {} songs".format(slice_labels.sum()))

song_count=st.slider('number_songs',
                    min_value=0,
                    max_value=len(slice_labels[slice_labels==1]),
                    value=10)

st.write("From the filtered dataset we are now comparing the top listened {} songs".format(song_count))


ordered_dataset=df[slice_labels].sort_values(by='playcount',ascending=False).head(n=song_count)
st.write(len(ordered_dataset))
song_playcount=ordered_dataset['playcount'].mean()
st.metric('Mean listeners per song','{:,}'.format(song_playcount))
# st.write(ordered_dataset)

chart1=alt.Chart(ordered_dataset).mark_bar().encode(
  Color('artist:O',
          scale = Scale(domain=['Bad Bunny', 'Drake', 'Ed Sheeran', 'keshi', 'ROSALÍA'],
                      range=[B, R, YG, O, Y])),
    x='sum(playcount)',
    y=alt.Y('name',sort='-x'),
    # color='artist'
)

chart2=alt.Chart(ordered_dataset).mark_bar().encode(
  Color('artist:O',
          scale = Scale(domain=['Bad Bunny', 'Drake', 'Ed Sheeran', 'keshi', 'ROSALÍA'],
                      range=[B, R, YG, O, Y])),
    x='sum(playcount)',
    y=alt.Y('album',sort='-x'),
    # color='artist'
)

cols_=st.columns(2)


with cols_[0]:
    st.altair_chart(chart1)
with cols_[1]:
    st.altair_chart(chart2)

countValues=ordered_dataset.groupby(['name'])['playcount'].sum().sort_values()

# Wrapt the javascript as html code
# html(f'<script>var songs={list(countValues.to_dict().keys())};var roomSizes = {list(countValues.to_dict().values())}</script>')
my_html2 =f'<script>var songs={list(countValues.to_dict().keys())};var roomSizes = {list(countValues.to_dict().values())}</script>'+ '''<div style="background-color: lightblue;"><div id="p5_div" style="width:100%;height:auto;"></div><script src="https://cdn.jsdelivr.net/npm/p5@1.4.2/lib/p5.js"></script><script>
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
        let oo = result; baul = result;return oo;
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
</script><body><main></main></body>

'''
# Execute your app
st.write("Visualize the count with squarify")
html(my_html2,width=500, height=500)

############
# Hongyu's part 
# ##############

# Analysis of listening duration#
def get_slide_hongyu(df2,artists):
    labels = pd.Series([1] * len(df), index=df2.index)

    if artists:
        labels &= df2['artist'].isin(artists)
    
    return labels

st.title("Now, Let's see Who has the longest streamed time?")

song_duration = int(ordered_dataset['listen_duration'].max())
st.metric('The top streamed song has been played','{:,}'.format(song_duration),"hours")

album_brush = alt.selection_multi(fields = ["artist"])

chart_song=alt.Chart(df).mark_circle(size = 100 ).encode(
    Color("artist",
            scale = Scale(domain=['Bad Bunny', 'Drake', 'Ed Sheeran', 'keshi', 'ROSALÍA'],
                      range=[B, R, YG, O, Y])),
    y='listen_duration:Q',
    opacity=alt.value(0.5),
    x=alt.Y('artist',sort='-x')
).add_selection(album_brush).properties(width=400)

chart_album=alt.Chart(df).mark_point(size = 80).encode( 
    Color("artist",
            scale = Scale(domain=['Bad Bunny', 'Drake', 'Ed Sheeran', 'keshi', 'ROSALÍA'],
                      range=[B, R, YG, O, Y])), 
    x='sum(listen_duration)',
    y=alt.Y('album',sort='-x')
).transform_filter(album_brush).properties(width=400,height = 500)

st.write(chart_song & chart_album)

# Select artist and see their streamed time #

cols_duration=st.columns(2)
with cols_duration[0]:
    artists= st.multiselect('Artist', df[df['artist'].isin(ourArtist)]["artist"].unique(),default=['Ed Sheeran', 'Drake'])
slice_labels_hongyu = get_slide_hongyu(df,artists)

with cols_duration[1]:
    song_count_duration =st.slider('number_songs',
                    min_value=0,
                    max_value=40,
                    value= 40 if (len(slice_labels_hongyu[slice_labels_hongyu==1])>40) 
                    else (len(slice_labels_hongyu[slice_labels_hongyu==1])))

ordered_dataset_hongyu=df[slice_labels_hongyu].sort_values(by='listen_duration',ascending=False).head(song_count_duration)

st.write("The filtered dataset contains {} songs".format(slice_labels_hongyu.sum()))
st.write("From the filtered dataset we are now comparing the top streamed {} songs by listening time".format(song_count_duration))


duration_chart_song=alt.Chart(ordered_dataset_hongyu).mark_circle(size=60).encode(
    Color("artist",
            scale = Scale(domain=['Bad Bunny', 'Drake', 'Ed Sheeran', 'keshi', 'ROSALÍA'],
                      range=[B, R, YG, O, Y])),
    y='sum(listen_duration)',
    x=alt.Y('name',sort='-x'),
    
).properties(width=700)

duration_chart_album=alt.Chart(ordered_dataset_hongyu).mark_bar().encode(
    Color("artist",
            scale = Scale(domain=['Bad Bunny', 'Drake', 'Ed Sheeran', 'keshi', 'ROSALÍA'],
                      range=[B, R, YG, O, Y])),    
    x='sum(listen_duration)',
    y=alt.Y('album',sort='-x'),
).properties(width=700)

# st.altair_chart(duration_chart)
st.write(duration_chart_song)
st.write(duration_chart_album)




st.markdown("This project was created by Hongyu Mao and Tomas Cabezon for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")

