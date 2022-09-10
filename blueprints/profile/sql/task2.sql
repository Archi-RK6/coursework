select title, session_date, (number_of_tickets_sold * avarage_ticket_price)
from movies join sessions
using (m_id)
join cinema
using (hall_number)
where month(session_date) = '$month' and year(session_date) = '$year'
group by title, session_date;