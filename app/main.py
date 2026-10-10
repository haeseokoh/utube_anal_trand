import os
from typing import Optional, List
from fastapi import FastAPI, BackgroundTasks, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from db.database import (
    init_db,
    get_all_videos,
    get_video_by_id,
    get_filter_options,
    get_analyst_opinions
)
from analyzer.trend_analyzer import (
    get_summary_kpis,
    get_surge_keywords,
    get_overall_keyword_trends,
    get_period_comparison,
    get_analyst_matrix,
    get_timeline_trends,
    get_analyst_view_timeline,
    get_available_months,
    get_monthly_analytics
)
from processor.llm_summarizer import (
    summarize_video,
    generate_period_intelligence,
    get_available_models,
    DEFAULT_MODEL
)
from pipeline import run_pipeline

app = FastAPI(
    title="YouTube Economic Analyst Trend Intelligence",
    description="유튜브 주요 경제 분석가들의 시각과 의견을 기간별로 정리한 트렌드 인텔리전스 대시보드 API",
    version="1.0.0"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 디렉토리 설정
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(CURRENT_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def read_root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/api/summary")
def api_summary(
    start_date: Optional[str] = Query(None, description="시작일 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="종료일 (YYYY-MM-DD)")
):
    """상단 핵심 KPI 및 감성 분포 (임의 기간 필터링)"""
    return get_summary_kpis(start_date=start_date, end_date=end_date)

@app.get("/api/periods")
def api_periods():
    """기간별(2024 상반기 vs 하반기 등) 비교 데이터 및 컨센서스"""
    return get_period_comparison()

@app.get("/api/months")
def api_months():
    """수집 및 분석 가능한 모든 연-월 목록 및 통계"""
    return get_available_months()

@app.get("/api/monthly/analysis")
def api_monthly_analysis(month: str = Query("2026-10", description="분석 대상 연-월 (YYYY-MM)")):
    """특정 월에 대한 심층 분석 및 전월(MoM) 대비 트렌드 변화"""
    return get_monthly_analytics(target_month=month)

@app.post("/api/pipeline/monthly")
def api_pipeline_monthly(
    background_tasks: BackgroundTasks,
    month: str = Query("2026-10", description="수집 대상 연-월 (YYYY-MM)")
):
    """특정 월간 타겟 유튜브 수집 및 분석 파이프라인 백그라운드 실행"""
    background_tasks.add_task(run_pipeline, target_month=month)
    return {"status": "started", "message": f"{month} 월간 경제 영상 수집 및 형태소 분석 파이프라인이 시작되었습니다."}


@app.get("/api/surge")
def api_surge(
    period: str = Query("all", description="기간 필터 (all, 2024-H1, 2024-H2 등)"),
    start_date: Optional[str] = Query(None, description="시작일 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="종료일 (YYYY-MM-DD)"),
    top_n: int = Query(15, ge=5, le=50)
):
    """기간별 급상승 키워드 Top N"""
    return get_surge_keywords(period=period, start_date=start_date, end_date=end_date, top_n=top_n)

@app.get("/api/keywords/top")
def api_top_keywords(
    period: str = Query("all", description="기간 필터"),
    start_date: Optional[str] = Query(None, description="시작일 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="종료일 (YYYY-MM-DD)"),
    top_n: int = Query(40, ge=10, le=100)
):
    """워드클라우드 및 전체 상위 키워드 빈도"""
    return get_overall_keyword_trends(period=period, start_date=start_date, end_date=end_date, top_n=top_n)

@app.get("/api/timeline")
def api_timeline():
    """월별/시계열 주요 경제 테마 추이"""
    return get_timeline_trends()

@app.get("/api/analysts/matrix")
def api_analyst_matrix(
    topic: str = Query("all", description="주제 필터"),
    period: str = Query("all", description="기간 필터"),
    start_date: Optional[str] = Query(None, description="시작일 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="종료일 (YYYY-MM-DD)")
):
    """분석가별 스탠스 및 핵심 주장 비교 매트릭스"""
    return get_analyst_matrix(topic=topic, period=period, start_date=start_date, end_date=end_date)

@app.get("/api/analysts/timeline")
def api_analyst_timeline(analyst: Optional[str] = Query(None)):
    """전문가별 시간에 따른 시각 변화(뷰 시프트) 추적 타임라인"""
    return get_analyst_view_timeline(analyst_name=analyst)

@app.post("/api/videos/create")
def api_create_video(payload: dict):
    """전문가 방송 및 의견 수동 아카이브 등록"""
    from db.database import save_video, save_analyst_opinion, save_video_keywords, clear_trend_cache
    from processor.nlp_engine import extract_keywords_and_sentiment
    import time
    
    vid = payload.get("video_id") or f"USR_{int(time.time())}"
    title = payload.get("title", "").strip()
    if not title:
        raise HTTPException(status_code=400, detail="제목은 필수 항목입니다.")
        
    analyst = payload.get("analyst_name", "경제전문가")
    category = payload.get("category", "거시경제/금리")
    published_at = payload.get("published_at") or "2026-10-10"
    url = payload.get("video_url") or f"https://www.youtube.com/watch?v={vid}"
    summary = payload.get("summary_text", "")
    transcript = payload.get("transcript_text", "")
    period = payload.get("period_label", "2026-10")
    
    # Kiwi 형태소 및 감성 분석
    nlp_res = extract_keywords_and_sentiment(f"{title} {summary} {transcript}")
    
    save_video({
        "video_id": vid,
        "title": title,
        "channel_title": payload.get("channel_title", "유튜브 채널"),
        "analyst_name": analyst,
        "category": category,
        "published_at": published_at,
        "video_url": url,
        "summary_text": summary,
        "transcript_text": transcript,
        "sentiment_label": payload.get("sentiment_label") or nlp_res["sentiment_label"],
        "sentiment_score": nlp_res["sentiment_score"],
        "processed": 1
    })
    
    save_video_keywords(vid, nlp_res["keywords"])
    
    topic = payload.get("topic") or category
    core_argument = payload.get("core_argument") or summary
    stance = payload.get("stance") or nlp_res["sentiment_label"].capitalize()
    key_quote = payload.get("key_quote", "")
    
    save_analyst_opinion(
        video_id=vid,
        analyst_name=analyst,
        topic=topic,
        stance=stance,
        core_argument=core_argument,
        key_quote=key_quote,
        period_label=period
    )
    
    clear_trend_cache()
    return {"status": "success", "video_id": vid, "message": "새로운 전문가 영상 및 의견이 등록되었습니다."}

@app.get("/api/videos")
def api_videos(
    category: Optional[str] = Query(None),
    analyst: Optional[str] = Query(None),
    sentiment: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    """필터링 및 검색 조건에 따른 유튜브 영상 목록"""
    return get_all_videos(
        category=category,
        analyst=analyst,
        sentiment=sentiment,
        start_date=start_date,
        end_date=end_date,
        search=search,
        limit=limit,
        offset=offset
    )

@app.get("/api/videos/{video_id}")
def api_video_detail(video_id: str):
    """특정 영상 상세 조회"""
    video = get_video_by_id(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

@app.post("/api/videos/{video_id}/summarize")
def api_summarize_video(
    video_id: str,
    model: str = Query(DEFAULT_MODEL, description="사용할 Ollama 모델명")
):
    """특정 영상 AI 3줄 요약 및 스탠스 분석 (Ollama)"""
    try:
        summary = summarize_video(video_id, model=model)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/intelligence/period")
def api_period_intelligence(
    period: str = Query("all", description="기간 라벨"),
    start_date: Optional[str] = Query(None, description="시작일 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="종료일 (YYYY-MM-DD)"),
    model: str = Query(DEFAULT_MODEL, description="Ollama 모델명")
):
    """기간별 종합 AI 브리핑 및 컨센서스 분석"""
    try:
        return generate_period_intelligence(period_label=period, start_date=start_date, end_date=end_date, model=model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/models")
def api_models():
    """사용 가능한 Ollama LLM 모델 목록"""
    return {"models": get_available_models(), "default": DEFAULT_MODEL}

@app.get("/api/filters")
def api_filters():
    """드롭다운 필터 목록"""
    return get_filter_options()

@app.post("/api/pipeline/run")
def api_run_pipeline(
    background_tasks: BackgroundTasks,
    live_crawl: bool = Query(True, description="유튜브 최신 영상 RSS 크롤링 포함 여부")
):
    """수집 및 분석 파이프라인 백그라운드 실행"""
    background_tasks.add_task(run_pipeline, collect_youtube_live=live_crawl)
    return {"status": "started", "message": "유튜브 수집 및 Kiwi 형태소 분석 파이프라인이 시작되었습니다."}
