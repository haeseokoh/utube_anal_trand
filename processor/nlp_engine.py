import re
from typing import List, Dict, Tuple, Set, Any
import kiwipiepy

# Kiwi 형태소 분석기 인스턴스
_kiwi_instance = None

def get_kiwi():
    global _kiwi_instance
    if _kiwi_instance is None:
        _kiwi_instance = kiwipiepy.Kiwi()
        # 사용자 정의 경제 전문 용어 등록
        economic_terms = [
            ("밸류업", "NNP"), ("코리아디스카운트", "NNG"), ("HBM", "SL"),
            ("빅컷", "NNG"), ("삼의법칙", "NNP"), ("스트레스DSR", "NNP"),
            ("라스트마일", "NNG"), ("금투세", "NNP"), ("엔비디아", "NNP"),
            ("하이닉스", "NNP"), ("삼성전자", "NNP"), ("쿠다", "NNP"),
            ("서학개미", "NNG"), ("장단기금리차", "NNG"), ("블랙웰", "NNP"),
            ("HBM4", "SL"), ("루빈", "NNP"), ("중립금리", "NNG"),
            ("SMR", "SL"), ("피지컬AI", "NNG"), ("입주절벽", "NNG"),
            ("기저부하", "NNG"), ("휴머노이드", "NNG")
        ]

        for word, tag in economic_terms:
            try:
                _kiwi_instance.add_user_word(word, tag)
            except Exception:
                pass
    return _kiwi_instance

# 불용어(Stopwords) 정의 (유튜브 진행 멘트 및 일반 잡음 단어)
STOPWORDS: Set[str] = {
    "영상", "오늘", "생각", "말씀", "채널", "구독", "좋아요", "지금", "관련", "때문",
    "부분", "경우", "사실", "이제", "진짜", "우리", "정도", "이것", "그것", "저것",
    "사람", "하나", "이야기", "정도", "모습", "상황", "자신", "시간", "시작", "결국",
    "자체", "이유", "이후", "동안", "가장", "어제", "내일", "이번", "지난", "다음",
    "대한", "통해", "위해", "대해", "기준", "내용", "가지", "바로", "다시", "누구",
    "무엇", "여기", "저기", "어디", "그때", "이때", "모두", "모든", "어떤", "다른",
    "정말", "매우", "너무", "조금", "많이", "점점", "계속", "항상", "가장", "다시"
}

# 감성/스탠스 어휘 사전
BULLISH_KEYWORDS = {
    "상승": 1.2, "랠리": 1.5, "신고가": 1.5, "수혜": 1.2, "호재": 1.4,
    "호실적": 1.5, "성장": 1.0, "턴어라운드": 1.5, "반등": 1.2, "매수": 1.0,
    "기대": 0.8, "돌파": 1.2, "완판": 1.4, "개선": 1.0, "서프라이즈": 1.4,
    "낙관": 1.2, "유망": 1.0, "혁신": 1.0, "독점": 1.2, "재평가": 1.2,
    "호황": 1.4, "폭등": 1.3, "회복": 1.0, "우상향": 1.4
}

BEARISH_KEYWORDS = {
    "하락": -1.2, "급락": -1.5, "침체": -1.5, "폭락": -1.5, "위기": -1.4,
    "부도": -1.6, "손실": -1.2, "둔화": -1.0, "충격": -1.3, "쇼크": -1.4,
    "붕괴": -1.6, "저점": -0.8, "공포": -1.3, "매도": -1.0, "악재": -1.4,
    "피크아웃": -1.4, "부실": -1.3, "적자": -1.2, "파산": -1.6, "고갈": -1.2,
    "디플레이션": -1.3, "절벽": -1.3, "불황": -1.4, "우려": -0.8
}

CAUTION_KEYWORDS = {
    "경계": -0.4, "신중": -0.3, "관망": 0.0, "변동성": -0.4, "불확실": -0.6,
    "보수적": -0.3, "경계감": -0.5, "리스크": -0.6, "압박": -0.5, "끈적": -0.4,
    "지연": -0.4, "혼조": -0.2, "주의": -0.5, "부담": -0.5, "조정": -0.3
}

def extract_keywords_and_sentiment(text: str, top_n: int = 30) -> Dict[str, Any]:
    """
    텍스트에서 Kiwi를 활용한 핵심 명사/영어 약어 추출 및 감성 스탠스 산출
    """
    if not text:
        return {
            "keywords": {},
            "sentiment_label": "neutral",
            "sentiment_score": 0.0,
            "keyword_counts": {}
        }
        
    kiwi = get_kiwi()
    tokens = kiwi.tokenize(text)
    
    keyword_freq: Dict[str, int] = {}
    bullish_score = 0.0
    bearish_score = 0.0
    caution_score = 0.0
    
    for t in tokens:
        form = t.form.strip()
        tag = t.tag
        
        # 1. 명사(NNG, NNP) 및 외국어/알파벳(SL)
        if tag in ("NNG", "NNP", "SL") and len(form) >= 2:
            form_upper = form.upper() if tag == "SL" else form
            if form not in STOPWORDS and form_upper not in STOPWORDS:
                keyword_freq[form_upper] = keyword_freq.get(form_upper, 0) + 1
                
        # 2. 감성 키워드 점수 가산
        if form in BULLISH_KEYWORDS:
            bullish_score += BULLISH_KEYWORDS[form]
        elif form in BEARISH_KEYWORDS:
            bearish_score += abs(BEARISH_KEYWORDS[form])
        elif form in CAUTION_KEYWORDS:
            caution_score += abs(CAUTION_KEYWORDS[form])
            
    # 상위 N개 키워드 추출
    sorted_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
    top_keywords_dict = dict(sorted_keywords)
    
    # 종합 스탠스 및 점수 계산
    net_score = (bullish_score - bearish_score)
    total_sentiment_tokens = bullish_score + bearish_score + caution_score
    
    if total_sentiment_tokens > 0:
        normalized_score = max(-1.0, min(1.0, net_score / total_sentiment_tokens))
    else:
        normalized_score = 0.0
        
    if normalized_score > 0.25:
        label = "bullish"
    elif normalized_score < -0.25:
        label = "bearish"
    elif caution_score > (bullish_score + bearish_score) * 0.5 and caution_score > 1.5:
        label = "caution"
    else:
        label = "neutral"
        
    return {
        "keywords": top_keywords_dict,
        "sentiment_label": label,
        "sentiment_score": round(normalized_score, 2),
        "bullish_weight": round(bullish_score, 2),
        "bearish_weight": round(bearish_score, 2),
        "caution_weight": round(caution_score, 2)
    }
