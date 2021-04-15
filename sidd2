from sqlalchemy import create_engine
import psycopg2
import io
import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd
#
# engine = create_engine('postgresql+psycopg2://LandScrap:w87zhetrhgxdvo21@db-postgresql-nyc3-22046-do-user-8994632-0.b.db.ondigitalocean.com:25060/LandScrap', pool_recycle=3600);
#
# dbConnection =engine.connect();

MyList = []
ChunkSize = 200
for i in pd.read_csv("core/rishuuu.csv",chunksize=ChunkSize) :
    MyList.append(i)

# What we done [df1,df2,df2.....chunksize]
print(MyList)
# 200 * 11
print(len(MyList))
# 25 bcz we divide into chunks i.e 200(chunks or data batchs) * 25(dfs) = 500 Records

df = pd.read_csv("core/rishuuu.csv")
print(df.shape)

# Combinig Chunks and convert into data frame

df1 = pd.concat(MyList,axis=0)
print("Rishu")
print(df1.shape)
print("Anji")
print(df1)
