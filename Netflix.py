
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import re



st.set_page_config(
    layout="wide",
    page_title="Netflix Dashboard"
)                                                                                    #define layout and page title




df= pd.read_csv('netflix_titles.csv')    # read file with pandas
df.drop('director' , axis = 1 , inplace =True)   #drop column as it is not necessary for analysis
df_sample= df.head(15) #show sample of data



df['country'].replace(np.nan, 'United States' , inplace = True ) #replace null values with the most repeated value
df['rating'].replace(np.nan, 'TV-MA' , inplace = True )  #replace null values with the most repeated value
df['duration'].replace(np.nan, '90 min' , inplace = True )  #replace null values with the most repeated value
df['cast'].replace(np.nan, 'David Attenborough' , inplace = True )   #replace null values with the most repeated value
df['date_added'].replace(np.nan, 'January 1, 2020' , inplace = True )   #replace null values with the most repeated value

df['rating'].replace('74 min', 'TV-MA' , inplace = True )  #replace null values with the most repeated value
df['rating'].replace('84 min', 'TV-MA' , inplace = True )  #replace null values with the most repeated value
df['rating'].replace('66 min', 'TV-MA' , inplace = True )  #replace null values with the most repeated value


df['movies'] = np.where(df['duration'].str.contains('min', case=False, na=False), df['duration'], np.nan) #extract movies only
df['Tv show'] = np.where(df['duration'].str.contains('Season', case=False, na=False), df['duration'], np.nan) #extract Tv Shows only

def clean_movies(value):                                               ##function to extract number of mins 
  if pd.notnull(value):
    # replace M with empty char
    value = value.replace('min', '') 
    value = value.replace(" " , '')
    return value
  else: return value


def clean_tv_show(value):                                              ##function to extract number of seasons
  if pd.notnull(value):
      value = value.split(' ')
      return value[0]
  else:
      return value

df['movies'] = df['movies'].apply(clean_movies)               ##applying function
df['Tv show'] = df['Tv show'].apply(clean_tv_show)            ##applying function

df['movies'].replace(np.nan, 0 , inplace = True)              ###replace null values with 0 to make it integer in dtype to apply analysis
df['movies'] = df['movies'].astype(int)                       ###make it integer in dtype

df['Tv show'].replace(np.nan, 0 , inplace = True )            ###replace null values with 0 to make it integer in dtype to apply analysis
df['Tv show'] = df['Tv show'].astype(int)                     ###make it integer in dtype


genre = set()                                                 ### empty set
genre1={}                                                     ### empty dictionary
for index , value in list(df['listed_in'].items()):           ### extract genres of movies and Tv Shows
    value = value.replace(' ', '')                            ### remove space
    value = value.lower()                                     ### lower case
    values = set(re.split(r',\s*|\s*&\s*', value))            ### split by ',' or '&'
    genre = set.union(genre , values)                         ###make one set of two sets
    for word in values:
        genre1[word] = genre1.get(word , 0) +1                ###count occurance of each genre

genre1 = pd.DataFrame(genre1.items(), columns =['type', 'frequency'])      ###apply results to a dataframe





#what are the top five countries ?
df1 = df['country'].value_counts().head(5).reset_index()                                                    ###get top five countries   
f1 = px.pie(df1, values='count', names='country', hole=.2, color_discrete_sequence=['#8B0000'])             ###plot it with plotly




# **what are the top five genres of movies ??**
df2= genre1.sort_values(by='frequency' , ascending=False)                                                   ###get top five genres
f2 = px.pie(df2.head(5), values='frequency', names='type', hole=.2, color_discrete_sequence=['#8B0000'])   ###plot it with plotly 
fig2 = px.treemap(df2, path=['type'], title='Treemap of Shows by Genre')


# **What type of content (Movies vs TV Shows) is more popular on the platform?*
df3=df['type'].value_counts().reset_index()                                                                  ###comparing between movies and Tv Shows
f3 = px.pie(df3, values='count', names='type', hole=.2, color_discrete_sequence=['#8B0000']  )               ###plot it with plotly


###distribution of Release year
df4 = df["release_year"].value_counts().reset_index().sort_values(by='release_year')          ###get release years
fig4 = px.line(df4, x="release_year", y=df4.columns[1:],color_discrete_sequence=['#8B0000'])  ###plot it with plotly


##what are the most ratings on Netflix?
df5 = df['rating'].value_counts().reset_index()                                                              ###Get the most rating      
fig5 = px.bar(df5, x="rating", y= 'count',color_discrete_sequence=['#8B0000'] )                              ###plot it with plotly



# **Tv shows in seasons**
df6 = df['Tv show'].value_counts().reset_index().sort_values(by='count' , ascending=False)    ###Get No. of seasons of Tv Shows
df6.drop(axis=0 , index=0 , inplace = True)                                                   ###drop the first row which has value of zero
fig6 = px.histogram(df6, x="Tv show", y= 'count',color_discrete_sequence=['#8B0000'] )              ###plot it with plotly


### movies in mins
df7= df['movies'].value_counts().reset_index().sort_values(by='movies' ,ascending=False)  ###Get No. of mins of movies
df7.drop(axis = 0 , index = 0 , inplace = True)                                           ###drop the first row which has value of zero
fig7 = px.histogram(df7, x="movies", y= 'count',color_discrete_sequence=['#8B0000'] )      ###plot it with plotly


# Streamlit Layout
st.title('Netflix')

# Display the sample data
st.header('Sample Data')
st.dataframe(df_sample, hide_index=True)

#Display visualization
st.header("Distribution of release years") 
st.plotly_chart(fig4)

# page content 
col1, col2, col3 = st.columns([5,5,5])

with col1:
        # Display visualizations
    st.header("what are the top five countries ?")
    st.plotly_chart(f1)
    
    # Display visualizations
    st.header("what are the top five genres of movies ?")
    st.plotly_chart(f2)
    

    # Display visualizations
    st.header("movies in mins")
    st.plotly_chart(fig7)


with col3:
       # Display visualizations
    st.header("which are the most movies or TV shows ?")
    st.plotly_chart(f3)
    
    # Display visualizations
    st.header("what are the most ratings on Netflix?")
    st.plotly_chart(fig5)
    
    # Display visualizations
    st.header("Tv-shows in seasons")
    st.plotly_chart(fig6)


st.header("Genres Map") 
st.plotly_chart(fig2)
