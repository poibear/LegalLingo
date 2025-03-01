import os
import json
import random
import thefuzz
from thefuzz import process
from datetime import datetime
from tax_explainer import getTaxDescription
from flask import Flask, redirect, render_template, request, url_for, flash

################################################################################

app = Flask(__name__, template_folder="templates")

# load form info for search
with open("form_names.json", "r") as f:
    form_names = json.load(f)

with open("FAQ.json", "r") as q:
    FAQ = json.load(q)
    
@app.context_processor
def datetime_variable():
    return {"datetime": datetime}

@app.route("/")
def index():
    # banner text
    catchphrases = [
        "Make your taxes easy like bingo!",
        "TurboTax? What's that?",
        "Avoid the IRS with our help!",
        "Read legal documents like a second language.",
        "Why pay for filing taxes when it can be free?"
    ]
    
    descriptions = [
        "Understand your tax documents in layman's terms",
        "We make every tax dollar count with our in-depth analyses",
        "Some call it taxes, we call it \"investing in the future\"",
        "We will make your tax return feel like a vacation"
    ]
    
    catchphrase = random.choice(catchphrases)
    description = random.choice(descriptions)

    help = "Need help with your taxes? Learn how to navigate them with LegalLingo!"

    return render_template("index.html", catchphrase=catchphrase, description=description, help=help, FAQ=FAQ)

@app.route("/query", methods=["GET"])
def query():
    """Gets top results of most likely available forms"""
    query = request.args.get("form") # form query key
        
    # filter by best match
    top_results = process.extract(
        query,
        form_names,
        limit=3, # how many results to show
        scorer=thefuzz.fuzz.token_sort_ratio
    )
    
    # if first result has no correlation, then dont return any results
    if top_results[0][1] == 0:
        top_results = None
    
    # make a table of the top results through html
    return render_template("form-results.html", top_results=top_results)

@app.route("/search", methods=["GET"])
def search():
    return render_template("search.html", form_names=form_names)
        
@app.route("/form", methods=["GET"])
def form():
    if request.args.get("name"):
        form_name = request.args.get("name") # e.g,. 1099
        summary = form_names[form_name]
        detailed_description = getTaxDescription(form_name)
        
        # sometimes summaries are blank
        if not summary:
            summary = f"No summary has been provided for {form_name}"
        
       # TODO https://platform.openai.com/docs/api-reference/assistants/createAssistant?lang=python
       
        return render_template("form.html", form_name=form_name, summary=summary, form_desc=detailed_description)
        
#Starts the server, do not change!
if __name__ == "__main__":
    host = "127.0.0.1"
    port = "8080"
    app.config["TEMPLATES_AUTO_RELOAD"] = True # reload on html change
    app.secret_key = 'supa secretz'
    app.debug = True
    app.run(host=host, port=port)