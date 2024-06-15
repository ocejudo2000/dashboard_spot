import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

# Load the dataset
file_path = 'data1.csv'
data = pd.read_csv(file_path)

# Ensure longitude values are negative
data['longitude'] = data['longitude'].apply(lambda x: -abs(x))

# Function to calculate distance between two points
def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers

# Streamlit app layout
st.title("Find Nearest Spaces")

# Input options
zip_code_input = st.text_input("Enter a Zip Code:")
num_locations = st.number_input("Number of Locations to Find:", min_value=1, value=5)
radius = st.number_input("Radius in Kilometers:", min_value=1.0, value=5.0)

# Display Google Map for user to select a point
st.write("Or select a point on the map:")
map_center = [19.4326, -99.1332]  # Center of Mexico City by default
m = folium.Map(location=map_center, zoom_start=12)
selected_point = st_folium(m, width=700, height=500)

# Variables to store the latitude and longitude of the selected point
latitude, longitude = None, None

if selected_point:
    if 'last_clicked' in selected_point and selected_point['last_clicked'] is not None:
        latitude = selected_point['last_clicked']['lat']
        longitude = selected_point['last_clicked']['lng']

# Find the zip code of the selected point
selected_zip_code = None
if latitude is not None and longitude is not None:
    point_data = data.apply(lambda row: calculate_distance(latitude, longitude, row['latitude'], row['longitude']), axis=1)
    nearest_point = data.iloc[point_data.idxmin()]
    selected_zip_code = nearest_point['zip_code_id']

if selected_zip_code:
    st.write(f"Zip Code of selected point: {selected_zip_code}")

# Submit button
if st.button("Submit"):
    # Find nearest spaces based on the selected criteria
    if zip_code_input or (latitude is not None and longitude is not None):
        if zip_code_input:
            # Use the latitude and longitude of the entered zip code
            zip_code_data = data[data['zip_code_id'] == zip_code_input]
            if not zip_code_data.empty:
                latitude = zip_code_data.iloc[0]['latitude']
                longitude = zip_code_data.iloc[0]['longitude']
            else:
                st.error("Invalid Zip Code. Please try again.")
                st.stop()
        
        if latitude is not None and longitude is not None:
            # Drop rows with missing latitude or longitude values
            data = data.dropna(subset=['latitude', 'longitude'])

            # Calculate distances and filter based on the radius
            data['distance'] = data.apply(lambda row: calculate_distance(latitude, longitude, row['latitude'], row['longitude']), axis=1)
            filtered_data = data[data['distance'] <= radius].nsmallest(num_locations, 'distance')

            if filtered_data.empty:
                st.write("No spaces found within the specified radius.")
            else:
                st.write(f"Found {len(filtered_data)} spaces within {radius} km:")
                st.dataframe(filtered_data)

                # Display the locations on the map
                m = folium.Map(location=[latitude, longitude], zoom_start=12)
                folium.Marker([latitude, longitude], tooltip="Selected Location", icon=folium.Icon(color='blue')).add_to(m)

                for _, row in filtered_data.iterrows():
                    folium.Marker(
                        [row['latitude'], row['longitude']],
                        tooltip=f"Spot ID: {row['Spot ID']}",
                        popup=f"Spot ID: {row['Spot ID']}\nType: {row['Type']}\nPrice Area: {row['Price Area']}\nCurrency Type: {row['Currency Type']}\nSquare Space: {row['square_space']}",
                        icon=folium.Icon(color='red')
                    ).add_to(m)

                # Display the map
                st_folium(m, width=700, height=500)
    else:
        st.write("Please enter a Zip Code or select a point on the map.")
