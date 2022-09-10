SELECT session_number, session_date, hall_name
FROM sessions join cinema using(hall_number)
WHERE m_id = '$m_id' AND session_date = CURDATE();