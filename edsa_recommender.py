"""

    Streamlit webserver-based Recommender Engine.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: !! Do not remove/modify the code delimited by dashes !!

    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st

# Data handling dependencies
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from plotly import graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
from PIL import Image

# Custom Libraries
from utils.data_loader import load_movie_titles
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model

# Data Loading
title_list = load_movie_titles('resources/data/movies.csv')
train = pd.read_csv("resources/data/train.csv")
train = train.drop(columns = 'timestamp', axis = 1)

# App declaration
def main():

    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["Recommender System","Solution Overview","EDA","About Us"]

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    page_selection = st.sidebar.selectbox("Choose Option", page_options)
    if page_selection == "Recommender System":
        # Header contents
        st.write('# Movie Recommender Engine')
        st.write('### EXPLORE Data Science Academy Unsupervised Predict')
        st.image('resources/imgs/Image_header.png',use_column_width=True)
        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('Fisrt Option',title_list[14930:15200])
        movie_2 = st.selectbox('Second Option',title_list[25055:25255])
        movie_3 = st.selectbox('Third Option',title_list[21100:21200])
        fav_movies = [movie_1,movie_2,movie_3]

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


        if sys == 'Collaborative Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = collab_model(movie_list=fav_movies,
                                                           top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    if page_selection == "Solution Overview":
        st.title("Solution Overview")
        st.write("Describe your winning approach on this page")

    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.
    if page_selection == "EDA":


        st.markdown("""# Rating Distributions""")
        data = train['rating'].value_counts().sort_index(ascending=False)
        trace = go.Bar(x = data.index,
                       text = ['{:.1f} %'.format(val) for val in (data.values / train.shape[0] * 100)],
                       textposition = 'auto',
                       textfont = dict(color = '#000000'),
                       y = data.values,
                       )
        # Create layout
        layout = dict(title = 'Distribution Of {} movie-ratings'.format(train.shape[0]),
                      xaxis = dict(title = 'Rating'),
                      yaxis = dict(title = 'Count'))
        # Create plot
        fig = go.Figure(data=[trace], layout=layout)
        st.plotly_chart(fig)

        st.markdown(""" 

            We can see that over 26% of all ratings in the data are 4, and very few ratings are 0.5, 1.0, 1.5, 2.5 and 3.0. 
            Low rating movies mean they are generally really bad and not highly recommended by users.
            """)





        st.markdown("""#  Number of ratings per movie""")
        data = train.groupby('movieId')['rating'].count().clip(upper=50)

        # Create trace
        trace = go.Histogram(x = data.values,
                             name = 'Ratings',
                             xbins = dict(start = 0,
                                          end = 50,
                                          size = 2))
        # Create layout
        layout = go.Layout(title = 'Distribution Of Number of Ratings Per movie (Clipped at 100)',
                           xaxis = dict(title = 'Number of Ratings Per movie'),
                           yaxis = dict(title = 'Count'),
                           bargap = 0.2)

        # Create plot
        fig = go.Figure(data=[trace], layout=layout)
        st.plotly_chart(fig)





        st.markdown("""#  Number of ratings per user""")
        data = train.groupby('userId')['rating'].count().clip(upper=50)

        # Create trace
        trace = go.Histogram(x = data.values,
                             name = 'Ratings',
                             xbins = dict(start = 0,
                                          end = 50,
                                          size = 2))
        # Create layout
        layout = go.Layout(title = 'Distribution Of Number of Ratings Per User (Clipped at 50)',
                           xaxis = dict(title = 'Ratings Per User'),
                           yaxis = dict(title = 'Count'),
                           bargap = 0.2)

        # Create plot
        fig = go.Figure(data=[trace], layout=layout)
        st.plotly_chart(fig)


    if page_selection == "About Us":

            st.markdown("# Data Lux")
            st.markdown("## ")
            st.markdown("""
                Data Lux is an information technology company that provides an 
                enterprise data science platform.

                We transform how you consume data by building Information Systems 
                that offer solutions for data collection, management and analysis.

                Simply put, we transform data to inform action.
            """)
            st.markdown("## Mission")

            st.markdown(""" 
                We develop data analytics and machine learning solutions 
                by aggregating disparate data sources to bring creativity and innovation in 
                the management of any business """)

            st.markdown("## Vision")

            st.markdown(""" 
                To become the most valuable data analytics partner in Africa and beyond.

                     """)

            st.markdown("## Values")

            st.markdown(""" 
                Customer Satisfaction, Respect & Honesty

                     """)

            st.markdown("## Team")



            with st.container():
                image_col, text_col = st.columns((1,2))
                with image_col:
                    st.image("resources/imgs/mama.jpeg")

                with text_col:
                    st.subheader("Diana Okeyo(Tech Lead)")
                    st.write("""
                        Data Lux Tech lead,
                        Solutions Architect and Scrum Master
                        """)
                    
            with st.container():
                image_col, text_col = st.columns((1,2))
                with image_col:
                    st.image("resources/imgs/pic.jpeg")

                with text_col:
                    st.subheader("Raphael Mbonu (Ml Engineer)")
                    st.write("""
                        Senior Machine Learning and 
                        Artificial Intelligence Developer
                        """)
                    
            with st.container():
                image_col, text_col = st.columns((1,2))
                with image_col:
                    st.image("resources/imgs/ed.jpeg")

                with text_col:
                    st.subheader("Edward Ogbei(Data analyst)")
                    st.write("""
                        Senior Data Analyst and
                        QA Consultant
                        """)
                    
            with st.container():
                image_col, text_col = st.columns((1,2))
                with image_col:
                    st.image("resources/imgs/colin.jpeg")

                with text_col:
                    st.subheader("Colin Mburugu (UI/UX Designer)")
                    st.write("""
                        Senior User Interface/Experience Designer
                        Cloud Engineer
                        """)



            with st.container():
                image_col, text_col = st.columns((1,2))
                with image_col:
                    st.image("resources/imgs/gab.jpeg")

                with text_col:
                    st.subheader("Gabriel Asiegbu (Business Analyst)")
                    st.write("""
                        Business Analyst and
                        Project Management lead
                        """)
                    







if __name__ == '__main__':
    main()
