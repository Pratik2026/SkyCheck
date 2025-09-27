"""
Intent classification module for the weather chatbot.
Implements hybrid rule-based + LLM classification with confidence scoring.
"""

import re
from typing import Tuple, Optional
from crewai.llm import LLM
import logging

logger = logging.getLogger("jpn_weather_bot.intent_classifier")


class IntentClassifier:
    """
    Hybrid intent classifier using rule-based patterns with LLM fallback.
    """
    
    CONFIDENCE_THRESHOLD = 0.70
    
    # Intent categories
    WEATHER_QUERY = "WEATHER_QUERY"
    GREETING = "GREETING"
    CAPABILITY_INFO = "CAPABILITY_INFO"
    GENERAL_CHAT = "GENERAL_CHAT"
    
    def __init__(self, llm: LLM):
        self.llm = llm
        
        # Weather-related patterns
        self.weather_keywords = [
            # English - Direct weather terms
            'weather', 'temperature', 'temp', 'rain', 'snow', 'sunny', 'cloudy', 
            'forecast', 'climate', 'humidity', 'wind', 'storm', 'thunderstorm',
            'drizzle', 'shower', 'precipitation', 'umbrella', 'coat', 'jacket',
            'hot', 'cold', 'warm', 'cool', 'freezing', 'humid', 'dry',
            # English - Travel/activity weather terms
            'visit', 'trip', 'travel', 'vacation', 'pack', 'wear', 'outdoor',
            'activities', 'sightseeing', 'hiking', 'beach', 'skiing', 'festival',
            # Japanese - Direct weather terms
            '天気', '気温', '雨', '雪', '晴れ', '曇り', '予報', '気候',
            '湿度', '風', '嵐', '雷', '雷雨', '小雨', 'シャワー',
            '降水', '傘', 'コート', 'ジャケット', '暑い', '寒い', 
            '暖かい', '涼しい', '蒸し暑い', '乾燥',
            # Japanese - Travel/activity weather terms
            '訪問', '旅行', '行く', '持参', '着る', 'アウトドア',
            '活動', '観光', 'ハイキング', 'ビーチ', 'スキー', '祭り'
        ]
        
        self.weather_questions = [
            # English patterns - Direct weather questions
            r'how\'?s?\s+(?:the\s+)?weather',
            r'what\'?s?\s+(?:the\s+)?weather',
            r'will\s+it\s+(?:rain|snow)',
            r'is\s+it\s+(?:raining|snowing|sunny|cloudy)',
            r'should\s+i\s+(?:bring|take|wear)',
            r'do\s+i\s+need\s+(?:umbrella|coat|jacket)',
            r'weather\s+(?:in|at|for)',
            r'temperature\s+(?:in|at|for)',
            r'forecast\s+(?:for|in|at)',
            # English patterns - Travel/activity questions that need weather
            r'should\s+i\s+(?:visit|go\s+to|travel\s+to)',
            r'good\s+time\s+to\s+(?:visit|go\s+to|travel)',
            r'planning\s+to\s+(?:visit|go|travel)',
            r'thinking\s+(?:about|of)\s+(?:visiting|going|traveling)',
            r'trip\s+to\s+\w+\s+(?:this|next|during)',
            r'vacation\s+(?:in|to)\s+\w+',
            r'what\s+to\s+(?:wear|pack|bring)\s+(?:in|for|to)',
            r'best\s+time\s+(?:to\s+visit|for)',
            r'outdoor\s+(?:activities|plans)',
            r'(?:hiking|beach|skiing|festival)\s+(?:in|at)',
            # Japanese patterns - Direct weather questions
            r'天気\s*(?:は|です|どう)',
            r'雨\s*(?:降る|です)',
            r'晴れ\s*(?:ます|です)',
            r'傘\s*(?:必要|いる)',
            r'気温\s*(?:は|です)',
            r'予報\s*(?:は|です)',
            r'今日\s*(?:の\s*)?天気',
            r'明日\s*(?:の\s*)?天気',
            # Japanese patterns - Travel/activity questions
            r'行く\s*(?:べき|方が)',
            r'訪問\s*(?:する|すべき)',
            r'旅行\s*(?:する|行く|予定)',
            r'何\s*(?:を\s*)?(?:着る|持参)',
            r'いつ\s*(?:が\s*)?(?:良い|最適)',
            r'アウトドア\s*(?:活動|予定)',
            r'(?:ハイキング|ビーチ|スキー)\s*(?:に|で)'
        ]
        
        # Greeting patterns
        self.greeting_patterns = [
            # English
            r'\b(?:hello|hi|hey|good\s+(?:morning|afternoon|evening)|greetings)\b',
            r'^\s*(?:hi|hello|hey)\s*[!.]*\s*$',
            # Japanese
            r'(?:こんにちは|こんばんは|おはよう|はじめまして|よろしく)',
            r'^\s*(?:こんにちは|おはよう)\s*[!.]*\s*$'
        ]
        
        # Capability/Help patterns
        self.capability_patterns = [
            # English
            r'what\s+(?:can\s+you\s+do|are\s+you)',
            r'how\s+(?:do\s+you\s+work|to\s+use)',
            r'\b(?:help|instructions|guide|features|capabilities)\b',
            r'tell\s+me\s+about\s+(?:yourself|this)',
            # Japanese
            r'何\s*(?:が\s*)?できる',
            r'使い方',
            r'ヘルプ',
            r'機能',
            r'について\s*教えて'
        ]
        
        # General chat patterns  
        self.general_chat_patterns = [
            # English
            r'how\s+are\s+you',
            r'thank\s*you|thanks',
            r'goodbye|bye|see\s+you',
            r'nice\s+to\s+meet',
            r'i\'?m\s+(?:good|fine|okay)',
            # Japanese
            r'元気\s*(?:です|？)',
            r'ありがとう',
            r'さようなら|また(?:ね|今度)',
            r'よろしく',
            r'はじめまして'
        ]
        
        # Location patterns (boost weather confidence)
        self.location_patterns = [
            r'in\s+[A-Z][a-zA-Z\s]+',
            r'at\s+[A-Z][a-zA-Z\s]+',
            r'to\s+[A-Z][a-zA-Z\s]+',
            r'[A-Z][a-zA-Z\s]+\s*(?:の|で|に)',
            r'(?:東京|大阪|京都|名古屋|福岡|札幌|神戸|仙台|広島|北海道)',
            r'(?:Tokyo|Osaka|Kyoto|Nagoya|Fukuoka|Sapporo|Kobe|Sendai|Hiroshima|Delhi|Mumbai|Bangalore|Chennai|Kolkata|Hyderabad|London|Paris|New York|NYC|San Francisco|SF|Los Angeles|LA|Chicago|Boston|Seattle|Miami|Las Vegas)',
            r'(?:India|Japan|USA|UK|France|Germany|Australia|Canada|China|Thailand|Singapore)'
        ]

        # Activity/Decision patterns that often need weather context
        self.activity_decision_patterns = [
            # English
            r'should\s+(?:i|we)\s+(?:go|visit|travel)',
            r'planning\s+(?:a\s+)?(?:trip|visit|vacation)',
            r'good\s+(?:time|day|week)\s+(?:to|for)',
            r'best\s+(?:time|day|season)\s+(?:to|for)',
            r'thinking\s+(?:about|of)\s+(?:going|visiting)',
            r'worth\s+(?:visiting|going)',
            r'outdoor\s+(?:plans|activities)',
            r'what\s+should\s+(?:i|we)\s+(?:wear|pack|bring)',
            # Japanese  
            r'行く\s*(?:べき|方が良い)',
            r'訪問\s*(?:する|すべき)',
            r'計画\s*(?:している|中)',
            r'良い\s*(?:時期|タイミング)',
            r'最適\s*(?:な\s*)?(?:時期|時間)',
            r'考えて\s*(?:いる|います)',
            r'価値\s*(?:ある|がある)',
            r'何\s*(?:を\s*)?(?:着る|持参|持って行く)'
        ]

    def classify_intent_rule_based(self, user_query: str) -> Tuple[str, float]:
        """
        Classify intent using rule-based patterns with confidence scoring.
        
        Args:
            user_query (str): User's input query
            
        Returns:
            Tuple[str, float]: (intent, confidence_score)
        """
        query_lower = user_query.lower().strip()

        weather_score = 0.0
        greeting_score = 0.0
        capability_score = 0.0
        general_chat_score = 0.0

        # Weather keyword scoring
        weather_keyword_count = sum(
            keyword.lower() in query_lower for keyword in self.weather_keywords
        )

        if weather_keyword_count >= 2:
            weather_score += 0.60
        elif weather_keyword_count == 1:
            weather_score += 0.40

        # Weather question patterns
        for pattern in self.weather_questions:
            if re.search(pattern, query_lower, re.IGNORECASE):
                weather_score += 0.50
                break

        # Activity/Decision patterns that need weather context
        activity_match = False
        for pattern in self.activity_decision_patterns:
            if re.search(pattern, query_lower, re.IGNORECASE):
                weather_score += 0.30 
                activity_match = True
                break

        # Location detection and scoring
        location_match = False
        for pattern in self.location_patterns:
            if re.search(pattern, user_query, re.IGNORECASE):
                location_match = True
                weather_score += 0.30 if weather_score > 0 or activity_match else 0.15
                break

        time_indicators = [r'this\s+(?:week|month|year)', r'next\s+(?:week|month)', r'during', r'in\s+(?:january|february|march|april|may|june|july|august|september|october|november|december)', r'今週', r'来週', r'今月', r'来月']
        has_time = any(re.search(pattern, query_lower, re.IGNORECASE) for pattern in time_indicators)

        if activity_match and location_match and has_time:
            weather_score += 0.25

        # Greeting patterns
        for pattern in self.greeting_patterns:
            if re.search(pattern, query_lower, re.IGNORECASE):
                greeting_score += 0.70
                break

        # Capability patterns
        for pattern in self.capability_patterns:
            if re.search(pattern, query_lower, re.IGNORECASE):
                capability_score += 0.70
                break

        # General chat patterns
        for pattern in self.general_chat_patterns:
            if re.search(pattern, query_lower, re.IGNORECASE):
                general_chat_score += 0.70
                break

        # Mixed intent handling - weather priority
        if weather_score > 0 and (greeting_score > 0 or general_chat_score > 0):
            weather_score += 0.20


        scores = {
            self.WEATHER_QUERY: weather_score,
            self.GREETING: greeting_score,
            self.CAPABILITY_INFO: capability_score,
            self.GENERAL_CHAT: general_chat_score
        }

        best_intent = max(scores, key=scores.get)
        confidence = min(scores[best_intent], 0.95)  # Cap at 95%

        logger.debug(f"Rule-based classification: {best_intent} (confidence: {confidence:.2f})")
        logger.debug(f"Scores: {scores}")
        logger.debug(f"Analysis - Activity: {activity_match}, Location: {location_match}, Time: {has_time if 'has_time' in locals() else False}")

        return best_intent, confidence

    def classify_intent_llm(self, user_query: str, language: str) -> str:
        """
        Classify intent using LLM for ambiguous cases.
        
        Args:
            user_query (str): User's input query
            language (str): Detected language ('japanese' or 'english')
            
        Returns:
            str: Classified intent
        """
        prompt = f"""Classify this user query into exactly one category:

WEATHER_QUERY: Questions about weather, temperature, forecasts, weather-related advice, 
OR travel/activity decisions that depend on weather conditions (visiting places, outdoor activities, 
what to wear/pack, best time to visit, etc.)

GREETING: Hello, hi, good morning, introductions  
CAPABILITY_INFO: What can you do, help, features, instructions
GENERAL_CHAT: Casual conversation, how are you, thank you, goodbye

Query: "{user_query}"
Language: {language}

Rules:
- If weather is mentioned alongside other topics, choose WEATHER_QUERY
- Travel questions like "Should I visit X?" are WEATHER_QUERY because weather affects travel decisions
- Activity planning questions that need weather context are WEATHER_QUERY
- Consider context and implied meaning - weather affects many decisions
- Look for location mentions that might indicate weather interest

Respond with only the category name."""

        try:
            response = self.llm.invoke(prompt)
            
            response_clean = response.strip().upper()
            
            if "WEATHER_QUERY" in response_clean:
                return self.WEATHER_QUERY
            elif "GREETING" in response_clean:
                return self.GREETING
            elif "CAPABILITY_INFO" in response_clean:
                return self.CAPABILITY_INFO
            elif "GENERAL_CHAT" in response_clean:
                return self.GENERAL_CHAT
            else:
                logger.warning(f"LLM returned unexpected response: {response}")
                return self.GENERAL_CHAT
                
        except Exception as e:
            logger.error(f"LLM classification failed: {e}")
            return self.GENERAL_CHAT

    def classify_intent(self, user_query: str, language: str) -> str:
        """
        Main intent classification method using hybrid approach.
        
        Args:
            user_query (str): User's input query
            language (str): Detected language ('japanese' or 'english')
            
        Returns:
            str: Final classified intent
        """
        logger.info(f"Classifying intent for query: {user_query[:50]}...")
        
        # Step 1: Rule-based classification
        rule_intent, confidence = self.classify_intent_rule_based(user_query)
        
        # Step 2: Use LLM if confidence is below threshold
        if confidence >= self.CONFIDENCE_THRESHOLD:
            logger.info(f"Rule-based classification successful: {rule_intent} (confidence: {confidence:.2f})")
            return rule_intent
        else:
            logger.info(f"Rule-based confidence too low ({confidence:.2f}), using LLM fallback")
            llm_intent = self.classify_intent_llm(user_query, language)
            logger.info(f"LLM classification result: {llm_intent}")
            return llm_intent


def classify_intent(user_query: str, llm: LLM, language: str = "english") -> str:
    """
    Convenience function for intent classification.
    
    Args:
        user_query (str): User's input query
        llm (LLM): Language model instance
        language (str): Detected language
        
    Returns:
        str: Classified intent
    """
    classifier = IntentClassifier(llm)
    return classifier.classify_intent(user_query, language)