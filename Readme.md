# PhonePe Pulse Data Visualization Tool

## Overview

This project utilizes the PhonePe Pulse dataset to create an interactive data exploration tool. It includes data extraction from GitHub, transformation into Pandas dataframes, storage in MySQL via SQLAlchemy, and visualization through Streamlit and Plotly.

### Domain: Fintech

### Technologies Used

- Python 3.12.2
- XAMPP (MySQL)
- Streamlit
- Plotly

### Key Libraries

- pandas
- plotly.express
- streamlit
- mysql.connector
- sqlalchemy

### Data Source

- The primary data source is [PhonePe Pulse GitHub](https://github.com/PhonePe/pulse/tree/master/data/aggregated/transaction/country/india/state).

### Features

#### GEO Visualization:
* The geo visualization showcases transaction amounts and counts across Indian states, plotted on a map. Additionally, it incorporates registered user counts, providing a state-wise overview on the map

#### DATA Visualization:
* The Data Visualization showcases transaction amounts, counts, and user distribution across Indian states from which we can take an key Insights to help devlop the business.
