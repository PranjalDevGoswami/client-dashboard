import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt


st.set_page_config(page_title="Dashboard", page_icon="🏢", layout="wide")
# Load data
import pandas as pd
import numpy as np

# Load data
file_path1 = r'/home/kumarp/Downloads/EduDashboard/Boult Data.xlsx'
data1 = pd.read_excel(file_path1)

# Get unique values
gender = data1['Gender'].unique()
age_range = data1['Age Range'].unique()
qualification = data1['Highest Qualification'].unique()
occupation = data1['Ocupation'].unique()  # Correct typo from 'Ocupation'
location = data1['Location'].unique()
respondent = data1['A1'].unique()
brand = data1['First Audio device Brand on Mind'].unique()


# Find the maximum length of the unique arrays
max_length = max(len(gender), len(age_range), len(qualification), len(occupation), len(location),len(brand))

# Pad the arrays with NaN to make them the same length
gender = np.pad(gender, (0, max_length - len(gender)), constant_values=np.nan)
age_range = np.pad(age_range, (0, max_length - len(age_range)), constant_values=np.nan)
qualification = np.pad(qualification, (0, max_length - len(qualification)), constant_values=np.nan)
occupation = np.pad(occupation, (0, max_length - len(occupation)), constant_values=np.nan)
location = np.pad(location, (0, max_length - len(location)), constant_values=np.nan)
brand = np.pad(brand, (0, max_length-len(brand)), constant_values=np.nan)

# Create a single DataFrame
df = pd.DataFrame({
    
    'Gender': gender,
    'Age Range': age_range,
    'Highest Qualification': qualification,
    'Ocupation': occupation,
    'Location': location,
    'Brand':brand
  
})

# Print the DataFrame (optional)

age_range_counts = data1['Age Range'].value_counts(dropna=False) 

location_counts = data1['Location'].value_counts(dropna=False)  # Include NaN if needed

boult_audio_data = data1[data1['First Audio device Brand on Mind'] == 'Boult Audio']
boult_gender_distribution = boult_audio_data['Gender'].value_counts()
boult_age_range_distribution = boult_audio_data['Age Range'].value_counts()

# Calculate percentages for display
boult_gender_percentage = boult_audio_data['Gender'].value_counts(normalize=True) * 100
boult_age_range_percentage = boult_audio_data['Age Range'].value_counts(normalize=True) * 100

combined_distribution = pd.DataFrame({
    'Category': ['Gender'] * len(boult_gender_distribution) + ['Age Range'] * len(boult_age_range_distribution),
    'Type': boult_gender_distribution.index.tolist() + boult_age_range_distribution.index.tolist(),
    'Count': boult_gender_distribution.values.tolist() + boult_age_range_distribution.values.tolist()
})





brand_mapping = {
    1: 'Boult Audio',
    2: 'boAt',
    3: 'Noise',
    4: 'Fireboltt',
    5: 'Dizo',
    6: 'ptron',
    7: 'Skullcandy',
    8: 'Mivi',
    9: 'OnePlus',
    10: 'Realme',
    98: 'Others'
}
 
positive_mapping = {#E2
    1: 'Affordable Price',
    2: 'Sales promotion, discounts and offers',
    3: 'Good battery',
    4: 'Good bass',
    5: 'Noise cancellation',
    6: 'Fast charging',
    7: 'After sales service',
    8: 'Easy availability',
    9: 'Brand image',
    10: 'Recommended by friends and family',
    98: 'Others'
}
 
negative_mapping = {#E3
    1: 'Unaffordable Price',
    2: 'No sales promotion, discounts and offers',
    3: 'Unsatisfactory After sale services',
    4: 'Poor product built',
    5: 'Poor customer support',
    6: 'Not easily available',
    7: 'Poor brand image',
    8: 'Negative word of mouth',
    9: 'Poor audio quality',
    10: 'Guarantee and warranty',
}



#Tabs
tabs = st.tabs(["Gender", "Brand Awareness","Boult User Coverage", "Brand Consumption", "Brand Performance"])

# Demography tab
# Demography tab
with tabs[0]:
    st.header("Gender")

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        persona = st.selectbox("Select Persona", data1['Gender'].unique())
    with col2:
        date_range = st.date_input("Select Date Range", [])

    # Charts
    col3, col4 = st.columns(2)
    with col3:
        # Pie chart for Gender count
        gender_counts = data1['Gender'].value_counts()
        fig = px.pie(values=gender_counts.values, names=gender_counts.index, title='Gender Count')
        st.plotly_chart(fig)

    with col4:
        # Bar chart for Occupation count
        occupation_counts = data1['Ocupation'].value_counts()
        fig = px.bar(x=occupation_counts.index, y=occupation_counts.values, title='Occupation Type Count')
        st.plotly_chart(fig)
        
        
    col5, col6 = st.columns(2)
    with col5:
        st.header("Age Range Respondent Count")

        # Display Age Range Counts
        age_range_df = age_range_counts.reset_index()
        age_range_df.columns = ['Age Range', 'Respondent Count']
        fig = px.bar(age_range_df, x='Age Range', y='Respondent Count', title='Age Range Respondent Count')
        st.plotly_chart(fig)
        
    with col6:
        st.header("Consumer Profile")
        fig_combined_distribution = px.bar(combined_distribution, x='Type', y='Count', color='Category', barmode='group',
                                   title='Gender and Age Range Distribution for Boult Audio Customers')
        st.plotly_chart(fig_combined_distribution)
       

# Brand Awareness tab
with tabs[1]:
    st.header("Brand Awareness")
    
    col1 , col2 = st.columns(2)
    with col1:
        age_range_count = data1['Smartwatch1'].value_counts()
        fig = px.pie(values=age_range_count.values, names=age_range_count.index, title='Smartwatch Count')
        st.plotly_chart(fig)
    
    with col2:
        st.header("Location-wise Respondent Count")
        location_df = location_counts.reset_index()
        location_df.columns = ['Location', 'Respondent Count']
        fig = px.bar(location_df, x='Location', y='Respondent Count', title='Location-wise Respondent Count')
        st.plotly_chart(fig)
        
        
        
# Brand Consumption tab
with tabs[2]:
    st.header("Boult User Coverage")
    col1, col2 = st.columns(2)
    
    with col1:
        total_respondents = len(data1['A1'])
        location_counts = data1['Zone'].value_counts(dropna=False)
        location_percentages = (location_counts / total_respondents) * 100

        # Create a DataFrame for Plotly
        pie_data = pd.DataFrame({'Zone': location_percentages.index, 'Percentage': location_percentages.values})

        # Create a pie chart
        fig = px.pie(pie_data, values='Percentage', names='Zone', title='Respondent Distribution by Zone')
        st.plotly_chart(fig)

    with col2:
        st.header("Brand User Coverage")
        total_respondents = len(data1['A1'])
        location_counts = data1['Location'].value_counts(dropna=False)
        location_percentages = (location_counts / total_respondents) * 100

        # Create a DataFrame for Plotly
        pie_data = pd.DataFrame({'Location': location_percentages.index, 'Percentage': location_percentages.values})

        # Create a bar chart (replace px.pie with px.bar)
        fig = px.bar(pie_data, x='Location', y='Percentage', title='Respondent Distribution by Location')
        st.plotly_chart(fig)

# Smartphone tab
with tabs[3]:
    st.header("Brand Consumption")
    import streamlit as st
    import pandas as pd
    import numpy as np
    import pydeck as pdk

    chart_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=["lat", "lon"],
    )

    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=37.76,
                longitude=-122.4,
                zoom=11,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=chart_data,
                    get_position="[lon, lat]",
                    radius=200,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
                pdk.Layer(
                    "ScatterplotLayer",
                    data=chart_data,
                    get_position="[lon, lat]",
                    get_color="[200, 30, 0, 160]",
                    get_radius=200,
                ),
            ],
        )
    )

# Brand Performance tab
with tabs[4]:
    st.header("Brand Performance")
    brands_counts = data1['First Audio device Brand on Mind'].value_counts(dropna=False)

    # Map positive values
    positive_mapping = data1['Affordable Price'].value_counts(dropna=False)

    # Create the Bar Chart
    fig, ax = plt.subplots(figsize=(14, 8))  # Increase the figure size
    bar_width = 0.35

    # Plot positive and negative reviews separately
    positive_counts = data1[data1['Affordable Price'] == 1]['First Audio device Brand on Mind'].value_counts()
    negative_counts = data1[data1['Affordable Price'] == 0]['First Audio device Brand on Mind'].value_counts()

    # Align the indices of both counts to avoid mismatches
    all_brands = data1['First Audio device Brand on Mind'].unique()
    positive_counts = positive_counts.reindex(all_brands, fill_value=0)
    negative_counts = negative_counts.reindex(all_brands, fill_value=0)

    # Sort the brands by total reviews for better arrangement
    total_counts = positive_counts + negative_counts
    sorted_brands = total_counts.sort_values(ascending=False).index

    positive_counts = positive_counts.reindex(sorted_brands)
    negative_counts = negative_counts.reindex(sorted_brands)

    index = range(len(sorted_brands))

    bar1 = ax.bar(index, positive_counts, bar_width, label='Positive Reviews')
    bar2 = ax.bar(index, negative_counts, bar_width, bottom=positive_counts, label='Negative Reviews')

    ax.set_xlabel('Brand')
    ax.set_ylabel('Number of Reviews')
    ax.set_title('Brand Performance Based on Reviews')
    ax.set_xticks(index)
    ax.set_xticklabels(sorted_brands, rotation=45, ha='right')  # Rotate labels and align right
    ax.legend()

    # Display the Bar Chart in Streamlit
    st.pyplot(fig)
