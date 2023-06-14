from app import app
from flask import Flask, render_template, request, redirect, url_for
import requests
import json
from bs4 import BeautifulSoup
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from app.utils import get_element, selectors


@app.route("/name", defaults={"name":"Anonim"})
@app.route("/name/<name>")
def name(name):
    return f"Hello {name}"

@app.route("/")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/extract", methods=["POST", "GET"])
def extract():
    if request.method == "POST":
        product_code = request.form.get("product_code")
        all_opinions = []
        # url = "https://www.ceneo.pl/" + product_code + "#tab=reviews"
        url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
        while(url):
            print(url)
            response = requests.get(url)
            page_dom = BeautifulSoup(response.text, "html.parser")
            opinions = page_dom.select("div.js_product-review")
            for opinion in opinions:
                single_opinion = {}
                for key, value in selectors.items():
                    single_opinion[key] = get_element(opinion, *value)
                all_opinions.append(single_opinion)
            try:
                url = "https://www.ceneo.pl"+get_element(page_dom, "a.pagination__next", "href")
            except TypeError:
                url = None

        if not os.path.exists("./app/data/opinions"):
            os.mkdir("./app/data/opinions")
        with open(f"./app/data/opinions/{product_code}.json", "w", encoding="UTF-8") as jf:
            json.dump(all_opinions, jf, indent=4, ensure_ascii=False)
        opinions = pd.read_json(json.dumps(all_opinions,ensure_ascii=False))
        opinions.score = opinions.score.map(lambda x: float(x.split("/")[0].replace(",",".")))
        stats = {
            "opinions_count": int(opinions.shape[0]),
            "pros_count": int(opinions.pros.map(bool).sum()),
            "cons_count": int(opinions.cons.map(bool).sum()),
            "avg_score": opinions.score.mean().round(2)
        }
        score = opinions.score.value_counts().reindex(list(np.arange(0,5.5,0.5)), fill_value = 0)
        score.plot.bar(color="hotpink")
        plt.xticks(rotation=0)
        plt.title("Histogram ocen")
        plt.xlabel("Liczba gwiazdek")
        plt.ylabel("Liczba opinii")
        plt.ylim(0,max(score.values)+1.5)
        for index, value in enumerate(score):
            plt.text(index, value+0.5, str(value), ha="center")
        try:
            os.mkdir("./app/static/plots")
        except FileExistsError:
            pass
        plt.savefig(f"./app/static/plots/{product_code}_score.png")
        plt.close()
        recommendation = opinions["recommendation"].value_counts(dropna = False).reindex(["Nie polecam", "Polecam", np.nan])
        print(recommendation)
        recommendation.plot.pie(
            label="", 
            autopct="%1.1f%%",
            labels = ["Nie polecam", "Polecam", "Nie mam zdania"],
            colors = ["crimson", "forestgreen", "gray"]
        )
        plt.legend(bbox_to_anchor=(1.0,1.0))
        plt.savefig(f"./app/static/plots/{product_code}_recommendation.png")
        plt.close()
        stats['score'] = score.to_dict()
        stats['recommendation'] = recommendation.to_dict()
        try:
            os.mkdir("./app/static/stats")
        except FileExistsError:
            pass
        with open(f"./app/static/stats/{product_code}.json", "w", encoding="UTF-8") as jf:
            json.dump(stats, jf, indent=4,ensure_ascii=False)
        return redirect(url_for('product_site', code=product_code))
    return render_template("extraction.html")

@app.route("/author")
def author():
    return render_template("author.html")

@app.route("/product_list")
def product_list():
    return render_template("product_list.html")

@app.route("/product_site/<code>")
def product_site(code):
    opinions = pd.read_json(f"./opinions/{code}.json")
    return render_template("product_site.html", product_code=code, opinions= opinions.to_html(header="True", table_id= "opinions", classes= "table table-striped table-info"))