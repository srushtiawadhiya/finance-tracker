from flask import Flask, render_template, request, redirect
from task1 import add_transaction, get_transactions

app = Flask(__name__)
@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        t_type = request.form["type"]
        category = request.form["category"]
        amount = float(request.form["amount"])
        date = request.form["date"]

        add_transaction(t_type,category,amount,date)
        return redirect("/")#refresh the page after adding trans.
    
    transactions = get_transactions()
    return render_template("index.html",transactions=transactions)

if __name__ == "__main__":
    app.run(debug=True)