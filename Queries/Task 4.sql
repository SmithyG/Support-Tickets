SELECT
  DISTINCT ON (t.ticketid) t.ticketid,
  t.productid,
  t.problem,
  t.status,
  t.priority,
  t.loggedtime,
  tU.updatetime
FROM ticket t
  LEFT JOIN ticketupdate tU ON (t.ticketid = tU.ticketid)
WHERE (t.status = 'open');