select
    strftime('%m', FL_DATE) as 'month', 
    strftime('%w', FL_DATE) as day_of_week, 
    OP_CARRIER as airline, 
    origin,
    dest,
    count(*) as num_of_flights,
    avg(arr_delay) as avg_delay
from
    airline_2009
group by
    strftime('%m', FL_DATE), 
    strftime('%w', FL_DATE), 
    OP_CARRIER, 
    origin, 
    dest