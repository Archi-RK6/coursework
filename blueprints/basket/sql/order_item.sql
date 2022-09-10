SELECT ticket_id, session_number_t, title, m_id, session_date, hall_name, avarage_ticket_price, seat_row, seat_number
FROM tickets JOIN sessions ON(session_number_t = session_number) JOIN movies USING(m_id) JOIN cinema USING(hall_number)
WHERE 1 AND ticket_id = '$ticket_id' ;
