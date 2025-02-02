import numpy as np
import torch
from torchtext import data

from .constants import MAX_LENGTH, MIN_FREQ


def __review_postprocessing(review, vocab):
    def freqs_sent(sentence):
        length = np.where(sentence == eos_ind)[0][0] + 1
        freqs = np.bincount(sentence, minlength=len(vocab.itos)) / length
        freqs[1] = 0
        return freqs

    review = np.array(review).astype(int)
    eos_ind = vocab.stoi['$end']
    freq_arr = np.apply_along_axis(
        freqs_sent,
        axis=1,
        arr=review
    )
    return freq_arr.T


def amazon_dataset_iters(
        parent_path, batch_sizes=(32, 64, 64),
        minimum_frequency=MIN_FREQ,
        verbose=True):
    """Helper function for creating batch iterators over Amazon Reviews datasets.

    Arguments:
        parent_path: path to folder with train.json, val.json and test.json in Amazon format
        device: device to allocate batches on
        batch_sizes: tuple of (train_batch_size, val_batch_size, test_batch_size)
        minimum_frequency: minimum frequency of words in batches (parameter of data.Field.build_vocab)
        verbose: True will print current status of processing

    Returns:
        (vocab, train_iter, val_iter, test_iter) - vocab and batch iterators for train, validation and test data.
        Each batch contains the following fields:
        batch.item - torch.LongTensor of shape (batch_size,) - numbers of reviewed items
        batch.user - torch.LongTensor of shape (batch_size,) - numbers of reviewers
        batch.text - torch.LongTensor of shape (word_num,batch_size) - encoded words in sentences
    """

    if torch.cuda.is_available():
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')

    item = data.Field(sequential=False)
    user = data.Field(sequential=False)
    text = data.Field(
        sequential=True,
        tokenize='spacy',
        init_token="$start",
        eos_token="$end",
        lower=True,
        dtype=torch.float,
        postprocessing=__review_postprocessing)
    tips = data.Field(
        sequential=True,
        tokenize='spacy',
        init_token="$start",
        eos_token="$end",
        fix_length=MAX_LENGTH + 2,
        lower=True)
    rating = data.Field(sequential=False, use_vocab=False, dtype=torch.float)
    if verbose:
        print('Loading datasets...')
    train, val, test = data.TabularDataset.splits(
        path=parent_path,
        train='train.json',
        test='test.json',
        validation='val.json',
        format='json',
        fields={
            'asin': ('item', item),
            'reviewerID': ('user', user),
            'reviewText': ('text', text),
            'summary': ('tips', tips),
            'overall': ('rating', rating)
        }
    )
    if verbose:
        print('datasets loaded')
    item.build_vocab(train)
    if verbose:
        print('item vocab built')
    user.build_vocab(train)
    if verbose:
        print('user vocab built')
    text.build_vocab(train.text, train.tips, min_freq=minimum_frequency)
    if verbose:
        print('text vocab built')
    tips.build_vocab(train.text, train.tips, min_freq=minimum_frequency)
    if verbose:
        print('tips vocab built')
    train_iter, val_iter, test_iter = data.Iterator.splits(
        datasets=(train, val, test),
        batch_sizes=batch_sizes,
        repeat=False,
        sort=False,
        device=device
    )
    return text.vocab, tips.vocab, train_iter, val_iter, test_iter
