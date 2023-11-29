import math

def calculate_azimuth(lat1, lon1, lat2, lon2):
    dlon = lon2 - lon1
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    brng = math.atan2(x, y)
    brng = math.degrees(brng)
    brng = (brng + 360) % 360
    brng = 360 - brng
    return brng

def calculate_distance_between_points(lat1, lon1, lat2, lon2):
    R = 6371e3
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    lon1 = math.radians(lon1)
    lon2 = math.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d

def calculate_distance_between_terrain_station_and_satellite(terrain_station_lat, terrain_station_lon, satellite_lat, satellite_lon, terrain_station_altitude, satellite_altitude):
    distance_between_terrain_station_and_satellite = math.sqrt(math.pow(calculate_distance_between_points(terrain_station_lat, terrain_station_lon, satellite_lat, satellite_lon), 2) + math.pow(terrain_station_altitude - satellite_altitude, 2))
    return distance_between_terrain_station_and_satellite

def calculate_elevation(antenna_lat, antenna_lon, satellite_lat, satellite_lon):
    antenna_lat = math.radians(antenna_lat)
    antenna_lon = math.radians(antenna_lon)
    satellite_lat = math.radians(satellite_lat)
    satellite_lon = math.radians(satellite_lon)

    elevation = math.degrees(math.asin(math.sin(antenna_lat) * math.sin(satellite_lat) + math.cos(antenna_lat) * math.cos(satellite_lat) * math.cos(antenna_lon - satellite_lon)))
    return elevation

def Xmtr_pow(pot_saturacion, perdidas_antena):
    Xmtr_pow = 10 * math.log10(pot_saturacion) - perdidas_antena
    return Xmtr_pow

def calculate_Xmtr_gain(pot_saturacion, diametro_antena, frec_ascendente):
    Xmtr_gain = 20 * math.log10((pot_saturacion * ((math.pi * diametro_antena * frec_ascendente) * 10 / 3)))
    return Xmtr_gain

def calculate_pire(Xmtr_pow, Xmtr_gain, backout):
    pire = Xmtr_pow + Xmtr_gain - backout
    return pire

def calculate_free_space_loss(frec_ascendente, frec_descendente, distance_between_terrain_station_and_satellite):
    free_space_loss = 20 * math.log10((4 * math.pi * distance_between_terrain_station_and_satellite * frec_ascendente * frec_descendente) / 299792458)
    return free_space_loss

def calculate_gas_attenuation(frec_ascendente, frec_descendente, distance_between_terrain_station_and_satellite, terrain_station_altitude, satellite_altitude):
    gas_attenuation = 0.07 * math.pow(frec_ascendente, 2) / (distance_between_terrain_station_and_satellite * math.sqrt(terrain_station_altitude)) + 0.07 * math.pow(frec_descendente, 2) / (distance_between_terrain_station_and_satellite * math.sqrt(satellite_altitude))
    return gas_attenuation

def calculate_rain_attenuation(frec_ascendente, frec_descendente, distance_between_terrain_station_and_satellite, terrain_station_altitude, satellite_altitude):
    rain_attenuation = 0.0001 * math.pow(frec_ascendente, 2) / (distance_between_terrain_station_and_satellite * math.sqrt(terrain_station_altitude)) + 0.0001 * math.pow(frec_descendente, 2) / (distance_between_terrain_station_and_satellite * math.sqrt(satellite_altitude))
    return rain_attenuation

def calculate_cloud_attenuation(frec_ascendente, frec_descendente, distance_between_terrain_station_and_satellite, terrain_station_altitude, satellite_altitude):
    cloud_attenuation = 0.0001 * math.pow(frec_ascendente, 2) / (distance_between_terrain_station_and_satellite * math.sqrt(terrain_station_altitude)) + 0.0001 * math.pow(frec_descendente, 2) / (distance_between_terrain_station_and_satellite * math.sqrt(satellite_altitude))
    return cloud_attenuation
def calculate_atmospheric_attenuation(frec_ascendente, frec_descendente, distance_between_terrain_station_and_satellite, terrain_station_altitude, satellite_altitude, rs, rt):
    atmospheric_attenuation = calculate_gas_attenuation(frec_ascendente, frec_descendente, distance_between_terrain_station_and_satellite, terrain_station_altitude, satellite_altitude) + calculate_rain_attenuation(frec_ascendente, frec_descendente, distance_between_terrain_station_and_satellite, terrain_station_altitude, satellite_altitude, rs, rt) + calculate_cloud_attenuation(frec_ascendente, frec_descendente, distance_between_terrain_station_and_satellite, terrain_station_altitude, satellite_altitude, rs, rt)
    return atmospheric_attenuation

def calculate_propagation_loss(frec_ascendente, frec_descendente, distance_between_terrain_station_and_satellite, terrain_station_altitude, satellite_altitude, rs, rt):
    propagation_loss = calculate_free_space_loss(frec_ascendente, frec_descendente, distance_between_terrain_station_and_satellite) + calculate_atmospheric_attenuation(frec_ascendente, frec_descendente, distance_between_terrain_station_and_satellite, terrain_station_altitude, satellite_altitude, rs, rt)
    return propagation_loss

def calculate_recieved_isotropic_power(Xmtr_pow, Xmtr_gain, propagation_loss):
    recieved_isotropic_power = Xmtr_pow + Xmtr_gain - propagation_loss
    return recieved_isotropic_power

def calculate_power_flux_density(recieved_isotropic_power, diametro_antena, frec_ascendente):
    power_flux_density = recieved_isotropic_power + 10 * math.log10((math.pow(diametro_antena, 2) * frec_ascendente) / 41253.4)
    return power_flux_density

def calculate_equivalent_temperature(terrain_station_altitude, satellite_altitude):
    equivalent_temperature = 290 * math.pow((terrain_station_altitude / satellite_altitude), 0.5)
    return equivalent_temperature

def calculate_noise_factor(terrain_station_altitude, satellite_altitude):
    noise_factor = 1.5 * math.pow((terrain_station_altitude / satellite_altitude), 0.5)
    return noise_factor

def calculate_noise_temperature(equivalent_temperature, noise_factor):
    noise_temperature = equivalent_temperature * noise_factor
    return noise_temperature

def calculate_noise_power(noise_temperature, frec_ascendente):
    noise_power = 10 * math.log10((1.38 * math.pow(10, -23) * noise_temperature * frec_ascendente * 1000000))
    return noise_power

def calculate_carrier_to_noise_ratio(power_flux_density, noise_power):
    carrier_to_noise_ratio = power_flux_density - noise_power
    return carrier_to_noise_ratio

def calculate_carrier_to_noise_density_ratio(carrier_to_noise_ratio, roll_off):
    carrier_to_noise_density_ratio = carrier_to_noise_ratio - 10 * math.log10(roll_off)
    return carrier_to_noise_density_ratio

def calculate_reciever_gain(antenna_gain, equivalent_temperature):
    reciever_gain = antenna_gain + 10 * math.log10(equivalent_temperature)
    return reciever_gain

def calculate_bandiwth_BPSK(Rb):
    bandwidth_BPSK = Rb
    return bandwidth_BPSK

def calculate_bandiwth_QPSK(Rb):
    bandwidth_QPSK = 2 * Rb
    return bandwidth_QPSK

def calculate_bandiwth_16QAM(Rb):
    bandwidth_16QAM = 4 * Rb
    return bandwidth_16QAM

def calculate_bandiwth_64QAM(Rb):
    bandwidth_64QAM = 6 * Rb
    return bandwidth_64QAM

def calculate_bandiwth_256QAM(Rb):
    bandwidth_256QAM = 8 * Rb
    return bandwidth_256QAM

def calculate_bandwidth(modulation, Rb):
    if modulation == "BPSK":
        bandwidth = calculate_bandiwth_BPSK(Rb)
    elif modulation == "QPSK":
        bandwidth = calculate_bandiwth_QPSK(Rb)
    elif modulation == "16QAM":
        bandwidth = calculate_bandiwth_16QAM(Rb)
    elif modulation == "64QAM":
        bandwidth = calculate_bandiwth_64QAM(Rb)
    elif modulation == "256QAM":
        bandwidth = calculate_bandiwth_256QAM(Rb)
    return bandwidth

def calculate_satellite_position(semimajor_axis, eccentricity, inclination, RAAN, argument_of_perigee, true_anomaly, time):
    # Calculate the mean motion
    mean_motion = math.sqrt(398600.4418 / math.pow(semimajor_axis, 3))

    # Calculate the mean anomaly
    mean_anomaly = mean_motion * time

    # Calculate the eccentric anomaly
    eccentric_anomaly = mean_anomaly + eccentricity * math.sin(mean_anomaly) * (1.0 + eccentricity * math.cos(mean_anomaly))

    # Calculate the true anomaly
    true_anomaly = math.acos((math.cos(eccentric_anomaly) - eccentricity) / (1.0 - eccentricity * math.cos(eccentric_anomaly)))

    # Calculate the argument of latitude
    argument_of_latitude = true_anomaly + argument_of_perigee

    # Calculate the radius
    radius = semimajor_axis * (1.0 - eccentricity * math.cos(eccentric_anomaly))

    # Calculate the position in the orbital plane
    x_orbital_plane = radius * math.cos(argument_of_latitude)
    y_orbital_plane = radius * math.sin(argument_of_latitude)

    # Calculate the position in the ECI frame
    x_ECI = x_orbital_plane * (math.cos(RAAN) * math.cos(inclination) - math.sin(RAAN) * math.sin(inclination) * math.cos(argument_of_latitude)) - y_orbital_plane * (math.sin(RAAN) * math.cos(inclination) + math.cos(RAAN) * math.sin(inclination) * math.cos(argument_of_latitude))
    y_ECI = x_orbital_plane * (math.cos(RAAN) * math.sin(inclination) + math.sin(RAAN) * math.cos(inclination) * math.cos(argument_of_latitude)) + y_orbital_plane * (math.cos(RAAN) * math.cos(inclination) - math.sin(RAAN) * math.sin(inclination) * math.cos(argument_of_latitude))
    z_ECI = x_orbital_plane * (math.sin(RAAN) * math.sin(argument_of_latitude)) + y_orbital_plane * (math.cos(RAAN) * math.sin(argument_of_latitude))

    return [x_ECI, y_ECI, z_ECI]