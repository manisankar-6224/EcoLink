
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

    connection.commit()
    connection.close()


# Main page
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
            <p>EcoLink 🌱 | Reuse More, Waste Less</p>
            <p>Supporting Responsible Consumption and Production — SDG 12</p>
        </footer>
    </body>
    </html>
    """


if __name__ == "__main__":
    create_table()
    app.run(debug=False)
