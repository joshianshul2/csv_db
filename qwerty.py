from sqlalchemy import create_engine
import psycopg2 
import io
import pandas as pds

engine = create_engine('postgresql+psycopg2://LandScrap:w87zhetrhgxdvo21@db-postgresql-nyc3-22046-do-user-8994632-0.b.db.ondigitalocean.com:25060/LandScrap', pool_recycle=3600);

# df =("SELECT state,county, SUM(price)/SUM(acres) AS NETPRICE FROM core_propertymaster GROUP BY state,county  limit 40",dbConnection)

# dataFrame.head(0).to_sql('core_avgmaster', engine, if_exists='replace',index=False) #drops old table and creates new empty table
dataFrame  = pds.read_sql("select * from \"core_avgmaster\"", engine);

conn = engine.raw_connection()
cur = conn.cursor()
output = io.StringIO()
dataFrame.drop_duplicates()
dataFrame.to_csv(output, sep='\t', header=False, index=False)
output.seek(0)
contents = output.getvalue()
cur.copy_from(output, 'core_avgmaster', null="") # null values become ''
conn.commit()
