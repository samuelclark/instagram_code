import pattern.en as paten
import pattern.vector as patvec
import nltk

__author__ = 'Sam'

# NP = emoticons


def pos_feature_builder(
        text, target_pos=('JJ', 'NN', 'VB', '!', 'NP', 'RB', 'CD')):
    """
        builds features from target part of speech tags specified by <target_pos>
    """
    if not text:
        return patvec.count([])
    try:

        parsed_text = paten.parsetree(text, lemmata=True)[0]
        selected = [
            word.lemma for word in parsed_text if word.tag.startswith(
                target_pos)]
    except IndexError as e:
        print text, e
        selected = []
    result = patvec.count(selected)
    return result


def postag_feature_builder(
        text, target_pos=('JJ', 'NN', 'VB', 'NP', 'RB', 'CD')):
    """
        faster version of the tag feature builder
        uses paten.tag instead of paten.parsetree
    """
    if not text:
        return {}
    # tag each word
    try:
        result = patvec.count(
            (word for word,
             tag in paten.tag(text,
                              tokenize=True,
                              encoding='utf-8') if tag in target_pos))
    except IndexError as e:
        print text, e
        result = {}
    return result


def unigram_text_feature(text):
    """
        return probability distribution {term: count} of each word in <text>
    """
    features = patvec.count(nltk.word_tokenize(text.lower()))
    return features


def bigram_text_feature(text):
    """
        return probability distribution {term: count} of each word in <text>
    """
    wl = nltk.word_tokenize(text.lower())
    bigrams = nltk.util.bigrams(wl)
    features = patvec.count(bigrams)
    return features


def trigram_text_feature(text):
    """
        return probability distribution {term: count} of each word in <text>
    """
    wl = nltk.word_tokenize(text.lower())
    trigrams = nltk.util.trigrams(wl)
    features = patvec.count(trigrams)
    return features


def unigram_bigram_text_feature(text):
    """
        combine unigram and bigram text features and return the joined dictionary
    """
    unigram_features = unigram_text_feature(text)
    bigram_features = bigram_text_feature(text)
    combined_features = unigram_features.copy()
    combined_features.update(bigram_features)

    return combined_features


test = "Be good with the clock because if you go too fast with the clock you are going to suck"
test2 = "Replacement for the best slinger in the World"


r1 = pos_feature_builder(test)
r2 = pos_feature_builder(test2)
