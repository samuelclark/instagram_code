instagram_code
==============

This project which I worked on from August to the end of September uses soft polarity labels as noisy indicators of sentiment in instagram comments / captions.

I collected over total 1 million instagram from tags =
['happy','sad', 'good', 'bad', 'fun', 'bored', 'love', 'hate', 'awesome', 'sucks', 'cool', 'stupid', 'want','ugly', 'beautiful'].

By associating the text of the "grams" caption + comments with the soft-label, I built a polarity classifier that achieved 76% accuracy on a current Twitter gold-standard test set.


Future work includes improving the classifier, reducing noise in the training set, and developing models based on other features. For example a classifier that determined the filter used on the image based on text performed surpisingly well.
Similarly there are oppertunities to build an image polarity classifier using some computer vision.


I hope to get back to it soon.
