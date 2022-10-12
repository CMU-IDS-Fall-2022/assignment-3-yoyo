import streamlit as st
import pandas as pd
import altair as alt
from streamlit.components.v1 import html

def get_slide_data_tomas(df,artists,albums):
    labels = pd.Series([1] * len(df), index=df.index)

    if artists:
        labels &= df['artist'].isin(artists)
    if albums:
        labels &= df['album'].isin(albums)
    
    return labels

st.title("Let's analyze some Spotify Data 🐧📊.")

@st.cache  # add caching so we load the data only once
def load_data():
    data_path = "spotify_data.csv"
    return pd.read_csv(data_path)

df = load_data()
ourArtist=['Bad Bunny', 'Drake', 'Ed Sheeran', 'keshi', 'ROSALÍA'] #we are only interested in songs of this 5 artists

st.write("Let's look at raw data in the Pandas Data Frame.")

st.write(df)

st.write("Which are the top played songs of the most streamed artists on spotify? ")

artist_chart=alt.Chart(df[df['artist'].isin(ourArtist)]).mark_bar().encode(
    x='sum(playcount)',
    y=alt.Y('artist',sort='-x'),
    color='artist'
)
st.altair_chart(artist_chart)
# st.write("total songs",df['artist'].count())
cols=st.columns(2)

us=['Drake','keshi']
with cols[0]:
    artists=st.multiselect('artist',df[df['artist'].isin(ourArtist)]['artist'].unique())
with cols[1]:
    albums=st.multiselect('album',df[df['artist'].isin(artists)]['album'].unique())

# print(artists)
slice_labels=get_slide_data_tomas(df,artists,albums)

song_count=st.slider('number_songs',
                    min_value=0,
                    max_value=len(slice_labels[slice_labels==1]),
                    value=(len(slice_labels[slice_labels==1])))

st.write("The sliced dataset contains {} elements".format(slice_labels.sum()))


ordered_dataset=df[slice_labels].sort_values(by='playcount',ascending=False).head(song_count)
song_playcount=ordered_dataset['playcount'].mean()
st.metric('Mean listeners per song',song_playcount)
# st.write(ordered_dataset)

chart=alt.Chart(ordered_dataset).mark_bar().encode(
    x='sum(playcount)',
    y=alt.Y('name',sort='-x'),
    color='artist'
)

st.altair_chart(chart)


# chart = alt.Chart(df).mark_point().encode(
#     x=alt.X("body_mass_g", scale=alt.Scale(zero=False)),
#     y=alt.Y("flipper_length_mm", scale=alt.Scale(zero=False)),
#     color=alt.Y("species")
# ).properties(
#     width=600, height=400
# ).interactive()

# st.write(chart)

st.markdown("This project was created by Student1 and Student2 for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")


# Define your javascript
my_js = """
alert("Hola mundo");
"""

# Wrapt the javascript as html code
my_html = '''<div style="width:1000px;height: 500px;background-color: lightblue;"><div id="p5_div" style="width:100%;height:auto;"></div><script src="https://cdn.jsdelivr.net/npm/p5@1.4.2/lib/p5.js"></script><script>
function setup() {
    fill(200)
    var myCanvas = createCanvas(800, 800);
    myCanvas.parent("p5_div");
}

function draw() {
    if (mouseIsPressed) {
        fill(0);
    } else {
        fill(255);
    }
    ellipse(mouseX, mouseY, 80, 80);
}
</script><body><main></main></body>'

'''
# Execute your app
st.title("Javascript example")
html(my_html)