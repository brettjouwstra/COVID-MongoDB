from flask import Flask, render_template

from _db import loc_collection
from _db import loc_stats
from _db import stats

app = Flask(__name__)

@app.route("/")
def index():
    all_data = loc_collection.find({})
    
    basic_stats = loc_collection.find_one({'uid': 84046103})

    high_death = loc_collection.find(sort=[('deaths', -1)]).limit(5)    

    confirmed_high = loc_collection.find(sort=[('confirmed', -1)]).limit(3)

    confirmed_low = loc_collection.find(sort=[('confirmed', 1)]).limit(3)

    SD_dead = {'jun': 273, 'july': 673, 'august': 993, 'sept': 1029, 'october': 948}
    ND_dead = {'jun': 1844, 'july': 2229, 'august': 2356, 'sept': 2299, 'october': 1812}

    return render_template('dashboard.html', basic_stats=basic_stats, high_death=high_death, confirmed_high=confirmed_high, confirmed_low=confirmed_low, SD_dead=SD_dead, ND_dead=ND_dead, stats=stats())


if __name__=='__main__':
    app.run(debug=True)