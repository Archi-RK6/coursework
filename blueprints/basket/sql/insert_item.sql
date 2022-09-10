UPDATE movies, sessions, tickets
SET movies.revenue = movies.revenue + '$revenue',
    movies.date_rev = CURDATE(),
    sessions.number_of_tickets_sold = sessions.number_of_tickets_sold + 1,
    tickets.availability = 'occupied'
WHERE sessions.session_number = '$session_number' AND movies.title = '$title' AND movies.m_id = sessions.m_id AND tickets.ticket_id ='$ticket_id';