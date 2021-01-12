select round(avg(overall_rating),2), round(avg(rooms_rating),2),round(avg(service_rating),2), 
round(avg(location_rating),2), round(avg(value_rating),2)
from repatronage_review_assignment
where user_id in  
(select user_id from
(select hotel_id, user_id, count(review_date)
from repatronage_review_assignment
group by user_id, hotel_id
having count(review_date) > 1) as a)
and review_date in
(select review_date from 
(select user_id, review_date, dense_rank()
over(partition by user_id order by review_date) r 
from repatronage_review_assignment) as b
where r=1);