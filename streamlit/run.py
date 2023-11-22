import streamlit as st
import pandas as pd
import plotly.express as px
import lastfm
from streamlit_agraph import agraph, Node, Edge, Config

data = pd.read_csv("data/playlist_2010to2022.csv")
data.artist_genres = data.artist_genres.apply(lambda x: eval(x))
data.track_id = data.track_id.apply(lambda x: f"https://open.spotify.com/track/{x}")

if __name__ == "__main__":
    st.set_page_config(
        page_title="Recommendation Project",
        page_icon="🎧",
        initial_sidebar_state="collapsed",
    )

    with st.sidebar:
        st.write("Some information about the project")
        st.link_button(
            "Dataset link",
            "https://www.kaggle.com/datasets/josephinelsy/spotify-top-hit-playlist-2010-2022",
        )

    st.title("Recommendation Project")

    # statistic part
    st.subheader("Library statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        _value = data.artist_name.unique().size
        st.metric(label="Artists", value=_value)
    with col2:
        _value = data.track_name.unique().size
        st.metric(label="Songs", value=_value)
    with col3:
        _value = pd.Series(data.artist_genres.sum()).unique().size
        st.metric(label="Genres", value=_value)

    # songs
    st.subheader("Top artists and their songs by genre")
    genres = pd.Series(data.artist_genres.sum()).value_counts().index
    genre_options = st.multiselect("Choose genres", genres)
    TOP = 10
    if genre_options:
        _genre_apply = data.artist_genres.apply(
            lambda x: True if set(x).intersection(set(genre_options)) else False
        )
        target_artists = data[_genre_apply].artist_name.value_counts().index[:TOP]
    else:
        target_artists = data.artist_name.value_counts().index[:TOP]

    _data = data[data.artist_name.isin(target_artists)]
    fig = px.sunburst(_data, path=["artist_name", "track_name"])
    st.plotly_chart(fig, use_container_width=True)

    # table
    st.subheader("Top Hits of the year")

    years = sorted(data.year.unique())
    year_option = st.selectbox("Choose the year", years)

    target_columns = ["artist_name", "track_name", "track_popularity", "track_id"]
    _data = data[data.year == year_option][target_columns]
    # _data.track_id = _data.track_id.apply(lambda x: f'<a target="_blank" href="{x}">Listen▶️</a>')
    _data = _data.style.background_gradient(subset=["track_popularity"])
    st.dataframe(
        _data,
        column_config={
            "artist_name": "Artist",
            "track_name": "Track name",
            "track_popularity": "Popularity",
            "track_id": st.column_config.LinkColumn("Track link"),
        },
        hide_index=True,
    )

    # Music
    st.subheader("Artist info")
    artist_input = st.text_input("Enter artist name", placeholder="Drake for example")
    if artist_input:
        is_ok = False
        with st.spinner("Wait for it..."):
            bio = lastfm.parse_bio(artist_input, False)
            if bio == "Artist does not exist":
                st.error(bio)
            else:
                is_ok = True
                st.toast("Artist is found!", icon="🔥")

                image_url = lastfm.parse_photo(artist_input)
                st.image(image_url)
                tags = lastfm.parse_tags(artist_input)
                tags_options = st.multiselect("Genges", tags, tags, disabled=True)

                bio_text = st.text_area("Artist bio", bio, height=300)

            if is_ok:
                similar_artist = lastfm.similar_artists(artist_input)

                nodes = []
                edges = []
                nodes.append(
                    Node(
                        id=artist_input,
                        label=artist_input,
                        size=50,
                        shape="circularImage",
                        image=image_url
                        # color="#ff4c78")
                    )
                )

                for artist in similar_artist:
                    nodes.append(
                        Node(
                            id=artist,
                            label=artist,
                            size=25,
                            shape="circularImage",
                            image=lastfm.parse_photo(artist),
                        )
                        # color="#198ba3")
                    )
                    edges.append(
                        Edge(
                            source=artist,
                            target=artist_input,
                        )
                    )
                config = Config(
                    directed=False,
                    physics=True,
                    hierarchical=False,
                )

                graph = agraph(nodes=nodes, edges=edges, config=config)

                st.link_button(
                    "Open in Last.fm", f"https://www.last.fm/music/{artist_input}"
                )

        st.balloons()
