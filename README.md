# Music Recommendation Application
## Introduction
> **User story:**
> As music fan, I want to find song, so I can listen it.

Dataset ([example](https://www.kaggle.com/datasets/josephinelsy/spotify-top-hit-playlist-2010-2022)) with spotify library

## Part 1 
### _Dataset Summary_
> **Job story:**
> When the application is run, I want to know a summary info about primary dataset 
> (such as quantity of songs or artists, date range etc.) so I can create a search query more accurately 

#### Requirements
> [!IMPORTANT] 
> Use only built-in python functions 

1) Read dataset and store it in a appropriate data structure ✅;
2) Write a function to get shape of dataset ✅;
3) Write a function which returns minimum and maximum values from a column ✅;
4) Write a function which returns top-n artists with the highest songs count in dataset (with count itself) ✅;
5) Using **argparse** tool to implement an application console call with positional and optional arguments ✅.

> #### Topics:
> 
> `Type Annotation`, `FileReader`, `Argparse`
## Part 2
### _Pre-built playlist_
> **Job story:**
> When I run the function,
> I want to obtain a playlist with n-songs, 
> so I can choose a playlist by type (artist or genre or years range or track's audio features) to listen.


#### Requirements
1) Write a function which returns top-n songs by artist;
2) Write a function which returns top-n songs for a genre;
3) Write a function which returns top-n songs by period;
4) Write a function which returns the most top-n similar songs by sound to current (by link);


> #### Topics:
> 
> `Sorting`, `Euclidean Distance`, `Cosine Similarity`

## Part 3
### _Text Search_
> **Job story:**
> When I run the function and pass text request,
> I want to get a response with appropriate tracks 
> so I can find and select the song I'm looking for.

#### Requirements
1) Preprocess tracks text (tokenization, stemming / lemmatization, stop words removal);
2) Write a function which takes some text query and returns top-n similar texts using Hamming distance or Jaccard index;
3) Implement BoW and TF-IDF models and update previous function using Cosine similarity.

> #### Topics:
> 
> `Regular Expressions`,`NLP`, `Word Embedding`
#### Requirements

## Part 4
### _Info Augmentation_

> **Job story:**
> When I run the function,
> I want to  ...
> so I  ...


> #### Topics:
> 
> `Requests`, `Beautiful Soup`

#### Requirements