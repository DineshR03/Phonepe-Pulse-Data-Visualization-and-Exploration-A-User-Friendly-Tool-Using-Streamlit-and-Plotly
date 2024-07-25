import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import time
from PIL import Image

# SQL Connection to python

import mysql.connector
from sqlalchemy import create_engine

mydb = mysql.connector.connect(host="localhost",user="root",password="")
mycursor = mydb.cursor(buffered=True,)

# creating database and using for table creation

mycursor.execute('create database if not exists phonepe')
mycursor.execute('use phonepe')

#creating SQLAlchemy engine to insert data_values

database_connection_string = "mysql+mysqlconnector://root:@localhost/phonepe"
engine = create_engine(database_connection_string) 


#set up page configuration for streamlit
icon = 'https://icons8.com/icon/OYtBxIlJwMGA/phone-pe'
st.set_page_config(
    page_title='PULSE',
    page_icon=icon,
    initial_sidebar_state='expanded',
    layout='wide',
    menu_items={"about": 'This Streamlit application was developed by Dinesh Babu R'}
)

title_text = '''<h1 style='font-size: 36px; color: #4B0082; text-align: center; font-family: Arial, sans-serif;'>Phonepe Pulse Data Visualization and Exploration</h1>'''
st.markdown(title_text, unsafe_allow_html=True)

#set up home page and option menu with side bar

with st.sidebar:
                
        selected = option_menu("Navigation",
                                options=["HOME", "GEO VISUALIZATION", "DATA VISUALIZATION"],
                                icons=["house", "globe", "lightbulb","info-circle"],
                                default_index=0,
                                orientation="vertical",
                                styles={"container": {"width": "100%", "border": "2px solid #000000", "background-color": "#127E40", "padding": "10px"},
                                        "icon": {"color": "#F8CD47", "font-size": "20px"},
                                        "option": {"color": "#FFFFFF", "font-size": "16px", "padding": "5px"}})


#setup the detail for the option 'HOME'
if selected =="HOME":
        col1,col2=st.columns(2)
        with col1:
                st.subheader(':violet[Phonepe]')
                st.markdown('''<h5>PhonePe is an extensively-used digital wallet in India, empowers users with an extensive suite of financial tools through its mobile app.<p>
                        <h5>PhonePe's popularity among millions of users underscores its role as a preferred choice in India's digital payments transformation.<h5>''',unsafe_allow_html=True)
                
                st.subheader(':violet[Phonepe Pulse]')
                st.markdown('''<h5>Phonepe Pulse is a platform that provides us with insights and trends related to their transactions and activities on the platform.
                            It offers data-driven analysis and visualizations, such as graphs and charts, to help us understand their spending patterns and other relevant information.<h5>''',unsafe_allow_html=True)
        with col2:
                image = Image.open("C:/Users/dines/Downloads/phonepe.jpg")
                st.image(image, caption='Phonepe Logo', use_column_width=True)


        col1,col2=st.columns(2)
        with col1:
                st.image('https://www.phonepe.com/pulsestatic/791/pulse/static/4cb2e7589c30e73dca3d569aea9ca280/1b2a8/pulse-2.webp',use_column_width=True)
        with col2:
                st.write(' ')
                st.subheader(':violet[Discover Insights:]')
                st.markdown('''
                        <h4>Transaction:<h5>Transaction insights involve analyzing customer transaction data to understand behavior and preferences.
                        By examining trends, categorizing transactions,and identifying patterns of india.
                        <h4>User: <h5>User insights refer to analyzing customer demographics, engagement metrics, and feedback.
                        By understanding demographics, tracking engagement of user in India ''',unsafe_allow_html=True)
                
                st.subheader(':violet[This Project is Inspired From Phonepe pulse site]')
                st.link_button('Orginal site','https://www.phonepe.com/pulse/')

        
#setup details for the option "Geo Visualization"
if selected =="GEO VISUALIZATION":
        
        def ind_geo():
                geo="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"                
                return geo
        
        geo_type = st.selectbox('**Data Category Selection**',["Transactions","Users"], index = None)
        st.write("You selected:", f"<span style='color:#F8CD47'>{geo_type}</span>", unsafe_allow_html=True)

        if geo_type=="Transactions":
                trans_geo_year_wise = st.toggle('Year-Wise')

                if not trans_geo_year_wise:
                        cat=st.radio('Category Selection',["Transaction Amount","Transaction Count"])
                        st.write("You selected:", f"<span style='color:#F8CD47'>{cat}</span>", unsafe_allow_html=True)

                        if cat =="Transaction Amount":
                                st.title(":violet[ Total Transaction Amount for States-Sum of all Year ]")

                                df = pd.read_sql_query('''SELECT state,sum(Transaction_amount) as 'Total Transaction Amount',
                                        AVG(Transaction_amount) as 'Average Transaction Amount'
                                        from agg_transaction
                                        GROUP by state''',con=engine)

                                fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                        locations='state',
                                        hover_data=['Total Transaction Amount','Average Transaction Amount'],
                                        color='Total Transaction Amount',
                                        color_continuous_scale='Magma',
                                        mapbox_style="carto-positron",zoom=3.5,
                                        center={"lat": 21.7679, "lon": 78.8718},)

                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(height=600)
                                st.plotly_chart(fig,use_container_width = True)

                        if cat =="Transaction Count":
                                st.title(":violet[Total Transaction Count for States-Sum of all Year]")

                                df = pd.read_sql_query('''SELECT state,sum(Transaction_count) as 'Total Transaction Count',
                                        AVG(Transaction_count) as 'Average Transaction Count'
                                        from agg_transaction
                                        GROUP by state''',con=engine)

                                fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                        locations='state',
                                        hover_data=['Total Transaction Count','Average Transaction Count'],
                                        color='Total Transaction Count',
                                        color_continuous_scale='Magma',
                                        mapbox_style="carto-positron",zoom=3.5,
                                        center={"lat": 21.7679, "lon": 78.8718},)

                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(height=600)
                                st.plotly_chart(fig,use_container_width = True)

                if trans_geo_year_wise:
                        df_year=pd.read_sql_query('''SELECT DISTINCT year as 'Year' from agg_transaction''',con=engine)
                        selected_year = st.selectbox("Select Year", options=df_year['Year'].tolist())
                        trans_geo_quater_wise = st.checkbox('Quarter-Wise')

                        if not trans_geo_quater_wise:
                                df = pd.read_sql_query('''SELECT state,sum(Transaction_amount) as 'Total Transaction Amount',
                                                AVG(Transaction_amount) as 'Average Transaction Amount',
                                                sum(Transaction_count) as 'Total Transaction Count',
                                                AVG(Transaction_count) as 'Average Transaction Count'
                                                from agg_transaction where year=%s
                                                GROUP by state''',con=engine,params=[(selected_year,)])
                        
                                fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                        locations='state',
                                        hover_data=['Total Transaction Amount','Average Transaction Amount','Total Transaction Count','Average Transaction Count'],
                                        color='Total Transaction Amount',
                                        color_continuous_scale=px.colors.sequential.Plasma,
                                        mapbox_style="carto-positron",zoom=3.5,
                                        center={"lat": 21.7679, "lon": 78.8718},)
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(height=600)
                                st.subheader(f":violet[Total Transaction Amount and Count for States in {selected_year}  ]")
                                st.plotly_chart(fig,use_container_width = True)

                        if trans_geo_quater_wise:
                                df_quater=pd.read_sql_query('''SELECT DISTINCT Quater as 'Quater' from agg_transaction''',con=engine)
                                selected_Quater = st.selectbox("Select Quater",options=df_quater['Quater'].tolist())

                                df = pd.read_sql_query('''SELECT state,sum(Transaction_amount) as 'Total Transaction Amount',
                                                AVG(Transaction_amount) as 'Average Transaction Amount',
                                                sum(Transaction_count) as 'Total Transaction Count',
                                                AVG(Transaction_count) as 'Average Transaction Count'
                                                from agg_transaction where year=%s and Quater=%s
                                                GROUP by state''',con=engine,params=(selected_year, selected_Quater))
                                
                                fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                        locations='state',
                                        hover_data=['Total Transaction Amount','Average Transaction Amount','Total Transaction Count','Average Transaction Count'],
                                        color='Total Transaction Amount',
                                        color_continuous_scale=px.colors.sequential.matter_r,
                                        mapbox_style="carto-positron",zoom=3.5,
                                        center={"lat": 21.7679, "lon": 78.8718},)
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(height=600)
                                st.subheader(f":violet[Total Transaction Amount and Count for States in {selected_year}-Q{selected_Quater}]")
                                st.plotly_chart(fig,use_container_width = True)

        if geo_type=="Users":
                user_geo_year_wise = st.toggle('Year-Wise')

                if not user_geo_year_wise:
                        st.title(":violet[ Total Register users Across States-Sum of all Year ]")

                        df = pd.read_sql_query('''SELECT DISTINCT state, SUM(Registered_Users) as 'Total Registered User',
                                        AVG(Registered_Users) as 'Average Register User'
                                        FROM map_user
                                        GROUP BY state''',con=engine)

                        fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                        locations='state',
                                        hover_data=['Total Registered User','Average Register User'],
                                        color='Total Registered User',
                                        color_continuous_scale='Magma',
                                        mapbox_style="carto-positron",zoom=3.5,
                                        center={"lat": 21.7679, "lon": 78.8718},)

                        fig.update_geos(fitbounds="locations", visible=False)
                        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                        fig.update_layout(height=600)
                        st.plotly_chart(fig,use_container_width = True)

                if user_geo_year_wise:
                        df_year=pd.read_sql_query('''SELECT DISTINCT year as 'Year' from map_user''',con=engine)
                        selected_year = st.selectbox("Select Year",options=df_year['Year'].tolist())
                        user_geo_quater_wise= st.toggle('Quater-Wise')

                        if not user_geo_quater_wise:
                                df = pd.read_sql_query('''SELECT DISTINCT state, SUM(Registered_Users) as 'Total Registered User',
                                                AVG(Registered_Users) as 'Average Register User'
                                                FROM map_user WHERE  year=%s
                                                GROUP BY state''',con=engine,params=[(selected_year,)])
                        
                                fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                                locations='state',
                                                hover_data=['Total Registered User','Average Register User'],
                                                color='Total Registered User',
                                                color_continuous_scale=px.colors.sequential.Plasma,
                                                mapbox_style="carto-positron",zoom=3.5,
                                                center={"lat": 21.7679, "lon": 78.8718},)
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(height=600)
                                st.subheader(f":violet[Total Registered User for States in {selected_year}  ]")
                                st.plotly_chart(fig,use_container_width = True)

                        if user_geo_quater_wise:
                                df_quater=pd.read_sql_query('''SELECT DISTINCT Quater as 'Quater' from map_user''',con=engine)
                                selected_Quater = st.selectbox("Select Quater",options=df_quater['Quater'].tolist())

                                df = pd.read_sql_query('''SELECT DISTINCT state, SUM(Registered_Users) as 'Total Registered User',
                                                AVG(Registered_Users) as 'Average Register User'
                                                FROM map_user WHERE  year=%s and Quater=%s
                                                GROUP BY state''',con=engine,params=(selected_year,selected_Quater))
                        
                                fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                                locations='state',
                                                hover_data=['Total Registered User','Average Register User'],
                                                color='Total Registered User',
                                                color_continuous_scale=px.colors.sequential.matter_r,
                                                mapbox_style="carto-positron",zoom=3.5,
                                                center={"lat": 21.7679, "lon": 78.8718},)
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(height=600)
                                st.subheader(f":violet[Total Registered User for States in {selected_year}-Q{selected_Quater} ]")
                                st.plotly_chart(fig,use_container_width = True)

#setup details for the option 'insights'
if selected =="DATA VISUALIZATION":
        select_insight=option_menu('',options=["INSIGHTS","CATEGORIES"],
                                        icons=["bar-chart","toggles","pie-chart"],
                                        orientation='horizontal',
                                        styles={"container":{"border": "2px ridge #000000"},
                                        icon: {"color": "#051C5F", "font-size": "20px"}})
                
        if select_insight =="INSIGHTS":
                qust=[  'Top 10 states with highest transaction',
                        'Top 10 states with lowest transaction',
                        'Top 10 states with highest Registered User',
                        'Top 10 District with highest transaction',
                        'Top 10 District with lowest transaction',
                        'Top 10 District with highest Registered User',
                        'Top 10 Brands used for Transaction',
                        'Sum of Transaction by categories',
                        'Top 10 Postal code with highest Transaction',
                        'Top 10 Postal code with highest Registered user'
                        ]
                query=st.selectbox(':red[Select Inquiry Topic]',options=qust,index=None)

                if query=='Top 10 states with highest transaction':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT state,sum(Transaction_amount) as 'Transaction Amount'
                                        from agg_transaction
                                        GROUP by state
                                        ORDER by sum(Transaction_amount) DESC LIMIT 10;''',con=engine)
                                
                                fig=px.bar(df,x='state',y='Transaction Amount',
                                                color='state',
                                                hover_data=['Transaction Amount'],
                                                title='Top 10 state of Highest Transaction Amount',
                                                color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                                                        
                        with col2:
                                df=pd.read_sql_query('''SELECT state, SUM(Transaction_count) AS 'Transaction Count' FROM agg_transaction
                                                WHERE state IN ( SELECT state FROM 
                                                (SELECT state, SUM(Transaction_amount) AS amount FROM agg_transaction 
                                                GROUP BY state ORDER BY amount DESC LIMIT 10 )as top_state )
                                                GROUP BY state order by sum(Transaction_count) DESC''',con=engine)
                                
                                fig=px.bar(df,x='state',y='Transaction Count',
                                                color='state',
                                                hover_data=['Transaction Count'],
                                                title='Transaction Count',
                                                color_continuous_scale=px.colors.sequential.Viridis)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                                
                        st.write("Key Insights:")
                        
                        st.write("- Telangana has experienced substantial growth in technology and IT sectors, particularly in cities like Hyderabad. This expansion likely contributed to an uptick in digital transactions facilitated by platforms like PhonePe.")

                        st.write("- Maharashtra, housing Mumbai as India's financial hub, boasts a varied economy spanning finance, manufacturing, and services. Its high level of urbanization and economic activity are major factors driving substantial transaction volumes.")

                        st.write("- Karnataka, with Bengaluru as a prominent technology and innovation center, hosts numerous IT firms and startups, which likely generate a significant volume of digital transactions.")
                
                        
                if query=='Top 10 states with lowest transaction':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT state,sum(Transaction_amount) as 'Transaction Amount'
                                        from agg_transaction GROUP by state
                                        ORDER by sum(Transaction_amount) ASC LIMIT 10''',con=engine)
                                df['state']=df['state'].str.replace('Dadra and Nagar Haveli and Daman and Diu','Dadra')

                                fig=px.bar(df,x='state',y='Transaction Amount',
                                                color='state',
                                                hover_data=['Transaction Amount'],
                                                title='Top 10 state of lowest Transaction Amount',
                                                color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)

                        with col2:
                                df=pd.read_sql_query('''SELECT state, SUM(Transaction_count) AS 'Transaction Count' FROM agg_transaction
                                                WHERE state IN ( SELECT state FROM 
                                                (SELECT state, SUM(Transaction_amount) AS amount FROM agg_transaction 
                                                GROUP BY state ORDER BY amount ASC LIMIT 10 )as top_state )
                                                GROUP BY state order by sum(Transaction_count) ASC''',con=engine)
                                df['state']=df['state'].str.replace('Dadra and Nagar Haveli and Daman and Diu','Dadra')
                                
                                fig=px.bar(df,x='state',y='Transaction Count',
                                                color='state',
                                                hover_data=['Transaction Count'],
                                                title='Top 10 state of lowest Transaction Count',
                                                color_continuous_scale=px.colors.sequential.Viridis)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                        
                        st.write("Key Insights:")
                        
                        st.write("- Lakshadweep, with its limited population and remote island setting, faces challenges in accessing digital infrastructure and financial services.")

                        st.write("- Mizoram encounters difficulties due to its sparse population and rugged terrain, which hinder the development of digital infrastructure and connectivity. Limited economic diversity and lower urbanization rates may also contribute to reduced transaction volumes.")

                        st.write("- The Andaman & Nicobar Islands grapple with geographical limitations and a relatively small population, which restricts access to digital services. Despite a thriving tourism sector, seasonal fluctuations and reliance on cash payments may impede the growth of digital transactions.")

                        st.write("- States like Ladakh, Sikkim, Nagaland, Meghalaya, Dadra & Nagar Haveli, Tripura, and Manipur experience lower transaction volumes due to a blend of factors. These regions often contend with rugged terrain, dispersed population centers, limited economic diversity, and cultural preferences favoring cash transactions.")
                        
                if query=='Top 10 states with highest Registered User':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT state ,sum(Registered_Users) as 'Registered User' FROM map_user 
                                                GROUP BY state ORDER BY sum(Registered_Users) DESC limit 10''',con=engine)
                                
                                fig=px.bar(df,x='state',y='Registered User',
                                                color='state',
                                                hover_data=['Registered User'],
                                                title='Top 10 state of highest Registered User',
                                                color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                        
                        with col2:
                                df=pd.read_sql_query('''SELECT state, SUM(App_Opens) AS 'App Opened' FROM map_user WHERE state IN 
                                                (SELECT state  FROM (SELECT state, SUM(Registered_Users) AS 'R_user'
                                                FROM map_user GROUP BY state ORDER BY sum(Registered_Users) DESC LIMIT 10)as top_user )
                                                GROUP BY state ORDER BY sum(App_Opens) DESC''',con=engine)
                                
                                fig=px.bar(df,x='state',y='App Opened',
                                                color='App Opened',
                                                hover_data=['App Opened'],
                                                title='App Opened',
                                                color_continuous_scale=px.colors.carto.Pastel_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                                
                        st.write("Key Insights:")
                        
                        st.write("- Maharashtra leads with the highest number of PhonePe registered users, indicating robust adoption of digital payment platforms in both urban and rural areas of the state.")

                        st.write("- Uttar Pradesh, Karnataka, and Andhra Pradesh closely follow, demonstrating substantial PhonePe user registrations and widespread acceptance of digital transactions in these densely populated states.")

                        st.write("- Rajasthan, Telangana, and West Bengal show significant PhonePe user bases, reflecting increasing digital adoption in regional economic hubs and urban clusters.")

                        st.write("- Tamil Nadu, Madhya Pradesh, and Gujarat contribute significantly to the overall PhonePe user base, showcasing diverse digital landscapes and the growing popularity of digital payment solutions across various regions of India.")
               
                if query=='Top 10 District with highest transaction':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT District,sum(Transaction_amount) as 'Transaction Amount'
                                        from map_transaction GROUP by District
                                        ORDER by sum(Transaction_amount) DESC LIMIT 10;''',con=engine)
                                df['District']=df['District'].str.replace('Central','Delhi Central')
                                
                                fig=px.bar(df,x='District',y='Transaction Amount',
                                                color='District',
                                                hover_data=['Transaction Amount'],
                                                title='Top 10 District of Highest Transaction Amount',
                                                color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                        
                        with col2:
                                df=pd.read_sql_query('''SELECT District, SUM(Transaction_count) AS 'Transaction Count' FROM map_transaction 
                                        WHERE District IN (SELECT District  FROM (SELECT District, SUM(Transaction_amount) AS 'amount' 
                                        FROM map_transaction GROUP BY District ORDER BY amount DESC LIMIT 10)as top_dist )
                                        GROUP BY District ORDER BY SUM(Transaction_count) DESC;''',con=engine)
                                df['District']=df['District'].str.replace('Central','Delhi Central')

                                fig=px.bar(df,x='District',y='Transaction Count',
                                                color='Transaction Count',
                                                hover_data=['Transaction Count'],
                                                title='Transaction Count',
                                                color_continuous_scale=px.colors.carto.Prism_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                        
                        st.write("Key Insights:")
                                
                        st.write("- Bengaluru, Hyderabad, and Pune are prominent centers for PhonePe transactions, driven by their leadership in IT and business sectors and high smartphone penetration.")

                        st.write("- Jaipur and Visakhapatnam lead PhonePe transactions in their respective regions, benefiting from a blend of traditional commerce and growing tech industries.")

                        st.write("- Rangareddy and Medchal Malkajgiri, integral parts of Hyderabad's metropolitan area, show significant volumes in PhonePe transactions, highlighting the increasing acceptance of digital payments in urban settings.")

                        st.write("- Patna, Krishna, and Delhi Central demonstrate substantial PhonePe transactions due to their administrative importance, strategic locations, and vibrant commercial environments, indicating widespread adoption of digital payment platforms.")        
                        
                if query=='Top 10 District with lowest transaction':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT District,sum(Transaction_amount) as 'Transaction Amount'
                                        from map_transaction GROUP by District
                                        ORDER by sum(Transaction_amount) ASC LIMIT 10;''',con=engine)
                                
                                fig=px.bar(df,x='District',y='Transaction Amount',
                                                color='District',
                                                hover_data=['Transaction Amount'],
                                                title='Top 10 District of Lowest Transaction Amount',
                                                color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                        
                        with col2:
                                df=pd.read_sql_query('''SELECT District, SUM(Transaction_count) AS 'Transaction Count' FROM map_transaction 
                                        WHERE District IN (SELECT District  FROM (SELECT District, SUM(Transaction_amount) AS 'amount' 
                                        FROM map_transaction GROUP BY District ORDER BY amount ASC LIMIT 10)as top_dist )
                                        GROUP BY District ORDER BY SUM(Transaction_count) ASC;''',con=engine)

                                fig=px.bar(df,x='District',y='Transaction Count',
                                                color='Transaction Count',
                                                hover_data=['Transaction Count'],
                                                title='Transaction Count',
                                                color_continuous_scale=px.colors.carto.Prism_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                                
                        st.write("Key Insights:")

                        st.write("- Rural districts like Pherzawl and Dibang Valley experience fewer transactions due to limited access to digital infrastructure and financial services.")

                        st.write("- Regions such as Pakke Kessang and Kurung Kumey see lower transaction volumes because of their sparse population densities, resulting in fewer digital transactions compared to more densely populated areas.")

                        st.write("- Districts like Muzaffarabad and Longleng encounter challenges such as poor internet connectivity, which hinder the adoption of digital payments.")

                        st.write("- Economic and cultural factors, including preferences for cash transactions, contribute to lower adoption rates of digital payments in these regions.")

                if query=='Top 10 Brands used for Transaction':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT DISTINCT User_brand as 'User Brand' ,SUM(User_count) as 'Count'
                                                FROM agg_user GROUP BY User_brand
                                                order by SUM(User_count) DESC LIMIT 10''',con=engine)
                                
                                fig=px.bar(df,x='User Brand',y='Count',
                                                color='User Brand',
                                                hover_data=['Count'],
                                                title='Top 10 Brands used for Transaction (sum of all states)',
                                                color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                        
                        with col2:
                                df=pd.read_sql_query('''SELECT User_brand AS 'User Brand', (SUM(User_count) / total_count) * 100 AS 'Percentage'
                                                FROM agg_user
                                                CROSS JOIN (SELECT SUM(User_count) AS total_count FROM agg_user) AS total
                                                GROUP BY User_brand
                                                ORDER BY SUM(User_count) DESC LIMIT 10;''',con=engine)
                                
                                fig=px.pie(df,names='User Brand',values='Percentage',color='User Brand',
                                                title='Percentage',
                                                color_discrete_sequence=px.colors.qualitative.Bold)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                                
                        st.write("Key Insights:")
                        
                        st.write("- Xiaomi, Samsung, Vivo, and Oppo dominate the market due to their extensive product range and strong brand recognition. Their affordability, innovation, focus on camera technology, and stylish designs collectively drive consumer purchases.")

                        st.write("- Realme, Motorola, and OnePlus are gaining market share with competitive pricing and innovative features. Realme's rapid growth, Motorola's reliability, and OnePlus's flagship-level features appeal to budget-conscious and tech-savvy consumers.")

                        st.write("- Apple and Huawei sustain their market positions through premium branding and advanced technology. Their aspirational value, loyal customer base, and reputation for innovation drive transactions in the premium smartphone segment.")

                        st.write("- Other brands cater to niche segments by offering budget-friendly options and diversifying the market. These brands contribute to overall transaction volumes by providing alternative choices for consumers.")
                                       
                        
                if query=='Top 10 District with highest Registered User':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT District, sum(Registered_Users) as 'Registered User' FROM map_user
                                        GROUP BY District ORDER BY sum(Registered_Users) DESC LIMIT 10''',con=engine)
                                
                                fig=px.bar(df,x='District',y='Registered User',
                                                color='District',
                                                hover_data=['Registered User'],
                                                title='Top 10 District of highest Registered User ',
                                                color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)

                        with col2:
                                df=pd.read_sql_query('''SELECT District, SUM(App_Opens) AS 'App Opened' FROM map_user WHERE District IN 
                                                (SELECT District  FROM (SELECT District, SUM(Registered_Users) AS 'R_user'
                                                FROM map_user GROUP BY District ORDER BY sum(Registered_Users) DESC LIMIT 10)as top_user )
                                                GROUP BY District ORDER BY sum(App_Opens) DESC''',con=engine)
                                
                                fig=px.bar(df,x='District',y='App Opened',
                                                color='App Opened',
                                                hover_data=['App Opened'],
                                                title='App Opened',
                                                color_continuous_scale=px.colors.carto.Prism_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                                
                        st.write("Key Insights:")
                        
                        st.write("- Bengaluru Urban leads with the highest number of registered PhonePe users, indicating widespread adoption of digital payment platforms in Karnataka's capital city and its surrounding urban areas.")

                        st.write("- Pune and Jaipur secure the second and third positions, respectively, in terms of PhonePe registrations, highlighting significant digital adoption in urban centers of Maharashtra and Rajasthan.")

                        st.write("- Districts like Thane, Mumbai Suburban, and Hyderabad show substantial PhonePe user bases, reflecting strong urban presence and increasing preference for digital payment solutions in metropolitan areas.")

                        st.write("- Ahmedabad, Rangareddy, and Surat districts represent diverse regions and make notable contributions to PhonePe registrations, showcasing a trend of widespread adoption extending beyond metropolitan areas.")
        
                        
                if query=='Sum of Transaction by categories':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT DISTINCT Transaction_type as 'categories',SUM(Transaction_amount) as 'Transaction Amount'
                                                        from agg_transaction GROUP BY Transaction_type ORDER BY SUM(Transaction_amount) DESC''',con=engine)
                                
                                fig=px.pie(df,names='categories',values='Transaction Amount',color='categories',
                                                title='Sum of Transaction Amount by categories',hole=0.3,
                                                color_discrete_sequence=px.colors.qualitative.Bold)
                                st.plotly_chart(fig,use_container_width=True)
                        
                        with col2:
                                st.subheader('Sum of Transaction Amount')
                                st.dataframe(df,hide_index=True)
                                
                        st.write("Key Insights:")
                        
                        st.write("- Peer-to-peer payments lead as the largest category, with a significant transaction amount of 169.78 trillion. This indicates a substantial volume of person-to-person financial transactions during the observed period.")

                        st.write("- Merchant payments (37.36 trillion) and recharge/bill payments (8.53 trillion) represent substantial commercial and essential service transactions.")

                        st.write("- Financial services transactions, though smaller at 80.10 billion, underscore the importance of banking and investment activities.")

                        st.write("- The category labeled as 'Others' (141.85 billion) indicates diverse financial activities beyond the specified categories.")        
                        
                if query=='Top 10 Postal code with highest Transaction':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT Pincode, sum(Transaction_amount) as 'Transaction Amount' FROM top_transaction
                                                GROUP BY Pincode ORDER BY sum(Transaction_amount) DESC LIMIT 10''',con=engine)
                                
                                fig=px.pie(df,names='Pincode',values='Transaction Amount',
                                                color="Pincode",
                                                title='Top 10 Postal code of highest Transaction Amount ',
                                                color_discrete_sequence=px.colors.qualitative.Pastel_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)

                        with col2:
                                df=pd.read_sql_query('''SELECT Pincode , SUM(Transaction_count) AS 'Transaction Count' FROM top_transaction
                                                WHERE Pincode IN (SELECT Pincode FROM (SELECT Pincode, SUM(Transaction_amount) AS 't_amt' 
                                                FROM top_transaction GROUP BY Pincode ORDER BY SUM(Transaction_amount) DESC LIMIT 10)as top_tran ) 
                                                GROUP BY Pincode ORDER BY SUM(Transaction_count) DESC;''',con=engine)
                                
                                fig=px.pie(df,names='Pincode',values='Transaction Count',
                                                color='Transaction Count',
                                                title='Transaction Count',
                                                color_discrete_sequence=px.colors.qualitative.Dark2_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                                
                        st.write("Key Insights:")
                        
                                

                if query=='Top 10 Postal code with highest Registered user':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT Pincode, sum(Registered_Users) as 'Registered user' FROM top_user
                                                GROUP BY Pincode ORDER BY  sum(Registered_Users) DESC LIMIT 10''',con=engine)
                                
                                fig=px.pie(df,names='Pincode',values='Registered user',
                                                color="Pincode",
                                                title='Top 10 Postal code with highest Registered user ',
                                                color_discrete_sequence=px.colors.qualitative.Vivid_r)
                                st.plotly_chart(fig,use_container_width=True)

                        with col2:
                                st.write('Top 10 Postal code with highest Registered user')
                                st.dataframe(df,hide_index=True)
                                       

        if select_insight =="CATEGORIES":
                fil_type=st.radio('Category Selection',["**State**","**District**"], index = None)
                st.write("You selected:", f"<span style='color:#F8CD47'>{fil_type}</span>", unsafe_allow_html=True)

                if fil_type=="**State**":
                        ques=['Year and Quater wise Transaction Amount of all states',
                                'Quater wise Transaction Amount for specific state',
                                'Transaction Category with specific state and year',
                                'Quater wise Transaction Amount for specific state and type',
                                'User Brand Count for selected state and year']
                        Query=st.selectbox(':red[select Query]',options=ques,index=None)
                        
                        if Query==ques[0]:
                                df_year=pd.read_sql_query('''SELECT DISTINCT year as 'Year' from agg_transaction''',con=engine)
                                select_year = st.selectbox("Select Year",options=df_year['Year'].tolist(),index=None)

                                df_quater=pd.read_sql_query('''SELECT DISTINCT Quater as 'Quater' from agg_transaction''',con=engine)
                                select_Quater = st.selectbox("Select Quater",options=df_quater['Quater'].tolist(),index=None)
                                bt=st.button('Show')
                                if bt:
                                        df=pd.read_sql_query('''SELECT state, SUM(Transaction_amount) as 'Transaction Amount'
                                        FROM agg_transaction where year = %s and Quater = %s
                                        GROUP BY state''',con=engine,params=[(select_year,select_Quater)])

                                        fig=px.scatter(df,x='state',y='Transaction Amount',
                                                        title=f'Showing Transaction Amount of {select_year}-Q{select_Quater}')
                                        st.plotly_chart(fig,use_container_width=True)

                                        df1=pd.read_sql_query('''SELECT state, SUM(Transaction_count) as 'Transaction Count'
                                        FROM agg_transaction where year = %s and Quater = %s
                                        GROUP BY state''',con=engine,params=[(select_year,select_Quater)])

                                        fig=px.scatter(df1,x='state',y='Transaction Count',
                                                        title=f'Showing Transaction Count of {select_year}-Q{select_Quater}')
                                        st.plotly_chart(fig,use_container_width=True)

                                        col1,col2=st.columns(2)
                                        with col1:
                                                st.dataframe(df,hide_index=True)
                                        with col2:
                                                st.dataframe(df1,hide_index=True)

                        if Query==ques[1]:
                                df_state=pd.read_sql_query('''Select DISTINCT state from agg_transaction''',con=engine)
                                select_state=st.selectbox('Select state',options=df_state['state'].tolist(),index=None)

                                df_year=pd.read_sql_query('''SELECT DISTINCT year as 'Year' from agg_transaction''',con=engine)
                                select_year = st.selectbox("Select Year",options=df_year['Year'].tolist(),index=None)
                                bt=st.button('Show')
                                if bt:
                                        col1,col2=st.columns(2)
                                        with col1:
                                                df=pd.read_sql_query(''' SELECT Quater,sum(Transaction_amount) as 'Transaction Amount'
                                                                from agg_transaction WHERE state=%s and year=%s
                                                                GROUP by Quater;''',con=engine,params=[(select_state,select_year)])
                                                
                                                fig=px.bar(df,x='Quater',y='Transaction Amount',
                                                        color='Transaction Amount',hover_data=['Transaction Amount'],
                                                        title=f'Quater wise Transaction Amount of {select_state} for the year:{select_year}',
                                                        color_continuous_scale=px.colors.sequential.Viridis     )
                                                st.plotly_chart(fig,use_container_width=True)
                                                st.dataframe(df,hide_index=True)
                                        
                                        with col2:
                                                df=pd.read_sql_query(''' SELECT Quater,sum(Transaction_count) as 'Transaction Count'
                                                                from agg_transaction WHERE state=%s and year=%s
                                                                GROUP by Quater;''',con=engine,params=[(select_state,select_year)])
                                                
                                                fig=px.bar(df,x='Quater',y='Transaction Count',
                                                        color='Transaction Count',hover_data=['Transaction Count'],
                                                        title=f'Quater wise Transaction Count of {select_state} for the year: {select_year}',
                                                        color_continuous_scale=px.colors.sequential.Plasma)
                                                st.plotly_chart(fig,use_container_width=True)
                                                st.dataframe(df,hide_index=True)
                        
                        if Query==ques[2]:
                                df_state=pd.read_sql_query('''Select DISTINCT state from agg_transaction''',con=engine)
                                select_state=st.selectbox('Select state',options=df_state['state'].tolist(),index=None)

                                df_year=pd.read_sql_query('''SELECT DISTINCT year as 'Year' from agg_transaction''',con=engine)
                                select_year = st.selectbox("Select Year",options=df_year['Year'].tolist(),index=None)
                                bt=st.button('Show')
                                if bt:
                                        col1,col2=st.columns(2)
                                        with col1:
                                                df=pd.read_sql_query(''' SELECT Transaction_type as 'category',sum(Transaction_amount) as 'Transaction Amount'
                                                                from agg_transaction WHERE state=%s and year=%s
                                                                GROUP BY Transaction_type''',con=engine,params=[(select_state,select_year)])
                                                
                                                fig=px.bar(df,x='category',y='Transaction Amount',
                                                        color='Transaction Amount',hover_data=['Transaction Amount'],
                                                        title=f'Categories of Transaction Amount of {select_state} for the year:{select_year}',
                                                        color_continuous_scale=px.colors.sequential.Magenta)
                                                st.plotly_chart(fig,use_container_width=True)
                                                st.dataframe(df,hide_index=True)

                                        with col2:
                                                df=pd.read_sql_query(''' SELECT Transaction_type as 'category',sum(Transaction_count) as 'Transaction Count'
                                                                from agg_transaction WHERE state=%s and year=%s
                                                                GROUP BY Transaction_type''',con=engine,params=[(select_state,select_year)])
                                                
                                                fig=px.bar(df,x='category',y='Transaction Count',
                                                        color='Transaction Count',hover_data=['Transaction Count'],
                                                        title=f'Categories of Transaction Count of {select_state} for the year:{select_year}',
                                                        color_continuous_scale=px.colors.sequential.Plasma_r)
                                                st.plotly_chart(fig,use_container_width=True)
                                                st.dataframe(df,hide_index=True)
                        
                        if Query==ques[3]:
                                df_state=pd.read_sql_query('''Select DISTINCT state from agg_transaction''',con=engine)
                                select_state=st.selectbox('Select state',options=df_state['state'].tolist(),index=None)

                                df_type=pd.read_sql_query('''SELECT DISTINCT Transaction_type as 'Type' from agg_transaction''',con=engine)
                                select_type=st.selectbox('Select Type',options=df_type['Type'].tolist(),index=None)
                                bt=st.button('Show')
                                if bt:
                                        col1,col2=st.columns(2)
                                        with col1:
                                                df=pd.read_sql_query('''SELECT state,Quater,sum(Transaction_amount) as 'Transaction Amount' from agg_transaction 
                                                                where state =%s and Transaction_type=%s group by state,Quater''',con=engine,params=[(select_state,select_type)])
                                                
                                                fig=px.bar(df,x='Quater',y='Transaction Amount',
                                                                        color='Transaction Amount',hover_data=['Transaction Amount'],
                                                                        title=f'showing quater wise Amount of {select_state} for type:{select_type}',
                                                                        color_continuous_scale=px.colors.sequential.Magma)
                                                st.plotly_chart(fig,use_container_width=True)
                                                st.dataframe(df,hide_index=True)
                                        
                                        with col2:
                                                df=pd.read_sql_query('''SELECT state,Quater,sum(Transaction_count) as 'Transaction Count' from agg_transaction 
                                                                where state =%s and Transaction_type=%s group by state,Quater''',con=engine,params=[(select_state,select_type)])
                                                
                                                fig=px.bar(df,x='Quater',y='Transaction Count',
                                                                        color='Transaction Count',hover_data=['Transaction Count'],
                                                                        title=f'showing quater wise Count of {select_state} for type:{select_type}',
                                                                        color_continuous_scale=px.colors.sequential.Plasma)
                                                st.plotly_chart(fig,use_container_width=True)
                                                st.dataframe(df,hide_index=True)

                        if Query==ques[4]:
                                df_state=pd.read_sql_query('''Select DISTINCT state from agg_user''',con=engine)
                                select_state=st.selectbox('Select state',options=df_state['state'].tolist(),index=None)

                                df_year=pd.read_sql_query('''SELECT DISTINCT year as 'Year' from agg_user''',con=engine)
                                select_year = st.selectbox("Select Year",options=df_year['Year'].tolist(),index=None)
                                bt=st.button('Show')
                                if bt:
                                        col1,col2=st.columns(2)
                                        with col1:
                                                df=pd.read_sql_query('''SELECT User_brand as 'User Brand',sum(User_count) as 'Count' from agg_user
                                                        WHERE state=%s and year=%s
                                                        GROUP by User_brand order by sum(User_count) DESC''',con=engine,params=[(select_state,select_year)])
                                                
                                                fig=px.bar(df,x='User Brand',y='Count',
                                                        color='Count',hover_data=['Count'],
                                                        title=f'Showing User Brand Count of {select_state} for the year:{select_year}',
                                                        color_continuous_scale=px.colors.sequential.Plasma)
                                                st.plotly_chart(fig,use_container_width=True)
                                                st.dataframe(df,hide_index=True)

                                        with col2:
                                                fig=px.pie(df,names='User Brand',values='Count',
                                                        color='User Brand',title='Count Percentage',
                                                        color_discrete_sequence=px.colors.sequential.Magma)
                                                st.plotly_chart(fig,use_container_width=True)

                
                if fil_type=="**District**":
                        ques=['District wise Transaction Amount for selected state & year',
                                'Year wise Transaction Amount for specific District',
                                'Year wise Registered User Count for Specific District']
                        Query=st.selectbox(':red[select Query]',options=ques,index=None)

                        if Query==ques[0]:
                                df_state=pd.read_sql_query('''SELECT DISTINCT state from map_transaction''',con=engine)
                                select_state=st.selectbox('Select state',options=df_state['state'].tolist(),index=None)

                                df_year=pd.read_sql_query('''SELECT DISTINCT year from map_transaction''',con=engine)
                                select_year = st.selectbox("Select Year",options=df_year['year'].tolist(),index=None)
                                bt=st.button('Show')
                                if bt:
                                        df=pd.read_sql_query('''SELECT District, SUM(Transaction_amount) as 'Transaction Amount'
                                        FROM map_transaction where state=%s and  year =%s
                                        GROUP BY District''',con=engine,params=[(select_state,select_year)])

                                        fig=px.bar(df,x='District',y='Transaction Amount',
                                                        color='Transaction Amount',hover_data=['Transaction Amount'],
                                                        title=f'District wise Transaction Amount of {select_state} for the year:{select_year}',
                                                        color_continuous_scale = 'Viridis')
                                        st.plotly_chart(fig,use_container_width=True)

                                        df1=pd.read_sql_query('''SELECT District, SUM(Transaction_count) as 'Transaction count'
                                        FROM map_transaction where state=%s and  year =%s
                                        GROUP BY District''',con=engine,params=[(select_state,select_year)])

                                        fig=px.bar(df1,x='District',y='Transaction count',
                                                        color='Transaction count',hover_data=['Transaction count'],
                                                        title=f'District wise Transaction count of {select_state} for the year:{select_year}',
                                                        color_continuous_scale = 'Plasma')
                                        st.plotly_chart(fig,use_container_width=True)

                                        col1,col2=st.columns(2)
                                        with col1:
                                                st.dataframe(df,hide_index=True)
                                        with col2:
                                                st.dataframe(df1,hide_index=True)
                        
                        if Query==ques[1]:
                                df_state=pd.read_sql_query('''SELECT DISTINCT state from map_transaction''',con=engine)
                                select_state=st.selectbox('Select state',options=df_state['state'].tolist(),index=None)

                                df_dist=pd.read_sql_query('''SELECT DISTINCT District FROM map_transaction 
                                                        where state=%s''',con=engine,params=[(select_state,)])
                                select_dist=st.selectbox('Select District',options=df_dist['District'].tolist(),index=None)
                                bt=st.button('Show')
                                if bt:
                                        col1,col2=st.columns(2)
                                        with col1:
                                                df=pd.read_sql_query('''SELECT year,sum(Transaction_amount) as 'Transaction Amount' from map_transaction
                                                        where state=%s and District= %s
                                                        GROUP by year''',con=engine,params=[(select_state,select_dist)])
                                                
                                                fig=px.bar(df,x='year',y='Transaction Amount',
                                                        color='Transaction Amount',hover_data=['Transaction Amount'],
                                                        title=f'Year wise Transaction Amount of {select_dist} District',
                                                        color_continuous_scale = "Viridis")
                                                st.plotly_chart(fig,use_container_width=True)
                                                st.dataframe(df,hide_index=True)

                                        with col2:
                                                df=pd.read_sql_query('''SELECT year,sum(Transaction_count) as 'Transaction count' from map_transaction
                                                        where state=%s and District= %s
                                                        GROUP by year''',con=engine,params=[(select_state,select_dist)])
                                                
                                                fig=px.bar(df,x='year',y='Transaction count',
                                                        color='Transaction count',hover_data=['Transaction count'],
                                                        title=f'Year wise Transaction count of {select_dist} District',
                                                        color_continuous_scale = "Plasma")
                                                st.plotly_chart(fig,use_container_width=True)
                                                st.dataframe(df,hide_index=True)

                        if Query==ques[2]:
                                df_state=pd.read_sql_query('''SELECT DISTINCT state from map_transaction''',con=engine)
                                select_state=st.selectbox('Select state',options=df_state['state'].tolist(),index=None)

                                df_dist=pd.read_sql_query('''SELECT DISTINCT District FROM map_transaction 
                                                        where state=%s''',con=engine,params=[(select_state,)])
                                select_dist=st.selectbox('Select District',options=df_dist['District'].tolist(),index=None)
                                bt=st.button('Show')
                                if bt:
                                        df=pd.read_sql_query('''SELECT year,sum(Registered_Users) as 'Registered User' from map_user
                                                where state=%s and District= %s
                                                GROUP by year''',con=engine,params=[(select_state,select_dist)])
                                        
                                        fig=px.bar(df,x='year',y='Registered User',
                                                color='Registered User',hover_data=['Registered User'],
                                                title=f'Year wise Registered User of {select_dist} District',
                                                color_continuous_scale = "Plasma")
                                        st.plotly_chart(fig,use_container_width=True)
                                        st.dataframe(df,hide_index=True)

                        