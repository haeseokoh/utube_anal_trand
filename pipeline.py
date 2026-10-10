import os
import sys
from typing import Dict, Any

from db.database import (
    init_db,
    get_connection,
    update_video_nlp_status,
    save_video_keywords,
    clear_trend_cache
)
from crawler.youtube_collector import (
    initialize_seed_database,
    collect_latest_youtube_videos,
    collect_by_month
)
from processor.nlp_engine import extract_keywords_and_sentiment
from analyzer.trend_analyzer import get_summary_kpis

def run_pipeline(
    collect_youtube_live: bool = False,
    target_month: str = None,
    limit_per_channel: int = 3
) -> Dict[str, Any]:
    """
    유튜브 경제 트렌드 전체 파이프라인 실행
    1. DB 초기화
    2. 시드 데이터 적재
    3. (선택) 유튜브 실시간 또는 특정 월별 RSS 수집 및 자막 추출
    4. Kiwi 형태소 분석 및 감성/스탠스 산출
    5. 트렌드 집계 캐시 갱신
    """
    print("=" * 60)
    print(">> [Pipeline] 유튜브 경제 분석가 트렌드 파이프라인 시작")
    print("=" * 60)
    
    # 1. DB 초기화
    init_db()
    
    # 2. 시드 데이터 적재
    seed_count = initialize_seed_database()
    print(f">> [Pipeline] 시드 데이터 처리 완료 ({seed_count}건 신규 적재)")
    
    # 3. 실시간 유튜브 최신 영상 또는 특정 월 영상 수집 (선택)
    if target_month:
        print(f">> [Pipeline] '{target_month}' 월간 경제 영상 수집 중...")
        month_count = collect_by_month(target_month=target_month, limit_per_channel=limit_per_channel)
        print(f">> [Pipeline] '{target_month}' 월간 수집 완료 ({month_count}건 신규 수집)")
    elif collect_youtube_live:
        print(f">> [Pipeline] 유튜브 최신 경제 영상 RSS 수집 중 (채널당 {limit_per_channel}건)...")
        live_count = collect_latest_youtube_videos(limit_per_channel=limit_per_channel)
        print(f">> [Pipeline] 유튜브 라이브 수집 완료 ({live_count}건 신규 수집)")

        
    # 4. Kiwi 형태소 분석 및 키워드 추출 (미처리 영상 대상)
    print(">> [Pipeline] Kiwi 형태소 분석 및 감성 스탠스 산출 중...")
    processed_count = 0
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT video_id, title, transcript_text, summary_text FROM videos WHERE processed = 0 OR processed = 1")
        rows = cursor.fetchall()
        
        for row in rows:
            vid = row[0]
            title = row[1]
            transcript = row[2] or ""
            summary = row[3] or ""
            
            # 분석 대상 텍스트: 검증된 실제 자막 원문이 있으면 제목과 자막을 사용하고, 자막이 없으면 원본 제목만 사용 (생성된 요약문 배제)
            source_text = f"{title} {transcript}" if (transcript and len(transcript.strip()) > 30) else title
            nlp_res = extract_keywords_and_sentiment(source_text, top_n=30)
            
            # 키워드 저장
            save_video_keywords(vid, nlp_res["keywords"])
            
            # 영상 상태 업데이트
            update_video_nlp_status(
                video_id=vid,
                processed=1,
                sentiment_label=nlp_res["sentiment_label"],
                sentiment_score=nlp_res["sentiment_score"]
            )
            processed_count += 1
            
    print(f">> [Pipeline] 총 {processed_count}건의 영상 형태소 및 감성 분석 완료.")
    
    # 5. 캐시 초기화
    clear_trend_cache()
    
    kpis = get_summary_kpis()
    print(f">> [Pipeline] 파이프라인 성공적으로 종료! (보유 영상: {kpis['total_videos']}개, 분석가: {kpis['total_analysts']}명)")
    return kpis

if __name__ == "__main__":
    run_pipeline(collect_youtube_live=False)
