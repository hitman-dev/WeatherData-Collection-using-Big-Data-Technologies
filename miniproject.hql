use weatherdb;

set hive.exec.dynamic.partition=true; 
set hive.exec.dynamic.partition.mode=nonstrict;
SET hive.exec.max.dynamic.partitions=1000;
SET hive.exec.max.dynamic.partitions.pernode=1000;

INSERT OVERWRITE TABLE weather_data_partitioned PARTITION(cityname)
SELECT datetime,temp_K,pressure,humidity_percent,
windspeed_mps,cloudiness_percent,cityname from weather_data_parquet;



