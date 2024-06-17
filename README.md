##Spot2 Supply Dashboard

#Overview
The Spot2 Supply Dashboard is an interactive web application developed using Streamlit and Folium. It provides a comprehensive view of the supply of commercial spaces, including rent and sale options, across various cities. This application allows users to filter and visualize data by type, price area, and currency, and provides detailed geographic distributions and key metrics of the available spaces.

#Features

Total View: Displays overall metrics, average square footage by category, currency distribution, and a geographic map of spaces with rate ranges.
By City View: Allows users to filter and visualize data for specific cities, showing detailed information about each space on a map.
Interactive Filters: Users can filter data by type, price area, and currency.
Geographic Visualization: Utilizes Folium to create interactive maps showing the distribution of spaces and their details.
Key Metrics: Includes total spaces, total square footage, average square footage by category, and currency distribution.

#Prerequisites

Python 3.6 or higher
Required Python packages:
streamlit
pandas
folium
streamlit_folium

#Installation

1. Clone the repository:
git clone https://github.com/your-repo/spot2-dashboard.git
cd spot2-dashboard

2. Create a virtual environment and activate it:
python3 -m venv myvenv
source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate

#Usage
1. Prepare your dataset:
Ensure your dataset is named data1.csv and placed in the root directory of the project.
The dataset should include the following columns: longitude, latitude, Type, Price Area, Currency Type, space_category, created_at_x, zip_codes_city, rate, square_space.
2. Run the Streamlit app:
streamlit run dashboard_spot.py
3. Access the dashboard:
Open your web browser and go to http://localhost:8501.


#Script Explanation
The script is divided into the following sections:

1. Data Loading and Preparation:

Loads the dataset using pandas.
Ensures longitude values are negative.
Maps integer values to human-readable formats for Type, Price Area, and Currency Type.
Converts created_at_x to a datetime format.

2. Filters and Sections:

Defines filters for type, price area, and currency.
Creates two main sections: Total View and By City View.

3. Total View:

Calculates and displays key metrics.
Provides data visualizations for average square footage by category and the amount of Spot IDs available since creation by category.
Shows a geographic map with rate ranges for each city.

4. By City View:

Allows users to search and select specific cities.
Displays detailed information about each space on an interactive map.
Visualizes key metrics and provides data visualizations similar to the Total View.


#Contribution
Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure your code adheres to the existing coding style and includes relevant tests.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For questions or feedback, please contact [Oscar Cejudo] at [ocejudo@hotmail.com].
