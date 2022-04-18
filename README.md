## The purpose of this assessment are:

* Using Docker to pack Python scripts for further CI/CD
* Using Docker compose to make the scripts working with Postgres DB and other tools
* The scripts will pull and store data from the fs
* Using Jupyter notebooks for analysis and visuaollowing APIs
  * [The World Bank Country API](https://datahelpdesk.worldbank.org/knowledgebase/articles/898590-country-api-queries)
  * [Restcountries.com all countries API](https://restcountries.com/#api-endpoints-v3-all)
* Creating views to verify that both data sourcelization


## File structure
![File structure](Screenshot%20from%202022-04-18%2017-05-30.png)


## Run Docker Compose
```shell
docker-compose up
```
The docker will build docker images of hte python code and start services of the following tools:
(the login info is configured in docker-compose.yml file)

* [pgAdmin](http://localhost:5050/browser/)
* [Jupyter Notebook](http://localhost:8888/lab?token=jupyter)

## Build DB view using API
Using browser to visit http://localhost:5000/buildview, that will 
* extract data from worldbank and restcountries
* save raw data into DB tables (rest_country_raw & world_country_raw)
* normalize and the data 
* upload the data into DB tables (rest_country & world_country)
* build DB view “country_info” with inner joined those 2 DB tables  (create_views.sql)
* create a role “analyst”  (create_user.sql)
* create a user “analyst_team” as an analyst role  

## Work with DB view 
There are some example code at country_example.py and region.ipynb

![visualization](Screenshot%20from%202022-04-18%2016-52-36.png)