from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

@app.route("/")
def index():
    url = "https://store.steampowered.com/api/appdetails?appids="
    app_id_list = [1091500, 1245620, 2050650, 2124490, 739630]
    app_list = []
    for app_id in app_id_list:
        app_dict = {}
        result = json.loads(requests.get(url + str(app_id)).content)
        app_dict["name"] = result[str(app_id)]['data']['name']
        app_dict["currency"] = result[str(app_id)]['data']['price_overview']['currency']
        app_dict["price"] = result[str(app_id)]['data']['price_overview']['initial']
        app_list.append(app_dict)
    return render_template("index.html", app_list=app_list)

@app.route("/app/<int:app_id>")
def get_app_info(app_id):
    url = "https://store.steampowered.com/api/appdetails?appids="
    url_2 = "https://store.steampowered.com/api/dlcforapp/?appid="
    result = json.loads(requests.get(url + str(app_id)).content)
    result_2 = json.loads(requests.get(url_2 + str(app_id)).content)
    app_dict = {}
    app_dict["name"] = result[str(app_id)]['data']['name']
    app_dict["currency"] = result[str(app_id)]['data']['price_overview']['currency']
    app_dict["price"] = result[str(app_id)]['data']['price_overview']['initial']
    if result_2["dlc"]:
        app_dict["dlc"] = result_2['dlc'][0]['name']
        app_dict["dlc_price_currency"] = result_2['dlc'][0]['price_overview']['currency']
        app_dict["dlc_price_value"] = result_2['dlc'][0]['price_overview']['final']
    app_dict["pc_requirements"] = result[str(app_id)]['data']['pc_requirements']['recommended']
    return render_template("app_info.html", app_dict=app_dict)

@app.route("/histogram/<int:app_id>")
def histogram(app_id):
    url = "https://store.steampowered.com/appreviewhistogram/"
    result = json.loads(requests.get(url + str(app_id)).content)

@app.route("/reviews/<int:app_id>")
def get_reviews(app_id):
    url = "https://store.steampowered.com/appreviews/"
    review_list = []
    result = json.loads(requests.get(url + str(app_id) + "?cursor=*&json=1&day_range=30&start_date=-1&end_date=-1&date_range_type=all&filter=summary&language=english%2Cdutch&l=english&review_type=all&purchase_type=all&playtime_filter_min=0&playtime_filter_max=0&filter_offtopic_activity=0&summary_num_positive_reviews=25938&summary_num_reviews=28651").content)
    review_score = (result["query_summary"]["review_score"])
    for i in result["reviews"]:
        review_list.append((i["review"]))
    return render_template("reviews.html", review_list=review_list, review_score=review_score)

if __name__ == "__main__":
    app.run(debug=True)