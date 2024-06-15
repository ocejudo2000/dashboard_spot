import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Load the dataset
file_path = 'data1.csv'
try:
    data = pd.read_csv(file_path)
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# Ensure longitude values are negative
data['longitude'] = data['longitude'].apply(lambda x: -abs(x))

# Map the values to more readable formats
data['Type'] = data['Type'].map({1: 'Rent', 2: 'Sale'})
data['Price Area'] = data['Price Area'].map({1: 'All space', 2: 'By Sq M'})
data['Currency Type'] = data['Currency Type'].map({1: 'MXP', 2: 'USD'})
data['space_category'] = data['space_category'].replace('field', 'empty lot')

# Convert created_at_x to datetime
data['created_at_x'] = pd.to_datetime(data['created_at_x'], errors='coerce')

# Define filters common for both views
type_options = st.sidebar.multiselect('Type', options=data['Type'].unique(), default=data['Type'].unique())
price_area_options = st.sidebar.multiselect('Price Area', options=data['Price Area'].unique(), default=data['Price Area'].unique())
currency_options = st.sidebar.multiselect('Currency Type', options=data['Currency Type'].unique(), default=data['Currency Type'].unique())

# Filter data common for both views
filtered_data = data[
    (data['Type'].isin(type_options)) &
    (data['Price Area'].isin(price_area_options)) &
    (data['Currency Type'].isin(currency_options))
]

# Create two sections
section = st.sidebar.radio("Select View", ("Total View", "By City View"))

if section == "Total View":
    # Total View
    st.title("Spot2 Supply Dashboard - Total View")

    # Calculating key metrics for Total View
    total_spaces = filtered_data['Spot ID'].count()  # Use count instead of nunique for total spaces
    average_rate_by_category = filtered_data.groupby('space_category')['square_space'].mean().reset_index()
    total_square_footage = filtered_data['square_space'].sum()
    currency_distribution = filtered_data['Currency Type'].value_counts(normalize=True).reset_index()

    # Calculate cumulative percentage for spaces by city and count of Spot IDs per city
    spaces_by_city = filtered_data['zip_codes_city'].value_counts(normalize=True).reset_index()
    spaces_by_city.columns = ['City', 'Percentage']
    spaces_by_city['Cumulative Percentage'] = spaces_by_city['Percentage'].cumsum()
    spaces_by_city = spaces_by_city[spaces_by_city['Cumulative Percentage'] <= 0.8]
    spaces_by_city['Count'] = spaces_by_city['City'].apply(lambda x: filtered_data[filtered_data['zip_codes_city'] == x].shape[0])

    # Rename columns for clarity
    currency_distribution.columns = ['Currency Type', 'Percentage']
    currency_distribution['Percentage'] = currency_distribution['Percentage'] * 100

    st.header("Key Metrics")
    st.metric("Total Spaces", total_spaces)
    st.metric("Total Square Footage", f"{total_square_footage} sq meters")

    st.header("Average Square Footage by Category of Space")
    st.dataframe(average_rate_by_category)

    st.header("Spaces by City (80% of Total Spaces)")
    st.dataframe(spaces_by_city[['City', 'Percentage', 'Count']])

    st.header("Currency Distribution")
    st.dataframe(currency_distribution)

    # Plotting the data for Total View
    import matplotlib.pyplot as plt

    # Average square footage by category of space
    fig, ax = plt.subplots()
    average_rate_by_category.plot(kind='bar', x='space_category', y='square_space', ax=ax, color='skyblue')
    ax.set_title('Average Square Footage by Category of Space')
    ax.set_xlabel('Category of Space')
    ax.set_ylabel('Average Square Footage')
    st.pyplot(fig)

    # Amount of Spot IDs available since created_at_x up to now by category of space
    spot_ids_by_date_and_category = filtered_data.groupby([filtered_data['created_at_x'].dt.to_period('M'), 'space_category']).size().unstack().fillna(0)

    fig, ax = plt.subplots()
    spot_ids_by_date_and_category.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')
    ax.set_title('Amount of Spot IDs Available Since Creation by Category of Space')
    ax.set_xlabel('Date Created')
    ax.set_ylabel('Number of Spot IDs')
    st.pyplot(fig)

    # Map visualization for Total View
    st.header("Geographic Distribution of Spaces")
    map_center = [19.4326, -99.1332]  # Center of Mexico City

    m = folium.Map(location=map_center, zoom_start=5)

    for city, group in filtered_data.groupby('zip_codes_city'):
        folium.CircleMarker(
            location=[group['latitude'].mean(), group['longitude'].mean()],
            radius=len(group) / 10,  # Adjust size based on the number of spaces
            popup=f"{city}: {len(group)} spaces, Rate Range: {group['rate'].min()} - {group['rate'].max()}",
            color='red',
            fill=True,
            fill_color='red'
        ).add_to(m)

    # Display the map
    st_folium(m, width=700, height=500)

elif section == "By City View":
    # By City View
    st.title("Spot2 Supply Dashboard - By City View")

    # Free text search for cities
    city_search = st.sidebar.text_input('City')
    filtered_cities = data[data['zip_codes_city'].str.contains(city_search, case=False, na=False)]['zip_codes_city'].unique()
    city_options = st.sidebar.multiselect('Select City', options=['All Cities'] + list(filtered_cities), default=['All Cities'])

    # Further filter by city if selected and not "All Cities"
    if 'All Cities' not in city_options:
        filtered_data = filtered_data[filtered_data['zip_codes_city'].isin(city_options)]

    # Calculating key metrics for By City View
    total_spaces = filtered_data['Spot ID'].count()  # Use count instead of nunique for total spaces
    average_rate_by_category = filtered_data.groupby('space_category')['square_space'].mean().reset_index()
    total_square_footage = filtered_data['square_space'].sum()
    currency_distribution = filtered_data['Currency Type'].value_counts(normalize=True).reset_index()

    # Calculate cumulative percentage for spaces by city and count of Spot IDs per city
    spaces_by_city = filtered_data['zip_codes_city'].value_counts(normalize=True).reset_index()
    spaces_by_city.columns = ['City', 'Percentage']
    spaces_by_city['Cumulative Percentage'] = spaces_by_city['Percentage'].cumsum()
    spaces_by_city = spaces_by_city[spaces_by_city['Cumulative Percentage'] <= 0.8]
    spaces_by_city['Count'] = spaces_by_city['City'].apply(lambda x: filtered_data[filtered_data['zip_codes_city'] == x].shape[0])

    # Rename columns for clarity
    currency_distribution.columns = ['Currency Type', 'Percentage']
    currency_distribution['Percentage'] = currency_distribution['Percentage'] * 100

    st.header("Key Metrics")
    st.metric("Total Spaces", total_spaces)
    st.metric("Total Square Footage", f"{total_square_footage} sq meters")

    st.header("Average Square Footage by Category of Space")
    st.dataframe(average_rate_by_category)

    st.header("Spaces by City (80% of Total Spaces)")
    st.dataframe(spaces_by_city[['City', 'Percentage', 'Count']])

    st.header("Currency Distribution")
    st.dataframe(currency_distribution)

    # Plotting the data for By City View
    import matplotlib.pyplot as plt

    # Average square footage by category of space
    fig, ax = plt.subplots()
    average_rate_by_category.plot(kind='bar', x='space_category', y='square_space', ax=ax, color='skyblue')
    ax.set_title('Average Square Footage by Category of Space')
    ax.set_xlabel('Category of Space')
    ax.set_ylabel('Average Square Footage')
    st.pyplot(fig)

    # Amount of Spot IDs available since created_at_x up to now by category of space
    spot_ids_by_date_and_category = filtered_data.groupby([filtered_data['created_at_x'].dt.to_period('M'), 'space_category']).size().unstack().fillna(0)

    fig, ax = plt.subplots()
    spot_ids_by_date_and_category.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')
    ax.set_title('Amount of Spot IDs Available Since Creation by Category of Space')
    ax.set_xlabel('Date Created')
    ax.set_ylabel('Number of Spot IDs')
    st.pyplot(fig)

    # Map visualization for By City View
    st.header("Geographic Distribution of Spaces")
    map_center = [19.4326, -99.1332]  # Center of Mexico City

    m = folium.Map(location=map_center, zoom_start=5 if 'All Cities' in city_options else 12)

    for city, group in filtered_data.groupby('zip_codes_city'):
        for _, row in group.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"City: {row['zip_codes_city']}, Rate: {row['rate']}, Type: {row['Type']}, Area: {row['square_space']} sqm",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)

    # Display the map
    st_folium(m, width=700, height=500)
