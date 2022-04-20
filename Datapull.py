import requests
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType


spark = SparkSession.builder.master('local').appName('miniproject').getOrCreate()


print("=============================== Getting latitude and longitude of each active weather station in India =====================")
boundurl = "https://api.waqi.info/map/bounds/?latlng=8.06667,68.11667,37.1000,97.41667&token=043906f232b199b1feab7e384b75decff5595e02"
response = requests.get(boundurl)
data = response.json()['data']
print("============================================================================================================================")


print("================================= Storing Latitude , longitude and station data in the dataframe ===========================")
lst = []
for item in data:
    if "India" in item.get("station").get("name"):
        lat = item.get("lat")
        lon = item.get("lon")
        station = item.get("station").get("name")
        dictionary = {
            'lat': lat,
            'lon': lon,
            'station': station
        }
        lst.append(dictionary)
df = spark.createDataFrame(lst)
print("============================================================================================================================")


print("===================================== List of tuples of (Latitude, Longitude) ==============================================")
lat_list = [float(row.lat) for row in df.select('lat').collect()]
lon_list = [float(row.lon) for row in df.select('lon').collect()]
latLon_list = list(map(lambda x, y:(x,y), lat_list, lon_list))
print("============================================================================================================================")

print("============================== Getting the data from API on all the available Locations in INDIA ===========================")
Api_Key = "46e9fda3b0702522c6b6352cbe6c6e50"

station_data_lst = []
for item in latLon_list:
    stationUrl = f"http://api.openweathermap.org/data/2.5/weather?lat={item[0]}&lon={item[1]}&appid={Api_Key}"
    station_response = requests.get(stationUrl)
    station_data = station_response.json()

    sd_dict = {
        "country": station_data['sys']['country'],
        'cityid': station_data['id'],
        'cityname': station_data['name'],
        "datetime": station_data['dt'],
        "timezone": station_data['timezone'],
        "longitude": station_data['coord']['lon'],
        "latitude": station_data['coord']['lat'],
        "main": station_data['weather'][0]['main'] if 'main' in station_data['weather'][0] else 'null',
        "description": station_data['weather'][0]['description'] if 'description' in station_data['weather'][0] else 'null',
        "icon": station_data['weather'][0]['icon'] if 'icon' in station_data['weather'][0] else 'null',
        "temp_K": station_data['main']['temp'] if 'temp' in station_data['main'] else 'null',
        "feels_like_K": station_data['main']['feels_like'] if 'feels_like' in station_data['main'] else 'null',
        "temp_min_K": station_data['main']['temp_min'] if 'temp_min' in station_data['main'] else 'null',
        "temp_max_K": station_data['main']['temp_max'] if 'temp_max' in station_data['main'] else 'null',
        "pressure": station_data['main']['pressure'] if 'pressure' in station_data['main'] else 'null',
        "humidity_percent": station_data['main']['humidity'] if 'humidity' in station_data['main'] else 'null',
        "pressure_sea_level_hPa": station_data['main']['sea_level'] if 'sea_level' in station_data['main'] else 'null',
        "pressure_ground_level_hPa": station_data['main']['grnd_level'] if 'grnd_level' in station_data['main'] else 'null',
        "visibility_m": station_data['visibility'] if 'visibility' in station_data else 'null',
        "windspeed_mps": station_data['wind']['speed'] if 'speed' in station_data['wind'] else 'null',
        "wind_direction_deg": station_data['wind']['deg']  if 'deg' in station_data['wind'] else 'null',
        "gust_mps": station_data['wind']['gust'] if 'gust' in station_data['wind'] else 'null',
        "cloudiness_percent": station_data['clouds']['all'] if 'all' in station_data['clouds'] else 'null',
        "sunrise": station_data['sys']['sunrise'],
        'sunset': station_data['sys']['sunset']
    }
    station_data_lst.append(sd_dict)
print("============================================================================================================================")


print("================================== Storing the data in dataframe and then appending to the dq_good==========================")
schema = StructType([ \
    StructField("country",StringType(),True), \
    StructField("cityid",StringType(),True), \
    StructField("cityname",StringType(),True), \
    StructField("datetime", StringType(), True), \
    StructField("timezone", StringType(), True), \
    StructField("longitude", StringType(), True), \
    StructField("latitude", StringType(), True), \
    StructField("main", StringType(), True), \
    StructField("description", StringType(), True), \
    StructField("icon", StringType(), True), \
    StructField("temp_K", StringType(), True), \
    StructField("feels_like_K", StringType(), True), \
    StructField("temp_min_K", StringType(), True), \
    StructField("temp_max_K", StringType(), True), \
    StructField("pressure", StringType(), True), \
    StructField("humidity_percent", StringType(), True), \
    StructField("pressure_sea_level_hPa", StringType(), True), \
    StructField("pressure_ground_level_hPa", StringType(), True), \
    StructField("visibility_m", StringType(), True), \
    StructField("windspeed_mps", StringType(), True), \
    StructField("wind_direction_deg", StringType(), True), \
    StructField("gust_mps" , StringType(), True), \
    StructField("cloudiness_percent", StringType(), True), \
    StructField("sunrise", StringType(), True), \
    StructField("sunset", StringType(), True)
])

station_hour_df = spark.createDataFrame(station_data_lst,schema=schema)
station_hour_df.write.csv("hdfs://localhost:9000/miniproject/raw/dq_good/data.csv",mode='append',header=True)
print("=============================================================================================================================")
