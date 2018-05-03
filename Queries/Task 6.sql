SELECT
  t.problem,
  tU.message,
  tU.updatetime,
  s.name
FROM ticket t
  FULL OUTER JOIN ticketupdate tU ON t.ticketid = tU.ticketid
  FULL OUTER JOIN staff s ON tU.staffid = s.staffid
WHERE (t.ticketid = 25)
ORDER BY t.ticketid, tU.updatetime;