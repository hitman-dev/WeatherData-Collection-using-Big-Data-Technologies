from pyspark.sql import SparkSession
import unidecode

spark = SparkSession.builder.master('local').appName('DataInject').getOrCreate()

print("======================================== Reading Raw data from dq_good =========================================")
weather_df = spark.read.csv('hdfs://localhost:9000/miniproject/raw/dq_good/data.csv',header=True,inferSchema=True)


print("==================Transliterating an Unicode object into an ASCII string in Cityname column=====================")
cols = ['cityname','datetime','temp_K','pressure','humidity_percent','windspeed_mps','cloudiness_percent']
weather_df = weather_df.select(*cols).toPandas()
weather_df['cityname'] = weather_df['cityname'].apply(lambda x: unidecode.unidecode(x))
weather_df = spark.createDataFrame(weather_df)

print("====================== Saving the Dataframe in Parquet format in append mode in persist folder =================")
weather_df.write.parquet("hdfs://localhost:9000/miniproject/raw/persist/date.parquet",mode='append')
print("=================================================================================================================")