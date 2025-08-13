from datetime import date
from forex_python.converter import CurrencyRates
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8000

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/calculate_age"):
            query = parse_qs(self.path.split("?", 1)[1])
            birth_year = int(query.get("year", [0])[0])
            birth_month = int(query.get("month", [0])[0])
            birth_date = int(query.get("day", [0])[0])
            today = date.today()
            age = today.year - birth_year - (
                (today.month, today.day) < (birth_month, birth_date)
            )
            self.respond(self.page_content(f"<h2>Your Age: {age} years</h2><a href='/'>Back</a>"))
        elif self.path.startswith("/currency_convert"):
            query = parse_qs(self.path.split("?", 1)[1])
            amount = float(query.get("amount", [0])[0])
            from_currency = query.get("from", [""])[0].upper()
            to_currency = query.get("to", [""])[0].upper()
            c = CurrencyRates()
            try:
                result = c.convert(from_currency, to_currency, amount)
                self.respond(self.page_content(f"<h2>{amount} {from_currency} = {round(result, 2)} {to_currency}</h2><a href='/'>Back</a>"))
            except Exception:
                self.respond(self.page_content("<h2>Currency conversion failed. Please check the inputs.</h2><a href='/'>Back</a>"))
        else:
            self.respond(self.page_content("""
                <h1>Calculator Portfolio</h1>
                <div class='card'>
                    <h2>Age Calculator</h2>
                    <form action="/calculate_age">
                        <label>Year:</label><input type="number" name="year" required><br>
                        <label>Month:</label><input type="number" name="month" required><br>
                        <label>Day:</label><input type="number" name="day" required><br>
                        <input type="submit" value="Calculate Age">
                    </form>
                </div>
                <div class='card'>
                    <h2>Currency Converter</h2>
                    <form action="/currency_convert">
                        <label>Amount:</label><input type="number" step="0.01" name="amount" required><br>
                        <label>From Currency (e.g., USD):</label><input type="text" name="from" required><br>
                        <label>To Currency (e.g., INR):</label><input type="text" name="to" required><br>
                        <input type="submit" value="Convert">
                    </form>
                </div>
            """))
#Using html in Python
    def page_content(self, body_html):
        return f"""
        <html>
        <head>
            <title>Calculator Portfolio</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #0D1B2A;
                    color: white;
                    margin: 0;
                    padding: 0;
                    text-align: center;
                }}
                h1 {{
                    background-color: #1B263B;
                    padding: 20px;
                    margin: 0;
                }}
                .card {{
                    background: #1E3A5F;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 20px auto;
                    width: 300px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.5);
                }}
                form {{
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }}
                input[type="number"], input[type="text"] {{
                    padding: 8px;
                    border: none;
                    border-radius: 5px;
                }}
                input[type="submit"] {{
                    background-color: #415A77;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 5px;
                    cursor: pointer;
                }}
                input[type="submit"]:hover {{
                    background-color: #778DA9;
                }}
                a {{
                    color: #FFD60A;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            {body_html}
        </body>
        </html>
        """

    def respond(self, html):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

if __name__ == "__main__":
    print(f"Server running at http://localhost:{PORT}")
    HTTPServer(("localhost", PORT), MyHandler).serve_forever()
