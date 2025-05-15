import nltk

# Download the VADER lexicon (necessary in cloud environments like Streamlit Cloud)
nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_mood(text):
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.5:
        return 'happy'
    elif compound >= 0.1:
        return 'calm'
    elif compound <= -0.5:
        return 'angry'
    elif compound <= -0.1:
        return 'sad'
    else:
        return 'neutral'
