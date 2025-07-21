from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

transactions = []
transaction_id = 1

@app.route("/", methods=["GET", "POST"])
def index():
    global transaction_id
    if request.method == "POST":
        t_type = request.form["type"]
        amount = float(request.form["amount"])
        description = request.form["description"]
        transactions.append({
            "id": transaction_id,
            "type": t_type,
            "amount": amount,
            "description": description
        })
        transaction_id += 1
        return redirect(url_for("index"))

    income = sum(t["amount"] for t in transactions if t["type"] == "income")
    expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
    balance = income - expense

    return render_template("index.html", transactions=transactions, income=income, expense=expense, balance=balance)

@app.route("/delete/<int:trans_id>", methods=["POST"])
def delete(trans_id):
    global transactions
    transactions = [t for t in transactions if t["id"] != trans_id]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
