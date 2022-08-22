# Convoy-data-export


In order to manage the data made by the convoys, 
a company decides to create a scoring system for the different cars making convoys. 
To do this, this program was developed to classify the cars according to their scores 
and send them in XML or JSON files according to their score.

## Data Structure
For each car, the following data is recorded:
- `vehicle_id`
- `engine_capacity`: The fuel storage capacity of the machine in liter
- `fuel_consumption`: The fuel consumption in liters per 100 km
- `maximum_load`: The maximum load supported by the vehicle in tons

## Scoring system
Cars travel on average **450km**. Therefore, for scoring purposes, we have considered this distance as the maximum distance. So the quotations for the score will be done as follows:
1. Number of stops at the refueling station (based on the capacity and consumption of the vehicle): If the vehicle makes more than two stops it has `0 points`, if it makes 1 stop it has `1 points` and if it makes no stops it will have `2 points`.
2. If the vehicle consumes more than 230 liters it has `1 points` and if not `2 points`.
3. The vehicle gets `2 points` if its load capacity is more than 20 tons and `0 points` otherwise
## Storage system
For each car if the score is higher than 3 we export it in a `JSON` file 
otherwise we send it in a `XML` file

## File type Supported
The program supports the following file types:
- `JSON`
- `XML`
- `CSV`
- `S3DB`
- `XLSX`  

For `CSV` and `XLSX` files, the program will remove all non digit characters from the file name.
