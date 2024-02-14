# sql.py
query_trip_data = """
-- Weekly Saturday Metric
WITH Sat_metrics AS 
(
select
 pickup_date sat_date,
 count(1) sat_trip_count,
 avg(fare_amount) sat_mean_fare_per_trip,
avg(timediff(pickup_datetime, dropoff_datetime)) sat_mean_duration_per_trip
 from tripdata 
 where pickup_date between '2014-01-01' and '2016-12-31' --(Specified date range from exercise)
and dayofweek(pickup_date) = 6 -- (Filtering for Saturday Metric)
group by pickup_date
),

-- Weekly Sunday Metric
Sun_metrics AS
(
select
pickup_date sun_date,
 count(1) sun_trip_count,
 avg(fare_amount) sun_mean_fare_per_trip,
avg(timediff(pickup_datetime, dropoff_datetime)) sun_mean_duration_per_trip
 from tripdata 
 where pickup_date between '2014-01-01' and '2016-12-31' --(Specified date range from exercise)
and dayofweek(pickup_date) = 7 --- (Filtering for Sunday Metric)
group by pickup_date
),

-- Monthly Saturday Metric
Sat_monthly_metrics AS
(
select
  DATE_FORMAT(sat_date, '%Y-%m') month,
 round(avg(sat_trip_count),1) sat_mean_trip_count,
 round(avg(sat_mean_fare_per_trip),1) sat_mean_fare_per_trip,
round(avg(sat_mean_duration_per_trip),1) sat_mean_duration_per_trip
 from Sat_metrics 
group by DATE_FORMAT(sat_date, '%Y-%m') 
),

-- Monthly Sunday Metric
Sun_monthly_metrics AS
(
select
  DATE_FORMAT(sun_date, '%Y-%m') month,
 round(avg(sun_trip_count),1) sun_mean_trip_count,
 round(avg(sun_mean_fare_per_trip),1) sun_mean_fare_per_trip,
round(avg(sun_mean_duration_per_trip),1) sun_mean_duration_per_trip
 from Sun_metrics 
group by DATE_FORMAT(sun_date, '%Y-%m') 
order by DATE_FORMAT(sun_date, '%Y-%m') 
)

select 
IFNULL(a.month, b.month) month,
sat_mean_trip_count,
sat_mean_fare_per_trip,
sat_mean_duration_per_trip,
sun_mean_trip_count,
sun_mean_fare_per_trip,
sun_mean_duration_per_trip
from Sat_monthly_metrics a full outer join Sun_monthly_metrics b
on a.month = b.month
"""