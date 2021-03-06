import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('weather ETL').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.4' # make sure we have Spark 2.4+

observation_schema = types.StructType([
    types.StructField('station', types.StringType()),
    types.StructField('date', types.StringType()),
    types.StructField('observation', types.StringType()),
    types.StructField('value', types.IntegerType()),
    types.StructField('mflag', types.StringType()),
    types.StructField('qflag', types.StringType()),
    types.StructField('sflag', types.StringType()),
    types.StructField('obstime', types.StringType()),
])


def main(in_directory, out_directory):

    weather = spark.read.csv(in_directory, schema=observation_schema)

    print(weather)
    # TODO: finish here.
    cleaned_data= weather.filter(weather.qflag.isNull())
    cleaned_data= cleaned_data.filter(cleaned_data.station.startswith('CA'))
    cleaned_data= cleaned_data.filter(cleaned_data.observation.startswith('TMAX'))
    cleaned_data = cleaned_data.withColumn('tmax', cleaned_data['value'] / 10)
    cleaned_data= cleaned_data.select("station","date","tmax")
    # cleaned_data=  types.StructType([
    #     types.StructField('qflag',weather.filter(weather.qflag.isNull()), types.StringType()),
    #     types.StructField('station',weather.filter(weather.station.startswith('CA')) ,types.StringType()),
    #     types.StructField('observation',weather.filter(weather.observation.startswith('TMAX')), types.StringType()),
    # ])



    # =weather.filter(weather.station.startswith('CA')).collect()
    # print(weather)

    cleaned_data.write.json(out_directory, compression='gzip', mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
