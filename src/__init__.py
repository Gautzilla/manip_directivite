from os import path

DATA_PATH = path.abspath(r'data')
DATABASE_PATH = path.join(DATA_PATH, 'manip_directivite.db')
AUDIO_FOLDER = path.join(DATA_PATH, 'audio')
ASSETS_FOLDER = path.join(DATA_PATH, 'assets')
SENTENCES_CSV_FILE = path.join(DATA_PATH, 'sentences.csv')

DEV = False