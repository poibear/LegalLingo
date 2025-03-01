import os
import json
import random
import thefuzz
from thefuzz import process
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for, flash

################################################################################

app = Flask(__name__, template_folder="templates")

# load form info for search
with open("form_names.json", "r") as f:
    form_names = json.load(f)

@app.route("/")
def index():
    # banner text
    catchphrases = [
        "Make your taxes easy like bingo!",
        "TurboTax? What's what?",
        "Avoid the IRS",
        "Read legal documents like a second language",
        "Why pay for filing taxes when it can be free?"
    ]
    
    catchphrase = random.choice(catchphrases)

    help = "Need help with your taxes? Learn how to navigate them with LegalLingo!"
# FORM 911 – REQUEST FOR TAS ASSISTANCE
# FORMS 1040 – 1040X – 1040ES
# FORM 433F – FINANCIAL COLLECTION INFORMATION STATEMENT
# FORM 9465 – INSTALLMENT AGREEMENT
# FORM 656 – OFFER IN COMPROMISE
# FORM 2848 – POWER OF ATTORNEY
# FORM 12508 – INNOCENT SPOUSE QUESTIONNAIRE
# FORM 8379 – INJURED SPOUSE
# FORM 4506 – REQUEST FOR TAX TRANSCRIPT
# FORM 8822 – CHANGE OF ADDRESS
# FORM W-4 – EMPLOYEE’S WITHHOLDING ALLOWANCE CERTIFICATE
# FORM W-7 – ITIN APPLICATION
# Publication 1, YOUR RIGHTS AS A TAXPAYER
    return render_template("index.html", catchphrase=catchphrase, help=help, form_names=form_names)

@app.route("/search")
def search():
    query = request.args.get("form") # form query key
    
    # filter by best match
    top_results = process.extract(
        query,
        form_names,
        limit=3,
        scorer=thefuzz.fuzz.token_sort_ratio
    )
    
    # make a table of the top results through html
    return render_template("form-results.html", top_results=top_results)
    
    
    
    
    

@app.route("/form")
def form():
    """Get query string from search box in index.html and process it"""
    return render_template("form.html")






#Starts the server, do not change!
if __name__ == "__main__":
    host = "127.0.0.1"
    port = "8080"
    app.config["TEMPLATES_AUTO_RELOAD"] = True # reload on html change
    app.secret_key = 'supa secretz'
    app.debug = True
    app.run(host=host, port=port)