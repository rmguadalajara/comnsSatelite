import matplotlib.pyplot as plt
import functions as func
import webbrowser
import folium
import pandas as pd
def plot_traces(ground_station, satellite):
    # Plot ground station trace in blue
    plt.plot(ground_station['longitude'], ground_station['latitude'], color='blue', label='Ground Station Trace')
    
    # Plot visible satellite trace in red
    plt.plot(satellite['longitude'], satellite['latitude'], color='red', label='Visible Satellite Trace')
    
    # Set plot title and labels
    plt.title('Ground Station and Visible Satellite Traces')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    
    # Add legend
    plt.legend()
    
    # Show the plot
    plt.show()

# función que pinta una ventana la incrusta un mapa de bing y el dataFrame de la traza del satélite
def plot_satellite_trace(ground_station, satellite):
    # Create a map
    satellite_trace_map = folium.Map(location=[ground_station['latitude'], ground_station['longitude']], zoom_start=3)
    
    # Add the ground station to the map
    folium.Marker([ground_station['latitude'], ground_station['longitude']], popup='Ground Station', icon=folium.Icon(color='blue')).add_to(satellite_trace_map)
    
    # Add the satellite trace to the map
    for i in range(len(satellite)):
        folium.Marker([satellite['latitude'][i], satellite['longitude'][i]], popup='Visible Satellite', icon=folium.Icon(color='red')).add_to(satellite_trace_map)
    
    # Save the map
    satellite_trace_map.save('satellite_trace_map.html')
    
    # Open the map
    webbrowser.open('satellite_trace_map.html')


#funcion que calcula la traza de un satélite sobre un mapa dados sus parámetros orbitales
def calculate_satellite_trace(ground_station, satellite):
    # Create a list to store the satellite trace
    satellite_trace = []

    # Calculate the satellite trace
    for i in range(0, 360, 1):
        # Calculate the satellite position
        satellite_position = func.calculate_satellite_position(satellite['semimajor_axis'], satellite['eccentricity'], satellite['inclination'], satellite['RAAN'], satellite['argument_of_perigee'], satellite['true_anomaly'], i)

        # Calculate the distance between the ground station and the satellite
        distance_between_ground_station_and_satellite = func.calculate_distance_between_terrain_station_and_satellite(ground_station['latitude'], ground_station['longitude'], satellite_position[0], satellite_position[1], ground_station['altitude'], satellite_position[2])

        # Calculate the elevation
        elevation = func.calculate_elevation(ground_station['latitude'], ground_station['longitude'], satellite_position[0], satellite_position[1])

        # Check if the satellite is visible
        if elevation > 10:
            # Append the satellite position to the satellite trace
            satellite_trace.append([satellite_position[0], satellite_position[1], satellite_position[2], distance_between_ground_station_and_satellite, elevation])

    # Convert the satellite trace to a Pandas DataFrame
    satellite_trace = pd.DataFrame(satellite_trace, columns=['latitude', 'longitude', 'altitude', 'distance_between_ground_station_and_satellite', 'elevation'])

    # Return the satellite trace
    return satellite_trace