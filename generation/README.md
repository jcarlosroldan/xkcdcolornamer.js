# XKCD color namer generation

Actually, the library only contains a transpiled [MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html). To generate it:

1. Install Python 3 and the `requirements.txt` file.
2. Download the [XKCD survey results](https://xkcd.com/color/colorsurvey.tar.gz) and put `mainsurvey_sqldump.txt` in the same folder as the Python scripts.
3. Run `1_compute_names.py` to generate a clean set of colors and names.
4. Run `2_train_colors.py` to generate the model at `last_model.js`. You can adjust the `NUM_COLORS` parameter as you prefer.
5. Minify the JS with your preferred minifier.

The images in the `images/` folder are for the sake of testing. I took them all, so feel free to use them as you please.