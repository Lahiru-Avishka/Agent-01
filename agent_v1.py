from enum import Enum
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re

def my_trade_agent(coin_pair):
    """
    Main trading agent function that follows a 4-step process:
    1. Browse web for trading news
    2. Filter relevant news for the coin pair
    3. Extract sentiment knowledge from news
    4. Make trading decision based on sentiment
    """
    try:
        news_list = browse_web_for_trading_info(f"latest news on {coin_pair}")  # 1st Step
        relevant_news = filter_relevent_news(news_list, coin_pair)  # 2nd Step
        news_knowledge = extract_knoladge_from_news(relevant_news)  # 3rd Step
        trade_decision = make_trade_decision(coin_pair, news_knowledge)  # 4th Step
        
        return trade_decision
    except Exception as e:
        return {
            "signal": "error",
            "confidence": 0.0,
            "action_time": datetime.now().strftime("%H:%M"),
            "error": str(e)
        }
    
    
def browse_web_for_trading_info(query):
    """
    Browse forex news RSS feed and extract news items
    Returns list of NewsLink objects
    """
    try:
        result = requests.get(
            "https://www.myfxbook.com/rss/latest-forex-news", 
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
            },
            timeout=10
        )
        
        if result.status_code != 200:
            print(f"Error fetching RSS feed: {result.status_code}")
            return []
        
        soup = BeautifulSoup(result.content, 'xml')
        items = soup.find_all('item')
        
        news_links = []
        for item in items:
            try:
                title = item.title.text if item.title else "No title"
                link = item.link.text if item.link else ""
                description = item.description.text if item.description else ""
                pubdate = item.pubDate.text if item.pubDate else ""
                
                news_link = NewsLink(title, link, description, pubdate)
                news_links.append(news_link)
                
            except AttributeError as e:
                continue
        
        print(f"Found {len(news_links)} news items from RSS feed")
        return news_links
        
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return []
    except Exception as e:
        print(f"Error parsing RSS: {e}")
        return []


def filter_relevent_news(news_list, coin_pair):
    """
    Filter news list to only include items relevant to the coin pair
    """

from groq import Groq

client = Groq()
completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
      {
        "role": "user",
        "content": ""
      }
    ],
    temperature=1,
    max_completion_tokens=8192,
    top_p=1,
    reasoning_effort="medium",
    stream=True,
    stop=None
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")


    
    relevant = []
    coin_keywords = [coin_pair.upper(), coin_pair.lower()]
    
    # Also check for individual currency components
    if '/' in coin_pair:
        base, quote = coin_pair.split('/')
        coin_keywords.extend([base.upper(), base.lower(), quote.upper(), quote.lower()])
    
    for news in news_list:
        # Check if coin pair or its components appear in title or description
        for keyword in coin_keywords:
            if (keyword in news.title or keyword in news.description):
                relevant.append(news)
                break  # Found match, no need to check other keywords
    
    print(f"Filtered to {len(relevant)} relevant news items for {coin_pair}")



class Sentiment(Enum):
    NEUTRAL = "neutral"
    POSITIVE = "positive"
    NEGATIVE = "negative"

class NewsLink:
    def __init__(self, title, link, description, pubdate):
        self.title = title
        self.link = link
        self.description = description
        self.pubdate = pubdate
    
    def __str__(self):
        return f"Title: {self.title[:50]}..."
    
    def __repr__(self):
        return f"NewsLink({self.title[:30]}...)"


def extract_knoladge_from_news(news) -> Sentiment:
    """
    Analyze news sentiment using keyword-based analysis
    Returns: Sentiment enum (POSITIVE, NEGATIVE, or NEUTRAL)
    """
    if not news:
        print("No news provided for sentiment analysis")
        return Sentiment.NEUTRAL
    
    positive_keywords = [
        'bullish', 'strong', 'growth', 'gain', 'rise', 'up', 'positive', 'buy', 
        'strengthen', 'recovery', 'optimistic', 'outlook', 'boost', 'rally',
        'exceed', 'beat', 'outperform', 'higher', 'surge', 'increase'
    ]
    
    negative_keywords = [
        'bearish', 'weak', 'fall', 'drop', 'down', 'negative', 'sell', 'weaken',
        'decline', 'loss', 'pessimistic', 'concern', 'worry', 'risk', 'plunge',
        'downturn', 'lower', 'decrease', 'slump', 'recession', 'crisis'
    ]
    
    combined_text = ""
    for news_item in news:
        combined_text += f"{news_item.title} {news_item.description} "
    
    # Clean and normalize text
    combined_text = combined_text.lower()
    
    # Count keyword occurrences
    pos_count = sum(1 for word in positive_keywords if word in combined_text)
    neg_count = sum(1 for word in negative_keywords if word in combined_text)
    
    print(f"Sentiment analysis: Positive words={pos_count}, Negative words={neg_count}")
    
    # Determine sentiment
    if pos_count > neg_count and pos_count > 0:
        return Sentiment.POSITIVE
    elif neg_count > pos_count and neg_count > 0:
        return Sentiment.NEGATIVE
    else:
        return Sentiment.NEUTRAL


def make_trade_decision(coin_pair, news_knowledge):
    """
    Make trading decision based on sentiment analysis
    """
    current_time = datetime.now().strftime("%H:%M")
    
    if news_knowledge == Sentiment.POSITIVE:
        return {
            "coin_pair": coin_pair,
            "signal": "buy",
            "confidence": 0.75,
            "action_time": current_time,
            "sentiment": "positive",
            "reason": "Positive news sentiment detected"
        }
    elif news_knowledge == Sentiment.NEGATIVE:
        return {
            "coin_pair": coin_pair,
            "signal": "sell",
            "confidence": 0.65,
            "action_time": current_time,
            "sentiment": "negative",
            "reason": "Negative news sentiment detected"
        }
    else:  # NEUTRAL
        return {
            "coin_pair": coin_pair,
            "signal": "hold",
            "confidence": 0.5,
            "action_time": current_time,
            "sentiment": "neutral",
            "reason": "Neutral or insufficient news sentiment"
        }
    
    
if __name__ == "__main__":
    # Test with multiple currency pairs
    test_pairs = ["EUR/USD", "GBP/USD", "USD/JPY"]
    
    for pair in test_pairs:
        print(f"\n{'='*50}")
        print(f"Analyzing {pair}...")
        decision = my_trade_agent(pair)
        print(f"Decision: {decision}")
        print(f"{'='*50}\n")