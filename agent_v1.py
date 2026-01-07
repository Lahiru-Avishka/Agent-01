from enum import Enum
def my_trade_agent(coin_pair):
    
    news_list = browse_web_for_trading_info(f"latest news on {coin_pair}") # 1st Step
    relevant_news = filter_relevent_news(news_list, coin_pair) # 2nd Step
    news_knowledge = extract_knoladge_from_news(relevant_news) # 3rd Step
    trade_decision = make_trade_decision(coin_pair, news_knowledge) # 4th Step
    
    return trade_decision
    
    
def browse_web_for_trading_info(query):
    return f"Browsing the web for information on: {query}"

def filter_relevent_news(news_list, coin_pair):
    return []


class Sentiment(Enum):
    NEUTRAL = "neutral"
    POSITIVE = "positive"
    NEGATIVE = "negative"

def extract_knoladge_from_news(news) -> Sentiment:
    return Sentiment.NEUTRAL 

def make_trade_decision(coin_pair, news_knowledge):
    return {
        "signal": "hold",
        "confidence": 0.5,
        "action_time": "12:00",
    }
    
if __name__ == "__main__":
    decision = my_trade_agent("EUR/USD")
    print(decision)  