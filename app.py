
from flask import Flask, request, redirect
import sqlite3
import os
from html import escape

app = Flask(__name__)

DATABASE = os.path.join(app.root_path, "ecolink.db")


# Connect to the SQLite database
def connect_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# Create the items table if it does not exist
def create_table():
    connection = connect_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            condition TEXT NOT NULL,
            area TEXT NOT NULL,
            description TEXT
        )
    """)
    connection.execute("""
	CREATE TABLE IF NOT EXISTS requests (
	    id INTEGER PRIMARY KEY AUTOINCREMENT,
	    item_id INTEGER NOT NULL,
	    requester_name TEXT NOT NULL,
	    message TEXT,
	    status TEXT NOT NULL DEFAULT 'Pending',
	    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	    FOREIGN KEY (item_id) REFERENCES items(id)
	 )
     """)    
    connection.commit()
    connection.close()


# Main page

@app.route("/request/<int:item_id>", methods=["GET", "POST"])
def request_item(item_id):
    connection = connect_db()

    item = connection.execute(
        "SELECT * FROM items WHERE id = ?", (item_id,)
    ).fetchone()

    if item is None:
        connection.close()
        return "Item not found.", 404

    if request.method == "POST":
        requester_name = request.form.get(
            "requester_name", ""
        ).strip()

        message = request.form.get("message", "").strip()

        if not requester_name or len(requester_name) > 100:
            connection.close()
            return "Please enter a name (maximum 100 characters).", 400

        if len(message) > 500:
            connection.close()
            return "Message must be 500 characters or fewer.", 400

        connection.execute("""
            INSERT INTO requests
            (item_id, requester_name, message)
            VALUES (?, ?, ?)
        """, (item_id, requester_name, message))

        connection.commit()
        connection.close()

        return """
        <html>
        <head><title>Request Submitted</title></head>
        <body style="font-family:Arial; background:#f2f8f1;
                     padding:40px; text-align:center; animation: ecoPageEnter 650ms ease-out both;">
            <h2 style="color:#246b45;">Request submitted!</h2>
            <p>Your item request has been saved.</p>
            <a href="/">Return to EcoLink</a>
        </body>
        </html>
        """

    connection.close()

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">
        <title>Request Item - EcoLink</title>
        <style>

            /* EcoLink visual polish: animations only; existing features stay unchanged */
            html {{ scroll-behavior: smooth; }}
            body {{ animation: ecoPageEnter 650ms ease-out both; }}
            header {{ animation: ecoHeaderEnter 700ms cubic-bezier(.2,.8,.2,1) both; }}
            main {{ animation: ecoContentEnter 700ms ease-out 80ms both; }}
            .card, .stat-card, form {{
                transition: transform 240ms ease, box-shadow 240ms ease, border-color 240ms ease;
                animation: ecoCardEnter 520ms ease-out both;
            }}
            .card:hover, .stat-card:hover {{
                transform: translateY(-4px);
                box-shadow: 0 10px 24px rgba(36, 107, 69, 0.13);
            }}
            button {{ transition: transform 180ms ease, background-color 180ms ease, box-shadow 180ms ease; }}
            button:hover {{ transform: translateY(-2px); box-shadow: 0 5px 12px rgba(36, 107, 69, 0.18); }}
            button:active {{ transform: translateY(0) scale(.98); }}
            a {{ transition: color 180ms ease, opacity 180ms ease; }}
            a:hover {{ opacity: .82; }}
            input, select, textarea {{ transition: border-color 180ms ease, box-shadow 180ms ease; }}
            input:focus, select:focus, textarea:focus {{
                outline: none;
                border-color: #70ad70;
                box-shadow: 0 0 0 3px rgba(112, 173, 112, .18);
            }}
            @keyframes ecoPageEnter {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            @keyframes ecoHeaderEnter {{
                from {{ opacity: 0; transform: translateY(-14px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            @keyframes ecoContentEnter {{
                from {{ opacity: 0; transform: translateY(12px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            @keyframes ecoCardEnter {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            @media (prefers-reduced-motion: reduce) {{
                html {{ scroll-behavior: auto; }}
                *, *::before, *::after {{
                    animation-duration: .01ms !important;
                    animation-iteration-count: 1 !important;
                    transition-duration: .01ms !important;
                    scroll-behavior: auto !important;
                }}
            }}

            body {{
                font-family: Arial, sans-serif;
                background: #f2f8f1;
                padding: 20px;
                color: #26382b;
            }}
            main {{
                max-width: 500px;
                margin: 30px auto;
                background: white;
                padding: 25px;
                border-radius: 10px;
            }}
            h2 {{ color: #246b45; }}
            label {{
                display: block;
                margin-top: 15px;
                font-weight: bold;
            }}
            input, textarea {{
                box-sizing: border-box;
                width: 100%;
                padding: 10px;
                margin-top: 6px;
                border: 1px solid #cbd8cb;
                border-radius: 5px;
            }}
            button {{
                margin-top: 18px;
                padding: 12px 18px;
                background: #246b45;
                color: white;
                border: 0;
                border-radius: 5px;
                cursor: pointer;
            }}
        </style>
    </head>
    <body>
        <main>
            <h2>Request: {escape(item['title'])}</h2>
            <p>Category: {escape(item['category'])}</p>

            <form method="POST">
                <label for="requester_name">Your name *</label>
                <input id="requester_name"
                       name="requester_name"
                       maxlength="100"
                       required>

                <label for="message">Message (optional)</label>
                <textarea id="message"
                          name="message"
                          maxlength="500"
                          rows="4"
                          placeholder="Why are you interested in this item?"></textarea>

                <button type="submit">Submit Request</button>
            </form>

            <p><a href="/">Cancel and return to EcoLink</a></p>
        </main>
    </body>
    </html>
    """

@app.route("/requests")
def view_requests():
    connection = connect_db()

    requests_list = connection.execute("""
        SELECT
            requests.id,
            requests.item_id,
            requests.requester_name,
            requests.message,
            requests.status,
            requests.created_at,
            items.title AS item_title
        FROM requests
        JOIN items ON requests.item_id = items.id
        ORDER BY requests.id DESC
    """).fetchall()

    connection.close()

    rows = ""

    for req in requests_list:
        rows += f"""
        <div class="card">
            <h3>{escape(req['item_title'])}</h3>
            <p><strong>Requester:</strong>
                {escape(req['requester_name'])}</p>
            <p><strong>Message:</strong>
                {escape(req['message'] or 'No message')}</p>
            <p><strong>Status:</strong>
                {escape(req['status'])}</p>
            <p><strong>Submitted:</strong>
                {escape(str(req['created_at']))}</p>

            <form method="POST"
                  action="/requests/{req['id']}/status">
                <label>Update status</label>
                <select name="status" required>
                    <option value="Pending"
                        {"selected" if req['status'] == 'Pending' else ""}>
                        Pending
                    </option>
                    <option value="Accepted"
                        {"selected" if req['status'] == 'Accepted' else ""}>
                        Accepted
                    </option>
                    <option value="Rejected"
                        {"selected" if req['status'] == 'Rejected' else ""}>
                        Rejected
                    </option>
                </select>
                <button type="submit">Save Status</button>
            </form>
        </div>
        """

    if not rows:
        rows = "<p>No requests have been submitted yet.</p>"

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">
        <title>EcoLink Requests</title>
        <style>

            /* EcoLink visual polish: animations only; existing features stay unchanged */
            html {{ scroll-behavior: smooth; }}
            body {{ animation: ecoPageEnter 650ms ease-out both; }}
            header {{ animation: ecoHeaderEnter 700ms cubic-bezier(.2,.8,.2,1) both; }}
            main {{ animation: ecoContentEnter 700ms ease-out 80ms both; }}
            .card, .stat-card, form {{
                transition: transform 240ms ease, box-shadow 240ms ease, border-color 240ms ease;
                animation: ecoCardEnter 520ms ease-out both;
            }}
            .card:hover, .stat-card:hover {{
                transform: translateY(-4px);
                box-shadow: 0 10px 24px rgba(36, 107, 69, 0.13);
            }}
            button {{ transition: transform 180ms ease, background-color 180ms ease, box-shadow 180ms ease; }}
            button:hover {{ transform: translateY(-2px); box-shadow: 0 5px 12px rgba(36, 107, 69, 0.18); }}
            button:active {{ transform: translateY(0) scale(.98); }}
            a {{ transition: color 180ms ease, opacity 180ms ease; }}
            a:hover {{ opacity: .82; }}
            input, select, textarea {{ transition: border-color 180ms ease, box-shadow 180ms ease; }}
            input:focus, select:focus, textarea:focus {{
                outline: none;
                border-color: #70ad70;
                box-shadow: 0 0 0 3px rgba(112, 173, 112, .18);
            }}
            @keyframes ecoPageEnter {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            @keyframes ecoHeaderEnter {{
                from {{ opacity: 0; transform: translateY(-14px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            @keyframes ecoContentEnter {{
                from {{ opacity: 0; transform: translateY(12px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            @keyframes ecoCardEnter {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            @media (prefers-reduced-motion: reduce) {{
                html {{ scroll-behavior: auto; }}
                *, *::before, *::after {{
                    animation-duration: .01ms !important;
                    animation-iteration-count: 1 !important;
                    transition-duration: .01ms !important;
                    scroll-behavior: auto !important;
                }}
            }}

            body {{
                font-family: Arial, sans-serif;
                background: #f2f8f1;
                color: #26382b;
                margin: 0;
            }}
            header {{
                background: #d0f0c0;
                text-align: center;
                padding: 22px;
            }}
            header h1 {{ color: green; }}
            main {{
                max-width: 760px;
                margin: 25px auto;
                padding: 0 16px;
            }}
            .card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 18px;
                box-shadow: 0 2px 7px #00000012;
            }}
            h2, .card h3 {{ color: #246b45; }}
            label {{
                display: block;
                margin-top: 12px;
                font-weight: bold;
            }}
            select {{
                padding: 10px;
                width: 100%;
                margin-top: 6px;
            }}
            button {{
                margin-top: 12px;
                background: #246b45;
                color: white;
                border: 0;
                border-radius: 5px;
                padding: 11px 16px;
                cursor: pointer;
            }}
            a {{ color: #246b45; }}
        </style>
    </head>
    <body>
        <header>
            <h1>🌱 EcoLink</h1>
            <p>Community Item Requests</p>
        </header>
        <main>
            <h2>Submitted Requests ({len(requests_list)})</h2>
            {rows}
            <p><a href="/">← Return to EcoLink</a></p>
        </main>
    </body>
    </html>
    """


@app.route("/requests/<int:request_id>/status", methods=["POST"])
def update_request_status(request_id):
    new_status = request.form.get("status", "")

    if new_status not in ["Pending", "Accepted", "Rejected"]:
        return "Invalid status.", 400

    connection = connect_db()

    result = connection.execute("""
        UPDATE requests
        SET status = ?
        WHERE id = ?
    """, (new_status, request_id))

    connection.commit()
    updated = result.rowcount
    connection.close()

    if updated == 0:
        return "Request not found.", 404

    return redirect("/requests")

@app.route("/", methods=["GET", "POST"])
def home():

    # Add a new item
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        condition = request.form.get("condition", "").strip()
        area = request.form.get("area", "").strip()
        description = request.form.get("description", "").strip()

        if title and category and condition and area:
            connection = connect_db()

            connection.execute("""
                INSERT INTO items
                (title, category, condition, area, description)
                VALUES (?, ?, ?, ?, ?)
            """, (title, category, condition, area, description))

            connection.commit()
            connection.close()

        return redirect("/")

    # Read search and category filters
    search = request.args.get("search", "").strip()
    category_filter = request.args.get("category", "").strip()

    # Retrieve matching items from SQLite
    connection = connect_db()

    query = "SELECT * FROM items WHERE 1=1"
    params = []

    if search:
        query += " AND (title LIKE ? OR description LIKE ?)"
        search_term = f"%{search}%"
        params.extend([search_term, search_term])

    allowed_categories = [
        "Books",
        "Clothing",
        "Electronics",
        "Furniture",
        "Household items",
        "Other"
    ]

    if category_filter in allowed_categories:
        query += " AND category = ?"
        params.append(category_filter)

    query += " ORDER BY id DESC"

    items = connection.execute(query, params).fetchall()
    connection.close()
    
    # Get dashboard statistics
    connection = connect_db()

    stats = connection.execute("""
        SELECT
            (SELECT COUNT(*) FROM items) AS total_items,
            (SELECT COUNT(*) FROM requests
             WHERE status = 'Pending') AS pending_requests,
            (SELECT COUNT(*) FROM requests
             WHERE status = 'Accepted') AS accepted_requests,
            (SELECT COUNT(*) FROM requests
             WHERE status = 'Rejected') AS rejected_requests,
	    (SELECT COUNT(*) FROM items) * 2 AS estimated_waste_kg
    """).fetchone()

    connection.close()


    # Build item cards
    item_cards = ""

    for item in items:
        item_cards += f"""
        <div class="card">
            <h3>{escape(item['title'])}</h3>
            <p><strong>Category:</strong> {escape(item['category'])}</p>
            <p><strong>Condition:</strong> {escape(item['condition'])}</p>
            <p><strong>Area:</strong> {escape(item['area'])}</p>
            <p>{escape(item['description'] or '')}</p>
	    <p>
		<a href="/request/{item['id']}">Request Item</a>
	    </p>
        </div>
        """

    if not item_cards:
        item_cards = """
        <p class="empty">
            No matching items found. Try another search!
        </p>
        """

    # Display the webpage
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>EcoLink - Community Exchange</title>

        <style>

            /* EcoLink visual polish: animations only; existing features stay unchanged */
            html {{ scroll-behavior: smooth; }}
            body {{ animation: ecoPageEnter 650ms ease-out both; }}
            header {{ animation: ecoHeaderEnter 700ms cubic-bezier(.2,.8,.2,1) both; }}
            main {{ animation: ecoContentEnter 700ms ease-out 80ms both; }}
            .card, .stat-card, form {{
                transition: transform 240ms ease, box-shadow 240ms ease, border-color 240ms ease;
                animation: ecoCardEnter 520ms ease-out both;
            }}
            .card:hover, .stat-card:hover {{
                transform: translateY(-4px);
                box-shadow: 0 10px 24px rgba(36, 107, 69, 0.13);
            }}
            button {{ transition: transform 180ms ease, background-color 180ms ease, box-shadow 180ms ease; }}
            button:hover {{ transform: translateY(-2px); box-shadow: 0 5px 12px rgba(36, 107, 69, 0.18); }}
            button:active {{ transform: translateY(0) scale(.98); }}
            a {{ transition: color 180ms ease, opacity 180ms ease; }}
            a:hover {{ opacity: .82; }}
            input, select, textarea {{ transition: border-color 180ms ease, box-shadow 180ms ease; }}
            input:focus, select:focus, textarea:focus {{
                outline: none;
                border-color: #70ad70;
                box-shadow: 0 0 0 3px rgba(112, 173, 112, .18);
            }}
            @keyframes ecoPageEnter {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            @keyframes ecoHeaderEnter {{
                from {{ opacity: 0; transform: translateY(-14px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            @keyframes ecoContentEnter {{
                from {{ opacity: 0; transform: translateY(12px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            @keyframes ecoCardEnter {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            @media (prefers-reduced-motion: reduce) {{
                html {{ scroll-behavior: auto; }}
                *, *::before, *::after {{
                    animation-duration: .01ms !important;
                    animation-iteration-count: 1 !important;
                    transition-duration: .01ms !important;
                    scroll-behavior: auto !important;
                }}
            }}


            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f2f8f1;
                color: #26382b;
            }}

            header {{
                background: #d0f0c0;
                text-align: center;
                padding: 25px 15px;
            }}

            header h1 {{
                color: green;
                margin: 0 0 8px;
                font-size: 32px;
            }}

            header p {{
                margin: 0;
            }}

            main {{
                max-width: 800px;
                margin: 25px auto;
                padding: 0 18px;
            }}

            h2 {{
                color: #246b45;
                margin-top: 28px;
            }}

            form, .card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 2px 7px #00000012;
            }}

            label {{
                display: block;
                margin-top: 14px;
                font-weight: bold;
            }}

            input, select, textarea {{
                display: block;
                width: 100%;
                padding: 11px;
                margin-top: 6px;
                border: 1px solid #cbd8cb;
                border-radius: 5px;
                font-size: 15px;
                background: white;
            }}

            textarea {{
                resize: vertical;
            }}

            button {{
                margin-top: 18px;
                background: #246b45;
                color: white;
                border: 0;
                padding: 12px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 15px;
            }}

            button:hover {{
                background: #174d30;
            }}

            .card {{
                border-left: 5px solid #70ad70;
            }}

            .card h3 {{
                color: #246b45;
                margin-top: 0;
            }}

            .card p {{
                overflow-wrap: anywhere;
            }}

            .empty {{
                background: white;
                padding: 20px;
                border-radius: 8px;
            }}

            .show-all {{
                display: inline-block;
                margin: 15px 0 0 12px;
                color: #246b45;
            }}

            .count {{
                color: #526b56;
                font-size: 14px;
            }}

.dashboard {{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 15px;
    margin-bottom: 25px;
}}

.stat-card {{
    background: white;
    border-left: 5px solid #70ad70;
    border-radius: 10px;
    padding: 16px;
    box-shadow: 0 2px 7px #00000012;
}}

.stat-card h3 {{
    color: #246b45;
    font-size: 15px;
    margin-top: 0;
}}

.stat-card p {{
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 0;
}}

@media (max-width: 500px) {{
    .dashboard {{
        grid-template-columns: 1fr;
    }}
}}


            footer {{
                text-align: center;
                padding: 22px;
                color: #526b56;
            }}

            @media (max-width: 600px) {{
                main {{
                    margin-top: 15px;
                    padding: 0 12px;
                }}

                form, .card {{
                    padding: 15px;
                }}
            }}
        </style>
    </head>

    <body>
        <header>
            <h1>🌱 EcoLink</h1>
            <p>Share useful items. Reduce waste.</p>
        </header>

        <main>
	    <p><a href="/requests">View Item Requests</a></p>
            <h2>List a Reusable Item</h2>

            <form method="POST">

                <label for="title">Item name *</label>
                <input
                    id="title"
                    name="title"
                    maxlength="100"
                    required
                    placeholder="e.g. School bag"
                >

                <label for="new-category">Category *</label>
                <select id="new-category" name="category" required>
                    <option value="">Choose a category</option>
                    <option>Books</option>
                    <option>Clothing</option>
                    <option>Electronics</option>
                    <option>Furniture</option>
                    <option>Household items</option>
                    <option>Other</option>
                </select>

                <label for="condition">Condition *</label>
                <select id="condition" name="condition" required>
                    <option value="">Choose condition</option>
                    <option>Like new</option>
                    <option>Good</option>
                    <option>Usable</option>
                </select>

                <label for="area">Area or locality *</label>
                <input
                    id="area"
                    name="area"
                    maxlength="100"
                    required
                    placeholder="e.g. Your locality"
                >

                <label for="description">Description</label>
                <textarea
                    id="description"
                    name="description"
                    maxlength="500"
                    rows="3"
                    placeholder="Describe the item"
                ></textarea>

                <button type="submit">Add Item</button>
            </form>
	    
<h2>EcoLink Dashboard</h2>

<div class="dashboard">
    <div class="stat-card">
        <h3>Total Items</h3>
        <p>{stats['total_items']}</p>
    </div>

    <div class="stat-card">
        <h3>Pending Requests</h3>
        <p>{stats['pending_requests']}</p>
    </div>

    <div class="stat-card">
        <h3>Accepted Requests</h3>
        <p>{stats['accepted_requests']}</p>
    </div>

    <div class="stat-card">
        <h3>Rejected Requests</h3>
        <p>{stats['rejected_requests']}</p>
    </div>
    <div class="stat-card">
        <h3>Estimated Waste Avoided</h3>
        <p>{stats['estimated_waste_kg']} kg</p>
    </div>
</div>

            <h2>Find Reusable Items</h2>
	    
            

            <form method="GET">

                <label for="search">Search by name or description</label>
                <input
                    id="search"
                    type="text"
                    name="search"
                    maxlength="100"
                    placeholder="e.g. school bag"
                    value="{escape(search, quote=True)}"
                >

                <label for="filter-category">Filter by category</label>
                <select id="filter-category" name="category">
                    <option value=""
                        {"selected" if not category_filter else ""}>
                        All categories
                    </option>
                    <option value="Books"
                        {"selected" if category_filter == "Books" else ""}>
                        Books
                    </option>
                    <option value="Clothing"
                        {"selected" if category_filter == "Clothing" else ""}>
                        Clothing
                    </option>
                    <option value="Electronics"
                        {"selected" if category_filter == "Electronics" else ""}>
                        Electronics
                    </option>
                    <option value="Furniture"
                        {"selected" if category_filter == "Furniture" else ""}>
                        Furniture
                    </option>
                    <option value="Household items"
                        {"selected" if category_filter == "Household items" else ""}>
                        Household items
                    </option>
                    <option value="Other"
                        {"selected" if category_filter == "Other" else ""}>
                        Other
                    </option>
                </select>

                <button type="submit">Search Items</button>
                <a class="show-all" href="/">Show All Items</a>
            </form>

            <h2>Community Items</h2>

            <p class="count">
                Showing {len(items)} matching item(s)
            </p>

            {item_cards}

        </main>

        <footer>
<h2>Find Reusable Items</h2>
            <p>EcoLink 🌱 | Reuse More, Waste Less</p>
            <p>Supporting Responsible Consumption and Production — SDG 12</p>
<h2>Our Environmental Mission</h2>

<div class="card">
    <p>
        EcoLink encourages people to share and reuse useful items
        instead of throwing them away.
    </p>

    <p>
        Reusing products can help reduce waste, conserve resources,
        and support responsible consumption.
    </p>

    <p>
        <strong>Supporting UN Sustainable Development Goal 12:</strong>
        Responsible Consumption and Production.
    </p>
</div>
        </footer>
    </body>
    </html>
    """


if __name__ == "__main__":
    create_table()
    app.run(debug=False)
