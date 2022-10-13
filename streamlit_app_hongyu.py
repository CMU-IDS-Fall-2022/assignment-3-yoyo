import streamlit as st
import pandas as pd
import altair as alt
from streamlit.components.v1 import html
from altair import Color,Scale

  # add caching so we load the data only once
@st.cache(allow_output_mutation=True)
def load_data():
    data_path = "spotify_data.csv"
    return pd.read_csv(data_path)

df = load_data()
df2 = df.copy()
ourArtist=['Bad Bunny', 'Drake', 'Ed Sheeran', 'keshi', 'ROSALÍA']

B = "#4001F4"
G = "#4b917d"
R = "#f037a5"
YG = "#cdf564"
O = "#ff5500"
Y = "#ffa51e"


# Add a new colum for listening time sum#
df2["listen_duration"] = df2["playcount"] * df2["duration"]


# Who has the longest playing time#
st.header("Who has the longest playing time?")
st.markdown("See the different ")

album_brush = alt.selection_multi(fields = ["artist"])

chart_song=alt.Chart(df2[df2['artist'].isin(ourArtist)]).mark_circle(size = 100 ).encode(
    Color("artist",
            scale = Scale(domain=['Bad Bunny', 'Drake', 'Ed Sheeran', 'keshi', 'ROSALÍA'],
                      range=[B, R, YG, O, Y])),
    y='listen_duration:Q',
    opacity=alt.value(0.5),
    x=alt.Y('artist',sort='-x')
).add_selection(album_brush).properties(width=500)

chart_album=alt.Chart(df2[df2['artist'].isin(ourArtist)]).mark_point(size = 80).encode( 
    Color("artist",
            scale = Scale(domain=['Bad Bunny', 'Drake', 'Ed Sheeran', 'keshi', 'ROSALÍA'],
                      range=[B, R, YG, O, Y])), 
    x='sum(listen_duration)',
    y=alt.Y('album',sort='-x')
).transform_filter(album_brush).properties(width=500,height = 500)

st.write(chart_song & chart_album)

# Who has the longest playing time#

def get_slide_hongyu(df2,artists):
    labels = pd.Series([1] * len(df), index=df2.index)

    if artists:
        labels &= df2['artist'].isin(artists)
    
    return labels


# select the artist & albums to see the listening duration #

cols_duration=st.columns(2)
with cols_duration[0]:
    artists = st.multiselect('Artist', df2[df2['artist'].isin(ourArtist)]["artist"].unique())
slice_labels_hongyu = get_slide_hongyu(df2,artists)

with cols_duration[1]:
    song_count_duration =st.slider('number_songs',
                    min_value=0,
                    max_value=40,
                    value= 40 if (len(slice_labels_hongyu[slice_labels_hongyu==1])>40) 
                    else (len(slice_labels_hongyu[slice_labels_hongyu==1])))

ordered_dataset_hongyu=df2[slice_labels_hongyu].sort_values(by='listen_duration',ascending=False).head(song_count_duration)

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


