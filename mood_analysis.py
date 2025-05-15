from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_mood(text):
    """
    Returns one of:
    joyful, excited, calm, sad, angry, anxious, neutral
    """
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    compound = scores['compound']
    pos = scores['pos']
    neg = scores['neg']
    neu = scores['neu']

    # Fine-grained mood detection
    if compound >= 0.7 and pos > 0.6:
        return "joyful"
    elif 0.4 <= compound < 0.7 and pos > 0.4:
        return "excited"
    elif -0.2 < compound < 0.2 and neu > 0.6:
        return "neutral"
    elif -0.2 < compound < 0.2 and pos > 0.3:
        return "calm"
    elif -0.6 < compound <= -0.2 and neg > 0.4:
        return "sad"
    elif compound <= -0.6 and neg > 0.5:
        return "angry"
    elif neg > 0.35 and compound < -0.3 and pos < 0.2:
        return "anxious"
    else:
        return "calm"
