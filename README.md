# Logistics Datawarehouse
Provides the creation of a datawarehouse and the extraction of sample a CSV file to populate it. <br>
The result is a self-service data-analysis to slice and dice freely combining different dimensions. <br>
A visualization of the data can be found in this dashboard: https://public.tableau.com/profile/gabriel3199#!/vizhome/logistics-datawarehouse/Dashboard1


1 - [Get started](#Get-Started)

2 - [The model](#The-Model)

3 - [Visualizing](#Visualizing)

4 - [Automation and the cloud](#Automation)

## Get Started
First, clone this project and cd onto it.
### Docker
Simply run in a CLI tool: (No need to sudo in Windows)
```
sudo docker build -t logistics-datawarehouse .
sudo docker-compose up --renew-anon-volumes
```
And the data is loaded. <br>
You can connect to the database using your favorite tool using this information:
```
host: localhost
port: 3306
database: logistics
user: root
password: password
```

### Manual

First you should have a MySQL instance and python 3.8+. <br>
Then, the easiest way to run the project is: <br>
1 - Create the database using the script at /scripts/create_database.sql <br>
2 - Install the requirements using pip <br>
    `pip install -r requirements.txt` <br>
3 - Export the environment variables to access the MySQL instance <br>
```
export DWH_HOST=localhost
export DWH_USER=root
export DWH_PASSWORD=password
export DWH_DATABASE=logistics
```
They are, respectively, the host, the user and password to access and the database name. 
If you're on a Windows CLI, change export to `set`. <br>
4 - Populate the database <br>
    `python populate.py` <br>
    
### Happy analysis!
```sql
SELECT  ld.city_pair, COUNT(*) as delays FROM truck_run_f
INNER JOIN lane_d ld on truck_run_f.lane_key = ld.lane_key
INNER JOIN on_time_d otd on truck_run_f.on_time_key = otd.on_time_key
where otd.delivery_indicator='Carrier Not On Time To Delivery'
GROUP BY ld.city_pair
ORDER BY delays DESC
``` 
The above query gets the most delayed to delivery routes.
  
## The Model
![alt text](./img/diagram.png)
The idea of the model is to model the process of contracting a truck to carry your shipment. We want to be able to analyze at the level of individual events.
It's meant to be a simple star schema to model the fact `truck_run`. The measures are the
book price, source price and profit. All the other variables present in the original data are transformed
to dimensions.
The quote, book, pickup, delivery and appointments are roleplayed to the dimensions date and time. Date and time are
split into different dimensions. <br>
The lane dimension holds both the origin and destination. The mileage is also put in this dimension because analyzing
the data we saw that it only differs between different lanes. <br>
Equipment and sourcing are two normal predictable dimensions, populated before the ETL. <br>
Shipper and carrier are also normal dimensions but populated in the ETL to map new or existing entities. <br>
The Load, On Time and Tracking are junk dimensions to map boolean values. They have finite possibilities but are only populated when needed.
The tracking, for example, has only one possible combination, which is all False.

Using this modeling we can get valuable information about how the metrics change slicing and dicing as many dimension we may want.

## Visualizing
The below dashboard can be fulled analyzed interactively at: https://public.tableau.com/profile/gabriel3199#!/vizhome/logistics-datawarehouse/Dashboard1 
![alt text](./img/dashboard.png)
The scatter in the middle changes its color based on the profit, and its size on the mileage. <br> The points in
the maps also respects this rule. <br> 
We see a clear relationship between book x source's price and the profit. <br>
The filters in the right gives the ability to slice and dice the data, we can change the month, see cancelled loads, automations,
filter by delays, equipment type and source channel. <br>
Filtering the date we can know: if we see more blues we are getting the most profitable runs.
The model is very versatile and can be combined/visualized in different ways to get more insights. There are numerous possibilities.
 
## Automation
![alt text](./img/cloud.png)

We can automate this process in a production environment tweaking the data source to put in S3, which triggers lambda to run this script.
The only alteration needed would be to create a handler to download the data from S3 and call src/core/load.py with it. Using
Redshift is optional but it's nice to automate via IaC the environment. <br>
We can also instead of triggering lambda in every new put on S3, use CloudWatch Events to bulk load everyday or week.