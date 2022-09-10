SELECT ticket_id, session_number, title, session_date, hall_name, avarage_ticket_price, seat_row, seat_number
FROM tickets JOIN sessions ON(session_number_t = session_number) JOIN movies USING(m_id) JOIN cinema USING(hall_number)
WHERE m_id = '$m_id' and session_number = '$session_number' and availability = 'free';