#################### Creating a hie database #####################

CREATE DATABASE [IF NOT EXISTS] weatherdb;

#################### Creating a hive table #######################

create table weather_data_parquet (
    cityname string,
    datetime BIGINT,
    temp_K double,
    pressure BIGINT,
    humidity_percent BIGINT,
    windspeed_mps double,
    cloudiness_percent BIGINT
    )
row format delimited
fields terminated by ',' 
stored as parquet
location 'hdfs://localhost:9000/miniproject/raw/persist/date.parquet';



####### Creating a PARTITIONED table based on cityname ###########

create table weather_data_partitioned (
    datetime BIGINT,
    temp_K double,
    pressure BIGINT,
    humidity_percent BIGINT,
    windspeed_mps double,
    cloudiness_percent BIGINT
    )
    PARTITIONED BY(cityname string);



