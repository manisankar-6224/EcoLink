
from flask import Flask, request, redirect

app = Flask(__name__)

# Temporary storage while the application is running
items = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        condition = request.form.get("condition", "").strip()
        area = request.form.get("area", "").strip()
        description = request.form.get("description", "").strip()

        if title and category and condition and area:
            items.append({
                "title": title,
                "category": category,
                "condition": condition,
                "area": area,
                "description": description
            })

        return redirect("/")

    item_cards = ""

    for item in items:
        item_cards += f"""
        <article class="card">
            <h3>{item['title']}</h3>
            <p><b>Category:</b> {item['category']}</p>
            <p><b>Condition:</b> {item['condition']}</p>
            <p><b>Area:</b> {item['area']}</p>
            <p>{item['description']}</p>
        </article>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>EcoLink</title>
        <style>
            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f2f7f0;
                color: #263b2a;
            }}
            header {{
                background: #246b45;
                color: white;
                padding: 20px;
                text-align: center;
            }}
            main {{
                max-width: 800px;
                margin: 30px auto;
                padding: 0 16px;
            }}
            form, .card {{
                background: white;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 8px #00000010;
            }}
            input, select, textarea {{
                display: block;
                width: 100%;
                box-sizing: border-box;
                padding: 10px;
                margin: 8px 0 16px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font: inherit;
            }}
            button {{
                background: #246b45;
                color: white;
                border: 0;
                padding: 12px 20px;
                border-radius: 5px;
                cursor: pointer;
            }}
            .card h3 {{ color: #246b45; }}
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
                <label>Item name *</label>
                <input name="title" maxlength="100" required
                       placeholder="e.g. School bag">

                <label>Category *</label>
                <select name="category" required>
                    <option value="">Choose a category</option>
                    <option>Books</option>
                    <option>Clothing</option>
                    <option>Electronics</option>
                    <option>Furniture</option>
                    <option>Household items</option>
                    <option>Other</option>
                </select>

                <label>Condition *</label>
                <select name="condition" required>
                    <option value="">Choose condition</option>
                    <option>Like new</option>
                    <option>Good</option>
                    <option>Usable</option>
                </select>

                <label>Area or locality *</label>
                <input name="area" maxlength="100" required
                       placeholder="e.g. Your locality">

                <label>Description</label>
                <textarea name="description" maxlength="500"
                          rows="3" placeholder="Describe the item"></textarea>

                <button type="submit">Add Item</button>
            </form>

            <h2>Community Items ({len(items)})</h2>
            {item_cards if item_cards else '<p>No items listed yet. Add the first one!</p>'}
        </main>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=False)
