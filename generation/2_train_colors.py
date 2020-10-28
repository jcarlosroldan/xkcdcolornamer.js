from collections import defaultdict as ddict
from os import listdir, makedirs, getcwd
from os.path import exists, dirname
from pickle import load as pload, dump as pdump
from PIL import Image
from random import shuffle, sample
from re import sub
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier

NUM_COLORS = 256, 512

PATH_NAMES = 'names.pk'
PATH_IMAGES_INPUT = 'images/original'
PATH_IMAGES_OUTPUT = 'images/done%s'

EXTENSIONS = 'jpg', 'jpeg', 'png', 'gif'
INVALID_FILENAME_CHARS_REGEX = r"[/\\\*;\[\]\":=,<>]"

def main():
	names = load_names()
	for num_colors in NUM_COLORS:
		print('num_colors = %s' % num_colors)
		rgbs2names = train_rgbs2names(names[:num_colors])
		name2rgb = train_name2rgb(names[:num_colors])
		process_images(rgbs2names, name2rgb, num_colors)

def load_names():
	with open(PATH_NAMES, 'rb') as fp:
		return pload(fp)

def train_rgbs2names(names, export=True):
	''' Why not rgb2name one on one? Because .predict is much faster in batches. '''
	X, Y = zip(*(
		(color, name)
		for name, colors in names
		for color in colors
	))
	res = MLPClassifier(hidden_layer_sizes=(9, 27, int(len(names) // 2)))
	res.fit(X, Y)
	print(res.classes_)
	if export:
		from sklearn_porter import Porter
		with open('last_model.js', 'w', encoding='utf-8') as fp:
			fp.write(Porter(res, language='js').export())
	return lambda rgbs: res.predict(rgbs)

def train_name2rgb(names):
	translator = {
		name: tuple(
			int(sum(c) / len(c))
			for c in zip(*colors)
		)
		for name, colors in names
	}
	return lambda name: translator[name] if name in translator else None

def process_images(rgbs2names, name2rgb, num_colors):
	dst = PATH_IMAGES_OUTPUT % num_colors
	makedirs(dst, exist_ok=True)
	for image in listdir(PATH_IMAGES_INPUT):
		name, ext = image.lower().rsplit('.', 1)
		if ext not in EXTENSIONS: continue
		print('\t%s' % image)
		img = Image.open('%s/%s' % (PATH_IMAGES_INPUT, image))
		img.putdata([name2rgb(name) for name in rgbs2names(img.getdata())])
		img.save('%s/%s.png' % (dst, name))

if __name__ == '__main__':
	main()