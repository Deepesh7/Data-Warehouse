# Project Datawarehouse

### Project Description

Sparkify is a music streaming startup. Their data resides in S3, in a directory of JSON logs. Sparkify wants to move their processes and data onto the cloud. The task is to build an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analysis. 

### How to Run
#### Step 1: To run this project you will need to fill the following information, and save it as _dwh.cfg_ in the project root folder.

    [CLUSTER]
    HOST = 
    DB_NAME = 
    DB_USER = 
    DB_PASSWORD = 
    DB_PORT = 5439
    CLUSTER_TYPE = multi-node
    NUM_NODES = 4
    NODE_TYPE = dc2.large
    CLUSTER_IDENTIFIER = 
    
    [IAM_ROLE]
    ARN = 
    
    [AWS]
    KEY = 
    SECRET = 
    
    [S3]
    LOG_DATA = 's3://udacity-dend/log_data'
    LOG_JSONPATH = 's3://udacity-dend/log_json_path.json'
    SONG_DATA = 's3://udacity-dend/song_data'
    
    [DWH]
    DWH_IAM_ROLE_NAME = 

#### STEP 2: Follow the instruction and execute the Initial_config.ipynb python file.

#### STEP 3: Run create_tables.py  script to create the tables.

    $python3 create_tables.py

#### STEP 4: Run etl.py script to extract data from S3 stage it in redshift and store it in dimensional table.

    $python3 etl.py

### Project Structure
The project includes following files:

- initial_config.ipynb: This includes detailed steps and code to initialize the cluster architecture.
- create_tables.py: The script creates the staging tables and the fact and dimension tables in the database.
- etl.py: The script ectracts the data from S3 bucket stages them in redshift and transforms and loads into dimensional and fact tables.
- sql_queries.py: The script includes all the queries required to create the tables and perform etl process on it.
- dwh.cfg: This include all the cluster configurations details.
- README.md: current file, follow this to understand the project.

### Database Schema
**Staging Tables**
- staging_events
- staging_songs

**Dimensional Tables**
- users
	user_id int PRIMARY KEY : ID of user
	first_name text : user's first name
	last_name text : user's last name
	gender text : user's gender
	level text : paid level or free level

- songs 
	song_id text PRiMARY KEY : ID of song
	title text : title of song
	artist_id text : ID of artist of the song
	year int : Year of song release
	duration float : Song duration in milliseconds

- artists
	artist_id text PRIMARY KEY : ID of artist
	name text : Name of artist
	location text : Location of artist
	latitude decimal : Latitude location of artist
	longitude decimal : Longitude location of artist

- time
	start_time timestamp PRIMARY KEY : start time (timestamp) of user 	activity
	hour int : Hour extracted from timestamp
	day int : Day extracted from timestamp
	week int : Week extracted from timestamp
	month int : Month extracted from timestamp
	year int : Year extracted from timestamp
	weekday text : Weekday extracted from timestamp

**Fact Tables**
- songplays: records in log data associated with song plays i.e. records with page NextSong

	songplay_id int PRIMARY KEY : ID for each songplay record
	start_time timestamp NOT NULL : start time (timestamp) of user activity
	user_id int NOT NULL : ID of user 
	level text : paid level or free level
	song_id text : ID of song
	artist_id text : ID of artist
	session_id text : ID of user session
	location text : User location
	user_agent text : Agent used by the user to access Sparkify Platform.

### Results
After completing the etl processes, the number of rows in each tables are: 
- staging_events: 8056
- staging_songs: 14896
- users: 105
- songs: 14896
- artists: 10025
- time: 8023
- songplays: 333

### Steps followed on this project

1. Create Table Schemas

- Design the fact and dimension tables in your star schema.
- Write SQL CREATE statements for each of these tables in sql_queries.py
- Create an IAM role that has read access to S3.
- Create an Redshift Cluster using Initial_congif.ipynb notebook. 
- Update the value for cluster endpoint in dwh.cfg file.
- Create a connection to the database and run the create_tables.py script to create all the tables.
- Write the SQL DROP statements in the sql_queries.py file. The create_tables.py first drops the tables if it exists and the creates the tables again. This way you start afresh whenever you run create_tables.py script.
- Test by running the create_tables.py and checking the tables schemas in your redshift database. You can use Query Editor in the AWS Redshift console for this.

2. Build ETL pipeline

- Implement the logic in etl.py to extract data from S3 and load data into staging tables on Redshift.
- Implement the logic in etl.py to transform and load data into dimensional and fact tables.
- Test by running create_tables.py and the etl.py and use SQL select queries on the Query Editor to test the result.
- Delete the Redshift cluster when you are done by following the steps in Initial_config.ipynb notebook.








