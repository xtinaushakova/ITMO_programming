from util.classifier import NaiveBayesClassifier
from util.classifier import train_test_split
from util.auxiliary import db_fetch
import util.parameters as param

from logzero import logger

if __name__ == '__main__':

    logger.info('Fetching training data...')
    data = db_fetch(labelled=True)

    logger.info('Splitting into train/test...')
    X, y = data, [news.label for news in data]
    X_train, y_train, X_test, y_test = train_test_split(X, y, random_seed=param.SEED, train_size=param.TRAIN_SIZE)

    logger.info('Fitting NaiveBayes...')
    classifier = NaiveBayesClassifier(alpha=param.ALPHA)
    classifier.fit(X_train, y_train)

    fmt = '\n\t{:10}: Seed\n\t{:10}: Alpha\n\t{:10.0%}: Train rel size (percentile)\n\t{:10.0%}: Accuracy\n\t{:10}: Token cleaning mode\n\t{:10}: Preserve stop-words'

    logger.debug(fmt.format(param.SEED, param.ALPHA, param.TRAIN_SIZE, classifier.score(X_test, y_test), param.TOKEN_CLEANING_MODE, param.PRESERVE_STOP_WORDS))
