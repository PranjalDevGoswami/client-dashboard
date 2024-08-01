import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Load data
file_path = r'/home/kumarp/Downloads/EduDashboard/Raw_Data_File-21122022_V1.xlsx'
data = pd.read_excel(file_path)

# Define filter mappings
location_mapping = {
    1: 'Delhi NCR',
    2: 'Chandigarh',
    3: 'Jaipur',
    4: 'Lucknow',
    5: 'Mumbai',
    6: 'Ahmedabad',
    7: 'Pune',
    8: 'Kolkata',
    9: 'Patna',
    10: 'Agra',
    11: 'Chennai',
    12: 'Bangalore',
    13: 'Cochin',
    14: 'Visakhapatnam',
    15: 'Madurai',
    16: 'Vijayawada',
    # 98: 'Others (Specify)',
}

gender_mapping = {
    1: 'Male',
    2: 'Female',
}

age_group_mapping = {
    1: 'Below 18',
    2: '18-27 years',
    3: '28-36 years',
    4: '37-45 years',
    6: '46 and above'
}

education_mapping = {
    1: 'Illiterate',
    2: 'Literate but no formal schooling/ School-Upto4 years',
    3: 'School-5 to 9 years',
    4: 'SSC / HSC (School upto 10 – 12 years)',
    5: 'Some College (including a Diploma) but not Grad',
    6: 'Graduate/ Postgraduate: General',
    7: 'Graduate/ Postgraduate: Professional'
}

reverse_location_mapping = {v: k for k, v in location_mapping.items()}
reverse_gender_mapping = {v: k for k, v in gender_mapping.items()}
reverse_age_group_mapping = {v: k for k, v in age_group_mapping.items()}
reverse_education_mapping = {v: k for k, v in education_mapping.items()}

# Streamlit header for filters
st.header("Filters")
col1, col2, col3, col4 = st.columns(4)

location_options = ['All'] + list(location_mapping.values())
gender_options = ['All'] + list(gender_mapping.values())
age_group_options = ['All'] + list(age_group_mapping.values())
education_options = ['All'] + list(education_mapping.values())

location = col1.selectbox("Location", location_options)
gender = col2.selectbox("Gender", gender_options)
age_group = col3.selectbox("Age Group", age_group_options)
education = col4.selectbox("Education", education_options)

# Function to get filter values
def get_filter_values(selected_value, mapping_column, reverse_mapping):
    if selected_value == 'All':
        return data[mapping_column].unique().tolist()
    return [reverse_mapping[selected_value]] if selected_value in reverse_mapping else []

# Get filter values
location_value = get_filter_values(location, 'A3', reverse_location_mapping)
gender_value = get_filter_values(gender, 'A4', reverse_gender_mapping)
age_group_value = get_filter_values(age_group, 'A5', reverse_age_group_mapping)
education_value = get_filter_values(education, 'A7', reverse_education_mapping)

# Apply filters
filtered_data = data[
    (data['A3'].isin(location_value)) & 
    (data['A4'].isin(gender_value)) & 
    (data['A5'].isin(age_group_value)) & 
    (data['A7'].isin(education_value))
]

# Plot pie chart if data is available
if not filtered_data.empty and 'A7' in filtered_data.columns:
    pie_data = filtered_data['A7'].value_counts().reset_index()
    pie_data.columns = ['Education Level', 'Count']
    pie_data['Education Level'] = pie_data['Education Level'].map(education_mapping)
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=pie_data['Education Level'],
        values=pie_data['Count'],
        textinfo='label+percent',
        hole=0.3
    )])
    fig_pie.update_layout(
        title='Distribution of Education Levels',
        showlegend=True,
        legend_title='Education Levels',
        legend=dict(x=0.8, y=0.8)
    )
    st.plotly_chart(fig_pie)
else:
    st.write("No data to display in pie chart.")

# Plot bar chart if data is available
if not filtered_data.empty and 'A7' in filtered_data.columns:
    bar_data = filtered_data['A7'].value_counts().reset_index()
    bar_data.columns = ['Education Level', 'Count']
    bar_data['Education Level'] = bar_data['Education Level'].map(education_mapping)
    
    fig_bar = px.bar(
        bar_data,
        y='Education Level',
        x='Count',
        title='Count of Each Education Level',
        labels={'Education Level': 'Education Level', 'Count': 'Count'},
        orientation='h'
    )
    fig_bar.update_layout(
        xaxis_title='Count',
        yaxis_title='Education Level',
    )
    st.plotly_chart(fig_bar)
else:
    st.write("No data to display in bar chart.")

# Prepare data for Sankey diagram
if not filtered_data.empty:
    # Ensure that 'A5' and 'A7' have valid mappings
    filtered_data = filtered_data[
        filtered_data['A5'].isin(reverse_age_group_mapping.values()) &
        filtered_data['A7'].isin(reverse_education_mapping.values())
    ]
    
    # Prepare Sankey diagram data
    sankey_data = filtered_data.groupby(['A5', 'A7']).size().reset_index(name='Count')
    
    # Nodes
    age_groups = list(age_group_mapping.values())
    education_levels = list(education_mapping.values())
    all_nodes = age_groups + education_levels
    node_labels = all_nodes
    node_indices = {label: idx for idx, label in enumerate(node_labels)}

    # Define a color palette
    color_palette = px.colors.qualitative.Plotly
    colors = [color_palette[i % len(color_palette)] for i in range(len(sankey_data))]
    
    # Create links with color
    links = []
    link_colors = []
    for i, (_, row) in enumerate(sankey_data.iterrows()):
        source = node_indices.get(age_group_mapping.get(row['A5'], 'Unknown'), None)
        target = node_indices.get(education_mapping.get(row['A7'], 'Unknown'), None)
        
        # Skip any links with unknown or None values
        if source is not None and target is not None:
            links.append({'source': source, 'target': target, 'value': row['Count']})
            link_colors.append(colors[i % len(colors)])

    # Create Sankey diagram
    if links:
        fig_sankey = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color='black', width=0.5),
                label=node_labels
            ),
            link=dict(
                source=[link['source'] for link in links],
                target=[link['target'] for link in links],
                value=[link['value'] for link in links],
                color=link_colors  # Add color to links
            )
        )])
        fig_sankey.update_layout(title_text="Sankey Diagram of Age Group to Education Level Flow")
        st.plotly_chart(fig_sankey)
    else:
        st.write("No valid data to display in Sankey diagram.")
else:
    st.write("No data to display in Sankey diagram.")

# Display filtered data
st.write("Filtered Data", filtered_data)

