# Import modules
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

# Set titles 
st.markdown('# <font color="#ffc72c">Stephen Curry NBA Statistics</font>', unsafe_allow_html=True)
st.markdown('*Gia Khang Ngo - Manveer Buttar - Julian Alexis-Leon*')
st.markdown('## <font color="#006BB6">Introduction</font>', unsafe_allow_html=True)

# Set Introduction 
# set two columns to seperate the text and image while they are side by side
col1,col2, =st.columns(2)
with col2:
    st.image('https://i.pinimg.com/originals/82/9a/82/829a82bd6f39f7456c6f4cc2dacc27f6.jpg', width= 300)

with col1:
    st.markdown('''* A visual graphic of NBA player Stephen Curry's regular season statistics from 2009 to 2021.
    * **Data source:** [Kaggle.com](https://www.kaggle.com/datasets/mujinjo/stephen-curry-stats-20092021-in-nba).''')

    st.image('https://pbs.twimg.com/media/FVbqDw1WQAM6BmI?format=jpg&name=large', width= 350)

# Import and display raw data
curry_data = pd.read_csv('Stephen Curry Regularseason Stats.csv')
st.markdown('#### <font color = "#006BB6">Raw Data', unsafe_allow_html=True)
check_data = st.expander('Click to see raw data')
with check_data:
    st.dataframe(curry_data)

# Download Data Button
st.download_button(label= 'Download Raw Data', data=curry_data.to_csv().encode('utf-8'), file_name='Stephen Curry Regular Season Stats.csv', mime='text/csv')

#Sidebar
# Set Season Range and Team user input
st.sidebar.markdown('**<font color="#ffc72c">User Input Features</font>**',unsafe_allow_html=True)
st.sidebar.markdown("*Select the seasons you want to analyze:*")
season_year = st.sidebar.multiselect('Curry\'s Seasonal Year (Bar chart, Heat map)', curry_data['Season_year'].unique())
team_against = st.sidebar.multiselect('Opponent\'s (Pie chart)', curry_data['OPP'].unique())

# Show Curry gif
st.sidebar.markdown("![Alt Text](https://media.giphy.com/media/l41lVCaNfN7zjhFsc/giphy.gif)")

# Show current date and time
st.sidebar.markdown(f'*Date and time the server was run: {datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}*')

# Plot the histogram after finding the total 3-points shots attempted and made
st.markdown('## <font color = "#006BB6">3 Pointers Made and Attempted per Year', unsafe_allow_html=True)

if season_year:
    st.write('Hover over the graph to see success percentage.')
    list_year = []
    list_3PTA = []
    list_3PTM = []
    list_percent = []

    # Create lists of seasonal years, 3-point attempts, 3-point mades.
    for i_year in sorted(season_year):
        yA = curry_data[curry_data['Season_year'] == i_year]['3PTA'].sum()
        yM = curry_data[curry_data['Season_year'] == i_year]['3PTM'].sum()
        list_year.append(i_year)
        list_3PTA.append(yA)
        list_3PTM.append(yM)
        list_percent.append(f'Success rate: {yM/yA*100:.1f}%')
    
    # Plot histogram
    fig1 = go.Figure(data=[
        go.Bar(x=list_year, y=list_3PTM, name='3-point Shots Made',
        hovertext=list_percent, marker_color='rgb(253, 185, 39)'),
        go.Bar(x=list_year, y=list_3PTA, name='3-point Shots Attempted',
        hovertext=list_percent, marker_color='rgb(29, 66, 138)')
    ])
    
    fig1 = fig1.update_layout(
        title='Steph Curry 3-Point Shot Statistics',
        xaxis_title='Season year',
        yaxis_title='Number of 3-point Shots',
        width=800,
        height=600
    )
    st.plotly_chart(fig1)
    st.markdown('''- Steph Curry suffered from ankle injuries in the 2011-2012 season 
        and hand injuries in the 2019-2020, resulting in a visible dip in 3-point shots attempted and made.''')
    st.markdown('''- 2015-2016 was the season with the highest percentage of 3-point shots made in a match, 
        the same season when Steph Curry was voted as the unanimous MVP.''')
# Display error when no season year is inputed
else:
    st.error("Please select at least one season year in the sidebar.")

#Pie Chart of Win Rate relative to oppenent teams
st.markdown('## <font color = "#006BB6">Winning Chance Relative to Teams Played', unsafe_allow_html=True)
if team_against:
    team = []
    W_cnt =[]
    opp = curry_data.groupby('OPP')['Result'].sum()

    #loops through series and counts number of wins for each team and reassigns it to the series
    for team in opp.index:
         W_cnt = opp[team].count('W')
         opp[team] = W_cnt

    #plotting the pie chart based off the teams selected by the user
    opp = opp[team_against]    
    fig2 = px.pie(opp, values=opp.values, names=opp.index)
    fig2 = fig2.update_layout(
        title='**Steph Curry Win Chnace Relative to Teams Selected (2009-Present)**')
    st.plotly_chart(fig2)
    
    st.markdown('''- Steph Curry likely has a worse percentage against a team like the Boston Celtics
        as they have historically been a good team since Curry has joined the league.
        On the other hand a team like the Sacramento Kings has been the opposite so his percentage against them is higher.''')
# Display error when no team is selected
else:
    st.error("Please select at least one team in the sidebar.")

#Heat map for Curry's assists made for minutes played     
st.markdown('## <font color = "#006BB6">Assists made for Minutes Played', unsafe_allow_html=True)
if season_year:
    #Create empty lists for assists and minutes to add to
    list_AST = []
    list_MIN = []
    
    #loops through and adds the assists and minutes from the csv file for the years the user chooses
    for i_year in season_year:
        yAST = curry_data[curry_data['Season_year'] == i_year]['AST'].to_list()
        yMIN = curry_data[curry_data['Season_year'] == i_year]['MIN'].to_list()
        list_AST.extend(yAST)
        list_MIN.extend(yMIN)
        
    #creates graph in the form of a 2d histogram (AKA a heatmap), and changes size if each square on heatmap
    fig3 = go.Figure(data= 
        go.Histogram2d(x=list_MIN, y=list_AST,
        autobinx=False,
        xbins=dict(size=0.9),
        autobiny=False,
        ybins=dict(size=0.9)
        ))
    
    #adds title and axis names
    fig3 = fig3.update_layout(
        title='Steph Curry Assists per Minute Played',
        xaxis_title='Minutes',
        yaxis_title='Assists'
        )

    #plots graph
    st.plotly_chart(fig3)

    st.markdown('- The heatmap demonstates Steph Curry\'s average assists made for the amount of minutes played in a game.')
    st.markdown('- Stephen Curry normally averages 4-8 assists and 30-40 minutes played per game.')
 
# Display error when no season year is chosen
else:
    st.error("Please select at least one season year in the sidebar.")