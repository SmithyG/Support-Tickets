DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE TABLE Staff
(
	StaffID			INTEGER PRIMARY KEY NOT NULL,
	Name			VARCHAR(40) NOT NULL CONSTRAINT staff_name_check CHECK (Name != '')
);

CREATE TABLE Product
(
	ProductID		INTEGER PRIMARY KEY NOT NULL,
	Name			VARCHAR(40) NOT NULL CONSTRAINT product_name_check CHECK (Name != '')
);

CREATE TABLE Customer
(
	CustomerID		INTEGER PRIMARY KEY NOT NULL,
	Name			VARCHAR(40) NOT NULL CONSTRAINT customer_name_check CHECK (Name != ''),
	Email			VARCHAR(40) NOT NULL UNIQUE CONSTRAINT email_check CHECK (Email != '')
);

CREATE TABLE Ticket
(
	TicketID		INTEGER PRIMARY KEY NOT NULL,
	Problem			VARCHAR(1000) NOT NULL CONSTRAINT problem_check CHECK (Problem != ''),
	Status			VARCHAR(20) NOT NULL DEFAULT('open') CONSTRAINT status_check CHECK (Status = 'open' OR Status = 'closed'),
	Priority		INTEGER NOT NULL CONSTRAINT priority_check CHECK (Priority >=1 AND Priority <=3),
	LoggedTime		TIMESTAMP NOT NULL,
	CustomerID		INTEGER REFERENCES Customer (CustomerID) ON DELETE RESTRICT ON UPDATE RESTRICT NOT NULL,
	ProductID		INTEGER REFERENCES Product (ProductID) ON DELETE RESTRICT ON UPDATE RESTRICT NOT NULL
);

CREATE TABLE TicketUpdate
(
	TicketUpdateID	INTEGER PRIMARY KEY NOT NULL,
	Message			VARCHAR(1000) NOT NULL CONSTRAINT message_check CHECK (Message != ''),
	UpdateTime		TIMESTAMP NOT NULL,
	TicketID		INTEGER REFERENCES Ticket (TicketID) ON DELETE CASCADE ON UPDATE RESTRICT NOT NULL,
	StaffID			INTEGER REFERENCES Staff (StaffID) ON DELETE RESTRICT ON UPDATE RESTRICT
);

CREATE INDEX ticket_open_index ON ticket (Status);

CREATE VIEW Closed_Ticket_Report AS SELECT
  t.ticketid,
  t.status,
  COUNT(tU.ticketid)                AS Number_Of_Updates,
  MIN(tU.updatetime) - t.loggedtime AS First_Response_Time,
  MAX(tU.updatetime) - t.loggedtime AS Total_Time_Elapsed
FROM ticketupdate tU FULL OUTER JOIN ticket t on tU.ticketid = t.ticketid
WHERE t.status = 'closed'
GROUP BY tU.ticketid, t.ticketid, t.loggedtime
ORDER BY t.ticketid;