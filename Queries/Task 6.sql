SELECT
  t.problem,
  tU.message,
  tU.updatetime,
  s.name
FROM ticket t
  INNER JOIN ticketupdate tU ON t.ticketid = tU.ticketid
  INNER JOIN staff s ON tU.staffid = s.staffid
WHERE (t.ticketid = 101)
ORDER BY t.ticketid, tU.updatetime;