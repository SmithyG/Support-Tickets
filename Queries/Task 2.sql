INSERT INTO ticket
VALUES (31, 'Damaged components', 'open', 2, current_timestamp, 2, 3);
SELECT *
FROM ticket
WHERE (TicketID = 31);