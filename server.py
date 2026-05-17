from fastmcp import FastMCP
import sqlite3
import json
from pathlib import Path
import database

mcp = FastMCP("Expense Tracker")
database.init_db()

CATEGORIES_PATH = Path(__file__).parent / "categories.json"
with open(CATEGORIES_PATH) as f:
    CATEGORIES = json.load(f)

##create the tool for add expenses

@mcp.tool()
def add_expenses(date, amount, description, category, sub_category="", comments=""):
    '''Add a new expense entry to the database.
    Based on the description, intelligently pick category and sub_category from this list:
    ''' + json.dumps(CATEGORIES) + '''
    Always choose the most specific sub_category that matches the expense description.'''

    with sqlite3.connect(database.DB_PATH) as c:
        curr = c.execute(
            "INSERT INTO expenses(date, amount, category, sub_category, comments) VALUES (?,?,?,?,?)",
            (date, amount, category, sub_category, comments or description)
        )
        return {"status": "ok", "id": curr.lastrowid, "category": category, "sub_category": sub_category}

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