from flask import *
import numpy as np
import pandas as pd
from PIL import Image, UnidentifiedImageError

app = Flask(__name__)


def count_colours(file):
    with Image.open(file) as img:
        img = img.convert('RGB')
        img_array = np.array(img)
    colours, counts = np.unique(img_array.reshape(-1, 3), axis=0, return_counts=True)
    df = pd.DataFrame(data=colours, index=counts)
    top_10 = df.sort_index(ascending=False)[:10]
    # Only returns the top 10, not the count
    # TODO: Return count as well
    return [(int(row[0]), int(row[1]), int(row[2])) for index, row in top_10.iterrows()]


@app.route("/", methods=["GET", "POST"])
def home():
    colours = None
    error = None
    if request.method == "POST":
        try:
            file = request.files['file']
            colours = count_colours(file)
        except UnidentifiedImageError:
            error = "No File Selected"

    return render_template("index.html", colours=colours, error=error)


if __name__ == "__main__":
    app.run(debug=True)
