from fastmcp import FastMCP
import os
import sqlite3
import database

mcp = FastMCP("Expense Tracker")
database.init_db()

##create the tool for add expenses

@mcp.tool()
def add_expenses(date,amount,category, subCategory="", comments=""):
    '''Add a new expense entry to the database'''
    with sqlite3.connect(database.DB_PATH) as c:
        curr = c.execute(
            "INSERT INTO expenses(date, amount, category, sub_category, comments) VALUES (?,?,?,?,?)",
            (date, amount, category, subCategory, comments)
        )
        return {"status": "ok", "id":curr.lastrowid}

##Read the existing expenses
@mcp.tool()
def list_expenses(startDate, endDate):
    '''List the expense entries within the exclusive date Range'''
    with sqlite3.connect(database.DB_PATH) as c:
        curr = c.execute(
            "SELECT * from expenses " \
            "WHERE date BETWEEN ? AND ?" \
            " ORDER BY expense_id ASC",
            (startDate, endDate)
        )
        cols = [d[0] for d in curr.description]
        return [dict(zip(cols,r)) for r in curr.fetchall()]

if __name__ == "__main__":
    mcp.run()