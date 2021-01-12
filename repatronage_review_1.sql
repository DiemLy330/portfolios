select f.hotel_id, f.user_id, round(avg(datediff(s.second_lodging, f.first_lodging)),0)
from
(select user_id, hotel_id, min(review_date) as first_lodging
from repatronage_review_assignment
where user_id in  
(select user_id from
(select hotel_id, user_id, count(review_date)
from repatronage_review_assignment
group by user_id, hotel_id
having count(review_date) > 1) as a)
group by user_id, hotel_id) as f
join
(select user_id, review_date as second_lodging
from 
(select user_id, review_date, dense_rank()
over(partition by user_id order by review_date) r 
from repatronage_review_assignment) as b
where r=2) as s 
on s.user_id = f.user_id
group by hotel_id;