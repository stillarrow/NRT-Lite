DS = 'yelp'
# DS = 'ratebeer'
OUTPUT_PATH = f'data/{DS}_output'

# Corpus
TRAIN_CORPUS = f'{OUTPUT_PATH}/split/train.txt'
DEV_CORPUS = f'{OUTPUT_PATH}/split/dev.txt'
TEST_CORPUS = f'{OUTPUT_PATH}/split/test.txt'

# User & Item files
USER_FILE = f'{OUTPUT_PATH}/users.txt'
ITEM_FILE = f'{OUTPUT_PATH}/items.txt'

# Vocabulary & Word Embedding
VOC_FILE = f'{OUTPUT_PATH}/vocabulary.json'
WORD_EMBEDDING_FILE = f'{OUTPUT_PATH}/voc_we.txt'

# Feature list
FEATURE_FILE = f'{OUTPUT_PATH}/features.json'
ITEM_FEATURE_FILE = f'{OUTPUT_PATH}/item_features.json'

# NDCG
NDCG_TEST_FILE = f'{OUTPUT_PATH}/ndcg.json'

# Checkpoints
SAVE_DIR = f'{DS}_checkpoints'
DEFAULT_MODEL_NAME = 'nnr'

# Trainer behaviors
PATIENCE = 10
PRINT_EVERY = 1000
SAVE_EVERY = 10

# Parameters for processing the dataset
MAX_LENGTH = 30  # Maximum sentence length to consider

BINARY_RATING_THRESHOLD = None      # None for no conversion, otherwise ratings >= the threshold are converted to 1, else as 0
RANKING_RATING_THRESHOLD = None     # if not None, change score to binary for ranking

# rating normalization
NORM_RATING = False
RATING_MEAN = 13.33
RATING_STD = 3.24

# RATING_MEAN = 3.78
# RATING_STD = 1.12

LOSS_TYPE_GRP_CONFIG = {
    'RankHinge': {'grp_size': 2, 'n_min_rated': 2},
    'BPR': {'grp_size': 3, 'n_min_rated': 1},
    'LambdaRank': {'grp_size': 44, 'n_min_rated': 1},
}
HINGE_THRESHOLD = 1.5
