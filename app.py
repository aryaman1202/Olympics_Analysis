import streamlit as st
import pandas as pd
import preprocessor
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image("https://1000logos.net/wp-content/uploads/2017/05/Olympics-Logo-1986.png")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis',
     'Country-Wise Analysis', 'Athlete-Wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = preprocessor.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally = preprocessor.fetch_medal_tally(
        df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in '+str(selected_year)+' Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title('Overall performance of '+selected_country+' in Olympics')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country+' performance in ' +
                 str(selected_year)+' Olympics')

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    no_of_editions = df['Year'].unique().shape[0]-1
    no_of_cities = df['City'].unique().shape[0]
    no_of_sports = df['Sport'].unique().shape[0]
    no_of_events = df['Event'].unique().shape[0]
    no_of_participated_athletes = df['Name'].unique().shape[0]
    no_of_nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(no_of_editions)
    with col2:
        st.header('Hosts')
        st.title(no_of_cities)
    with col3:
        st.header('Sports')
        st.title(no_of_sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(no_of_events)
    with col2:
        st.header('Nations')
        st.title(no_of_nations)
    with col3:
        st.header('Athletes')
        st.title(no_of_participated_athletes)

    nations_over_time = preprocessor.data_over_time(df, 'region')
    st.title("Participating Nations over Olympic Editions")
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.plotly_chart(fig)

    events_over_time = preprocessor.data_over_time(df, 'Event')
    st.title("Events over Olympic Editions")
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.plotly_chart(fig)

    athletes_over_time = preprocessor.data_over_time(df, 'Name')
    st.title("No of Atheletes over Olympic Editions")
    fig = px.line(athletes_over_time, x='Edition', y='Name')
    st.plotly_chart(fig)

    st.title("No of Events over Time w.r.t. Sport")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)

    x = preprocessor.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-Wise Analysis':
    st.title("Country Wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.selectbox('Select a Country',country_list)


    st.title("Medals vs Time for countries")
    country_df = preprocessor.year_wise_medaltally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.plotly_chart(fig)


    st.title("Sports in which "+selected_country+' Excel')
    pt = preprocessor.country_event_heatmap(df,selected_country)
    fig,ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)


    st.title("Top 10 Athletes of "+selected_country)
    top10_df = preprocessor.most_successful_athletes(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete-Wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age of Athletes")
    st.plotly_chart(fig)


    st.title("Weight vs Height Analysis of Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport',sport_list)
    temp_df = preprocessor.weight_vs_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'])
    st.pyplot(fig)

    
    st.title("Men vs Women Participation in Olympics")
    final = preprocessor.men_vs_women(df)
    fig = px.line(final,x="Year",y=["Male","Female"])
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)
