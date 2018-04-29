/*Produce a report showing the status of each closed support ticket. For each ticket you should
include the number of updates, the time that elapsed between the question being logged and the first
update, and the time between the question being logged and the final update. You may assume that
all closed tickets have at least one update from a member of staff. */
SELECT
  t.ticketid,
  t.status,
  COUNT(tU.ticketid)                AS Number_Of_Updates,
  MIN(tU.updatetime) - t.loggedtime AS First_Response_Time,
  MAX(tU.updatetime) - t.loggedtime AS Total_Time_Elapsed
FROM ticketupdate tU FULL OUTER JOIN ticket t on tU.ticketid = t.ticketid
WHERE t.status = 'closed'
GROUP BY tU.ticketid, t.ticketid, t.loggedtime
ORDER BY t.ticketid;
