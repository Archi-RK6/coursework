select title,count(session_number), sum(number_of_tickets_sold) 
from sessions join movies 
using (m_id) 
where month(session_date) = '$month' and year(session_date) =  '$year'
group by title;