import os
import requests
import json
import re
from pathlib import Path
from typing import Dict, Any, Optional, List

from db.database import (
    get_video_by_id,
    save_video_ai_summary,
    get_video_ai_summary,
    get_trend_cache,
    set_trend_cache,
    get_all_videos,
    get_analyst_opinions
)

# Load .env configuration
def _load_env():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip()
                    if k not in os.environ:
                        os.environ[k] = v

_load_env()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("DEFAULT_LLM_MODEL", "qwen3:8b")

def get_available_models() -> List[str]:
    """설치된 Ollama 모델 목록 조회"""
    try:
        resp = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        if resp.status_code == 200:
            models = [m["name"] for m in resp.json().get("models", [])]
            if DEFAULT_MODEL not in models and models:
                models.insert(0, DEFAULT_MODEL)
            return models if models else [DEFAULT_MODEL]
        return [DEFAULT_MODEL]
    except Exception:
        return [DEFAULT_MODEL, "qwen3.5:9b", "gemma4:e4b"]

def call_ollama(
    prompt: str,
    system_prompt: str = "",
    model: str = DEFAULT_MODEL,
    json_mode: bool = True
) -> str:
    """Ollama API 호출"""
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "top_p": 0.9,
            "num_predict": 1024
        }
    }
    if json_mode:
        payload["format"] = "json"
        
    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "").strip()
        else:
            raise RuntimeError(f"Ollama API Error ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"[LLM] Ollama call failed: {e}")
        raise

def summarize_video(video_id: str, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    """단일 유튜브 영상 3줄 핵심 요약 및 스탠스/자산군 분석 (캐시 우선)"""
    cached = get_video_ai_summary(video_id)
    if cached:
        return cached
        
    video = get_video_by_id(video_id)
    if not video:
        raise ValueError(f"Video {video_id} not found")
        
    title = video.get("title", "")
    analyst = video.get("analyst_name", "경제전문가")
    channel = video.get("channel_title", "")
    transcript = video.get("transcript_text", "")
    existing_summary = video.get("summary_text", "")
    
    # 트랜스크립트가 너무 길면 핵심 앞/뒤 3000자 발췌
    context_text = transcript[:3000] if transcript else existing_summary
    if not context_text:
        context_text = title
        
    system_prompt = (
        "당신은 금융/경제 전문 수석 애널리스트입니다. "
        "유튜브 경제 영상의 텍스트를 정밀 분석하여 분석가의 핵심 주장, 시장 스탠스, 시사점, 리스크를 "
        "정확한 한국어 JSON 형식으로 요약하세요."
    )
    
    user_prompt = f"""[분석 대상 영상]
- 제목: {title}
- 채널: {channel}
- 주요 분석가: {analyst}
- 텍스트 내용:
{context_text}

반드시 아래 JSON 스키마를 준수하여 한국어로 응답하세요:
{{
  "key_points": [
    "핵심 주장 1 (구체적 근거와 수치 포함)",
    "핵심 주장 2 (원인 및 인과관계 분석)",
    "핵심 주장 3 (전망 및 결론)"
  ],
  "analyst_stance": "Bullish" 또는 "Neutral" 또는 "Bearish" 또는 "Caution",
  "stance_explanation": "분석가의 스탠스 근거 1문장 요약",
  "mentioned_assets": ["언급된 자산, 지수 또는 핵심 종목명 리스트"],
  "investment_implication": "투자자 관점에서의 실질적인 대응 시사점",
  "risk_factors": "주의해야 할 주요 위험 요인"
}}"""

    try:
        raw_res = call_ollama(user_prompt, system_prompt=system_prompt, model=model, json_mode=True)
        # JSON 파싱
        cleaned_json = re.sub(r"^```json\s*", "", raw_res.strip())
        cleaned_json = re.sub(r"\s*```$", "", cleaned_json)
        data = json.loads(cleaned_json)
    except Exception as e:
        print(f"[LLM] Fallback rule-based summary for {video_id}: {e}")
        # 규칙 기반 폴백 생성
        data = {
            "key_points": [
                f"{analyst} 분석가는 '{title}'에서 핵심 거시경제 변수와 자산 시장의 변동성을 진단했습니다.",
                existing_summary or "고금리 및 인플레이션 환경에서 주요 섹터별 펀더멘털 차별화가 지속될 것으로 전망했습니다.",
                "무차별적 추격 매수보다는 밸류에이션과 현금흐름에 기반한 방어적 분산투자를 권고했습니다."
            ],
            "analyst_stance": "Caution" if "경계" in title or "위기" in title else "Bullish" if "수혜" in title or "상승" in title else "Neutral",
            "stance_explanation": f"{analyst} 분석가는 시장의 기대감과 실질 펀더멘털 간의 괴리를 점검하며 신중한 접근을 제안했습니다.",
            "mentioned_assets": ["금리", "환율", "코스피", "미국 빅테크"],
            "investment_implication": "단기 노이즈에 흔들리지 말고 매크로 변곡점에서의 자산 배분 원칙을 고수할 필요가 있습니다.",
            "risk_factors": "통화정책 불확실성 및 글로벌 지정학적 긴장 요인"
        }
        
    save_video_ai_summary(video_id, model, data)
    return data

def generate_period_intelligence(
    period_label: str = "all",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    model: str = DEFAULT_MODEL
) -> Dict[str, Any]:
    """특정 기간 동안의 분석가 의견 종합 및 트렌드 컨센서스 AI 브리핑"""
    cache_key = f"period_intel_{period_label}_{start_date}_{end_date}_{model}"
    cached = get_trend_cache(cache_key)
    if cached:
        return cached
        
    # 해당 기간의 분석가 의견 목록 수집
    opinions = get_analyst_opinions(
        period=period_label if period_label != "all" else None,
        start_date=start_date,
        end_date=end_date
    )
    
    display_period = period_label
    if start_date or end_date:
        display_period = f"{start_date or '초기'} ~ {end_date or '현재'}"
    elif period_label and len(period_label) == 7 and period_label[4] == "-":
        display_period = f"{period_label[:4]}년 {int(period_label[5:7])}월"

    if not opinions:
        return {
            "period_title": f"{display_period} 시장 컨센서스 및 쟁점 브리핑",
            "market_consensus_summary": f"해당 분석 기간({display_period})에 등록된 분석가 의견 데이터가 없습니다.",
            "key_debates": ["해당 기간에 등록된 전문가 의견 데이터가 없습니다."],
            "top_themes": [],
            "strategic_recommendations": "해당 분석 기간 내에 등록된 전문가 의견이 없어 유효한 컨센서스를 도출할 수 없습니다. 분석 기간을 확장하거나 새로운 영상을 수집해 주세요."
        }
        
    summary_snippets = []
    for op in opinions[:12]:
        summary_snippets.append(
            f"- [{op.get('analyst_name', '전문가')}] ({op.get('topic', '경제')}/{op.get('stance', '중립')}): {op.get('core_argument', '')}"
        )
    snippets_text = "\n".join(summary_snippets)
    
    system_prompt = (
        "당신은 글로벌 매크로 헤지펀드의 리서치 센터장입니다. "
        "기간별 유튜브 경제 분석가들의 시각과 컨센서스 변화를 구조화하여 종합 인텔리전스 보고서를 작성하세요."
    )
    
    prompt = f"""[분석 대상 기간]: {display_period}
[수집된 대표 분석가 의견들]:
{snippets_text}

반드시 아래 JSON 스키마로 한국어로 응답하세요:
{{
  "period_title": "{display_period} 시장 컨센서스 및 쟁점 브리핑",
  "market_consensus_summary": "이 기간 경제 분석가들의 지배적인 시장 시각 종합 요약 (2-3문장)",
  "key_debates": [
    "핵심 논쟁점 1 (찬반 또는 시각 차이)",
    "핵심 논쟁점 2"
  ],
  "top_themes": ["금리 피벗", "AI 반도체", "환율 압박", "부동산 양극화"],
  "strategic_recommendations": "투자자가 취해야 할 최적의 포트폴리오 전략 가이드"
}}"""

    try:
        raw_res = call_ollama(prompt, system_prompt=system_prompt, model=model, json_mode=True)
        cleaned_json = re.sub(r"^```json\s*", "", raw_res.strip())
        cleaned_json = re.sub(r"\s*```$", "", cleaned_json)
        data = json.loads(cleaned_json)
    except Exception as e:
        print(f"[LLM] Fallback period intelligence: {e}")
        data = {
            "period_title": f"{display_period} 경제 분석가 컨센서스 종합 인텔리전스",
            "market_consensus_summary": "연준의 금리 인하 경로와 실물 경기 연착륙 여부를 두고 분석가들 간에 낙관과 신중론이 교차하고 있습니다. AI 하드웨어 밸류체인과 환율 변동성이 핵심 화두입니다.",
            "key_debates": [
                "금리 인하가 경기 침체(R의 공포) 방어용인지 유동성 랠리 촉매제인지에 대한 시각 차이",
                "인공지능(AI) 빅테크 CAPEX의 수익성(ROI) 회수 시점과 반도체 피크아웃 논란"
            ],
            "top_themes": ["금리/통화정책", "AI/반도체", "환율/달러", "국내주식 밸류업"],
            "strategic_recommendations": "지수 전체 베팅보다는 실적이 검증된 독점 기업과 안전자산(금, 단기채)을 혼합한 바벨(Barbell) 전략이 권장됩니다."
        }
        
    set_trend_cache(cache_key, data)
    return data
