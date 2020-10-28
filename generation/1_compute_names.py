from re import findall, match, compile as rcompile
from pickle import dump
from collections import defaultdict

PATH_DUMP = 'mainsurvey_sqldump.txt'  # from https://xkcd.com/color/colorsurvey.tar.gz
PATH_NAMES = 'names.pk'
REGEX_ENTRIES = rcompile(r'answers" VALUES\(\d+,\d+,\d+.\d+,((\d+),(\d+),(\d+),\'(.+?)\')')
REGEX_SPACES = rcompile(r'\s+')
REPLACE_CONTAINS = (('-', ' '), ('/', ' '), ('.', ' '), ('!', ''), ('?', ''), (' again', ''), (' color', ''), (' tone', ''), ('gray', 'grey'), ('fuchia', 'fuschia'), ('fuchsia', 'fuschia'), ('fucia', 'fuschia'), ('fucshia', 'fuschia'), ('fucsia', 'fuschia'), ('fuscha', 'fuschia'), ('fuschia', 'fuschia'), ('fuscia', 'fuschia'), ('fusha', 'fuschia'), ('fushcia', 'fuschia'), ('fushia', 'fuschia'), ('fusia', 'fuschia'), ('gren', 'green'), ('puple', 'purple'), ('redish', 'reddish'), ('robin egg', 'robins egg'), ('terra cotta', 'terracotta'), ('burgandy', 'burgundy'), ('ocre', 'ochre'), ('purpleish', 'purplish'), ('purply', 'purpley'), ('pruple', 'purple'), ('chartruese', 'chartreuse'), ('chartruse', 'chartreuse'), ('turqoise', 'turquoise'), ('turqouise', 'turquoise'), ('turquiose', 'turquoise'), ('turquise', 'turquoise'), ('torquoise', 'turquoise'), ('poop', 'poo'), ('kaki', 'khaki'), ('lila', 'lilac'), ('sea foam', 'seafoam'), ('violett', 'violet'), ('perriwinkle', 'periwinkle'), ('marroon', 'maroon'), ('marron', 'maroon'), ('fluro', 'fluor'), ('lilacc', 'lilac'), ('avacado', 'avocado'), ('biege', 'beige'), ('bleu', 'blue'), ('blue', 'blu'), ('lavander', 'lavender'), ('lavendar', 'lavender'), ('ocher', 'ochre'), ('tope', 'taupe'), ('ble', 'blu'), ('voilet', 'violet'), ('purle', 'purple'), ('kelley', 'kelly'), ('fluoro', 'fluor'), ('kakhi', 'khaki'), ('purpe', 'purple'), ('purplel', 'purple'))
REPLACE_EQUALS = (('turquois', 'turquoise'), ('gree', 'green'), ('greeb', 'green'), ('yello', 'yellow'), ('purpl', 'purple'), ('brow', 'brown'), ('bluw', 'blu'))
SPAM_CONTAINS = ('aids', 'asd', 'asdf', 'ass', 'blur', 'bob', 'boring', 'cocksucker', 'data', 'dick', 'disgust', 'do a barrel roll', 'dunno', 'eww', 'fag', 'fuck', 'gay', 'gross', 'horrible', 'i don', 'idk', 'josh', 'meh', 'nigger', 'no idea', 'penis', 'sex', 'ugh', 'weird', 'what', 'wtf', 'xkcd', 'you', 'your mom', 'yuck')
SPAM_EQUALS = ('ick')

def main():
	survey = load_survey()
	names = build_names(survey)
	save_names(names)

def load_survey():
	with open(PATH_DUMP, 'r', encoding='utf-8') as fp:
		return fp.read()

def build_names(survey):
	names = defaultdict(list)
	for _, r, g, b, name in REGEX_ENTRIES.findall(survey):
		names[clean_color(name)].append((int(r), int(g), int(b)))
	names = [
		(name, colors)
		for name, colors in sorted(names.items(), key=lambda kv: -len(kv[1]))
		if 2 < len(name) < 100 and not is_spam(name)
	]
	return names

def clean_color(color):
	res = REGEX_SPACES.sub(' ', color).strip()
	for before, after in REPLACE_CONTAINS:
		res = res.replace(before, after)
	for before, after in REPLACE_EQUALS:
		if res == before:
			res = after
	return res

def is_spam(color):
	return len(color) < 3 or len(color) > 100 or \
		any(s in color for s in SPAM_CONTAINS) or \
		any(s == color for s in SPAM_EQUALS)

def save_names(names):
	with open(PATH_NAMES, 'wb') as fp:
		dump(names, fp, protocol=4)

if __name__ == '__main__':
	main()