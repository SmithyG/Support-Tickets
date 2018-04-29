import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)


# Definition of the connection object to connect to the postgreSQL database.


def getConn():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="Wetdog101")
    return conn


# Default route when web page is accessed and returns the home page.


@app.route('/', methods=['GET'])
def home():
    conn = None
    conn = getConn()
    cur = conn.cursor()
    cur.execute('SET search_path TO public')
    cur.execute('SELECT customerid FROM customer')
    customerRows = cur.fetchall()
    cur.execute('SELECT productid FROM product')
    productRows = cur.fetchall()
    cur.execute('SELECT ticketid FROM ticket')
    ticketRows = cur.fetchall()
    cur.execute('''SELECT ticketid FROM ticket WHERE (status='open') ORDER BY ticketid ASC''')
    openTicketRows = cur.fetchall()
    return render_template('home.html', customerList=customerRows, productList=productRows, ticketList=ticketRows,
                           openTicketList=openTicketRows)


# addCustomer is a function that controls the insertion of new customers into the database.


@app.route('/addCustomer', methods=['POST'])
def addCustomer():
    try:
        # Here the connection object is cleared to ensure no errors/mismatches,
        # this also clears any previous cursors attached.
        conn = None
        # Next we request the data to be inserted into the database from the form located on the home page.
        id = int(request.form['id'])
        name = request.form['name']
        email = request.form['email']
        # A new connection to the database is established and subsequently a new cursor is created.
        conn = getConn()
        cur = conn.cursor()
        cur.execute('SET search_path TO public')

        # The statement is prepared and the values earlier requested from the form are substituted in.
        cur.execute('INSERT INTO customer VALUES (%s,%s,%s)', \
                    [id, name, email])
        conn.commit()
        return render_template('home.html', msg='Record Added')

    except Exception as e:
        # An exception is thrown if the statement fails and an error is displayed.
        return render_template('home.html', msg='Record NOT Added', error=e)

    finally:
        if conn:
            conn.close()


# The addTicket function that controls the insertion of a new ticket is defined here.


@app.route('/addTicket', methods=['POST'])
def addTicket():
    try:
        conn = None
        conn = getConn()
        cur = conn.cursor()
        cur.execute('SET search_path TO public')

        ticketID = int(request.form['ticketid'])
        problem = request.form['problem']
        priority = request.form['priority']
        customerID = int(request.form['customerid'])
        productID = int(request.form['productid'])

        # The current_timestamp (date/time value) is used in the statement to log the time that the ticket was added.
        cur.execute('INSERT INTO ticket VALUES (%s,%s,DEFAULT,%s,CURRENT_TIMESTAMP ,%s,%s)', \
                    [ticketID, problem, priority, customerID, productID])
        cur.execute('SELECT * FROM ticket WHERE ticketid = %s', [ticketID])
        rows = cur.fetchall()
        conn.commit()
        # The inserted ticket is then displayed on the insertedTicket page.
        return render_template('insertedTicket.html', insertedTicket=rows, msg2='Record Added')

    except Exception as e:
        return render_template('insertedTicket.html', msg2='Record NOT Added', error2=e)

    finally:
        if conn:
            conn.close()


# The addUpdate function controls the insertion of ticket updates.


@app.route('/addUpdate', methods=['POST'])
def addUpdate():
    try:
        conn = None
        updateID = int(request.form['updateid'])
        message = request.form['message']
        ticketID = int(request.form['ticketid'])
        staffID = int(request.form['staffid'])

        conn = getConn()
        cur = conn.cursor()
        cur.execute('SET search_path TO public')

        # Again here we use the CURRENT_TIMESTAMP value to log the time of the ticket update.
        cur.execute('INSERT INTO ticketupdate VALUES (%s,%s,CURRENT_TIMESTAMP,%s,%s)', \
                    [updateID, message, ticketID, staffID])
        conn.commit()
        return render_template('home.html', msg3='Record Added')

    except Exception as e:
        return render_template('home.html', msg3='Record NOT Added', error3=e)

    finally:
        if conn:
            conn.close()


# getOutStandingTickets is a function that displays open tickets in the database on the web page.


@app.route('/listOutstandingTickets', methods=['GET'])
def getOutstandingTickets():
    try:
        conn = None
        conn = getConn()
        cur = conn.cursor()
        cur.execute('SET search_path TO public')

        cur.execute('''SELECT DISTINCT ON (t.ticketid) t.ticketid, t.productid, t.problem, t.status, t.priority, t.loggedtime,
        tU.updatetime FROM ticket t LEFT JOIN ticketupdate tU ON (t.ticketid = tU.ticketid) WHERE (t.status = 'open');''')
        rows = cur.fetchall()
        conn.commit()
        return render_template('outstandingTickets.html', outstandingtickets=rows)

    except Exception as e:
        return render_template('outstandingTickets.html', error4=e)

    finally:
        if conn:
            conn.close()


# The closeTicket function allows for a selected ticket's status to be set to closed.


@app.route('/closeTicket', methods=['POST'])
def closeTicket():
    try:
        conn = None
        ticketID = int(request.form['ticketid'])
        conn = getConn()
        cur = conn.cursor()
        cur.execute('SET search_path TO public')

        cur.execute("UPDATE ticket SET status='closed' WHERE (ticketid=%s)", [ticketID])
        conn.commit()
        return render_template('home.html', msg4='Record Updated')

    except Exception as e:
        return render_template('home.html', msg4='Record NOT Updated', error5=e)

    finally:
        if conn:
            conn.close()


# Given a ticket ID, the listUpdates function will show all updates on a ticket in chronological order.


@app.route('/listUpdates', methods=['POST'])
def listUpdates():
    try:
        conn = None
        ticketID = int(request.form['ticketid'])
        conn = getConn()
        cur = conn.cursor()
        cur.execute('SET search_path TO public')

        cur.execute('''SELECT
        t.problem,
        tU.message,
        tU.updatetime,
        s.name
        FROM ticket t
        INNER JOIN ticketupdate tU ON t.ticketid = tU.ticketid
        INNER JOIN staff s ON tU.staffid = s.staffid
        WHERE (t.ticketid = %s)
        ORDER BY t.ticketid, tU.updatetime;''', [ticketID])
        rows = cur.fetchall()
        conn.commit()
        return render_template('ticketAndUpdates.html', ticketandupdates=rows)

    except Exception as e:
        return render_template('ticketAndUpdates.html', error6=e)

    finally:
        if conn:
            conn.close()


# getClosedTickets is a function that lists all closed tickets along with the first response time,
# as well as the total time elapsed until the ticket was closed.


@app.route('/listClosedTickets', methods=['GET'])
def getClosedTickets():
    try:
        conn = None
        conn = getConn()
        cur = conn.cursor()
        cur.execute('SET search_path TO public')

        cur.execute('''SELECT
        t.ticketid,
        t.status,
        COUNT(tU.ticketid)                AS Number_Of_Updates,
        MIN(tU.updatetime) - t.loggedtime AS First_Response_Time,
        MAX(tU.updatetime) - t.loggedtime AS Total_Time_Elapsed
        FROM ticketupdate tU FULL OUTER JOIN ticket t on tU.ticketid = t.ticketid
        WHERE t.status = 'closed'
        GROUP BY tU.ticketid, t.ticketid, t.loggedtime
        ORDER BY t.ticketid;''')
        rows = cur.fetchall()
        conn.commit()
        return render_template('closedTickets.html', closedtickets=rows)

    except Exception as e:
        return render_template('closedTickets.html', error7=e)

    finally:
        if conn:
            conn.close()


# The deleteCustomer function allows the user to delete a customer from the database when a ticket ID is provided.
# However, if the customer has any associated support tickets then an error will be thrown and the record will not
# be deleted.


@app.route('/deleteCustomer', methods=['POST'])
def deleteCustomer():
    try:
        conn = None
        customerID = int(request.form['customerid'])
        conn = getConn()
        cur = conn.cursor()
        cur.execute('SET search_path TO public')

        cur.execute('''DELETE FROM customer
        WHERE customerid = %s;''', [customerID])
        conn.commit()
        return render_template('home.html', msg5='Record Deleted')

    except Exception as e:
        return render_template('home.html', msg5='Record NOT Deleted', error8=e)

    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    app.run(debug=True)
