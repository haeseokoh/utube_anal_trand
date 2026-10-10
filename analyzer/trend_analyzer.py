import sqlite3
from typing import List, Dict, Any, Optional
from collections import defaultdict
from db.database import get_connection, get_trend_cache, set_trend_cache

def get_summary_kpis(start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
    """대시보드 상단 핵심 KPI 통계 (임의 기간 필터링 지원)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        where = "WHERE 1=1"
        params = []
        if start_date:
            where += " AND published_at >= ?"
            params.append(start_date)
        if end_date:
            where += " AND published_at <= ?"
            params.append(end_date)
        
        # 총 영상 수 및 분석가 수
        cursor.execute(f"SELECT COUNT(*), COUNT(DISTINCT analyst_name), COUNT(DISTINCT channel_title) FROM videos {where}", params)
        total_videos, total_analysts, total_channels = cursor.fetchone()
        
        # 감성/스탠스 분포
        cursor.execute(f"SELECT sentiment_label, COUNT(*) FROM videos {where} GROUP BY sentiment_label", params)
        sentiment_counts = {r[0]: r[1] for r in cursor.fetchall() if r[0]}
        
        # 최다 언급 주제/카테고리
        cursor.execute(f"SELECT category, COUNT(*) as cnt FROM videos {where} GROUP BY category ORDER BY cnt DESC LIMIT 1", params)
        top_cat_row = cursor.fetchone()
        top_category = top_cat_row[0] if top_cat_row else "거시경제/금리"
        
        # 총 조회수
        cursor.execute(f"SELECT SUM(view_count) FROM videos {where}", params)
        total_views = cursor.fetchone()[0] or 0
        
        return {
            "total_videos": total_videos,
            "total_analysts": total_analysts,
            "total_channels": total_channels,
            "sentiment_distribution": {
                "bullish": sentiment_counts.get("bullish", 0),
                "neutral": sentiment_counts.get("neutral", 0),
                "caution": sentiment_counts.get("caution", 0),
                "bearish": sentiment_counts.get("bearish", 0)
            },
            "top_category": top_category,
            "total_views": total_views
        }

def get_surge_keywords(
    period: str = "all",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    top_n: int = 15
) -> List[Dict[str, Any]]:
    """급상승(Surge) 키워드 산출 (자유 기간 및 특정 월 지원)"""
    cache_key = f"surge_kw_{period}_{start_date}_{end_date}_{top_n}"
    cached = get_trend_cache(cache_key)
    if cached:
        return cached
        
    with get_connection() as conn:
        cursor = conn.cursor()
        
        where = "WHERE 1=1"
        params = []
        if start_date:
            where += " AND v.published_at >= ?"
            params.append(start_date)
        if end_date:
            where += " AND v.published_at <= ?"
            params.append(end_date)
            
        if (not start_date and not end_date) and period and period not in ("all", "custom", "recent-3m"):
            if len(period) == 7 and period[4] == "-":
                where += " AND SUBSTR(v.published_at, 1, 7) = ?"
                params.append(period)
            else:
                where += " AND (o.period_label = ? OR SUBSTR(v.published_at, 1, 7) = ?)"
                params.extend([period, period])
                
        query = f"""
            SELECT k.keyword, SUM(k.count) as total_count, COUNT(DISTINCT k.video_id) as doc_freq
            FROM video_keywords k
            JOIN videos v ON k.video_id = v.video_id
            LEFT JOIN analyst_opinions o ON v.video_id = o.video_id
            {where}
            GROUP BY k.keyword
            ORDER BY total_count DESC, doc_freq DESC
            LIMIT ?
        """
        params.append(top_n)
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # 점수 산출
        results = []
        max_count = rows[0][1] if rows else 1
        for rank, row in enumerate(rows, 1):
            kw, count, doc_freq = row[0], row[1], row[2]
            surge_score = round((count / max_count) * 100, 1)
            results.append({
                "rank": rank,
                "keyword": kw,
                "count": count,
                "doc_freq": doc_freq,
                "surge_score": surge_score
            })
            
    set_trend_cache(cache_key, results)
    return results

def get_overall_keyword_trends(
    period: str = "all",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    top_n: int = 40
) -> List[Dict[str, Any]]:
    """워드클라우드 및 상위 키워드 차트용 데이터 (자유 기간 지원)"""
    cache_key = f"top_kw_{period}_{start_date}_{end_date}_{top_n}"
    cached = get_trend_cache(cache_key)
    if cached:
        return cached
        
    with get_connection() as conn:
        cursor = conn.cursor()
        
        where = "WHERE 1=1"
        params = []
        if start_date:
            where += " AND v.published_at >= ?"
            params.append(start_date)
        if end_date:
            where += " AND v.published_at <= ?"
            params.append(end_date)
            
        if (not start_date and not end_date) and period and period not in ("all", "custom", "recent-3m"):
            if len(period) == 7 and period[4] == "-":
                where += " AND SUBSTR(v.published_at, 1, 7) = ?"
                params.append(period)
            else:
                where += " AND (o.period_label = ? OR SUBSTR(v.published_at, 1, 7) = ?)"
                params.extend([period, period])
                
        query = f"""
            SELECT k.keyword, SUM(k.count) as total_count
            FROM video_keywords k
            JOIN videos v ON k.video_id = v.video_id
            LEFT JOIN analyst_opinions o ON v.video_id = o.video_id
            {where}
            GROUP BY k.keyword
            ORDER BY total_count DESC
            LIMIT ?
        """
        params.append(top_n)
        cursor.execute(query, params)
        rows = cursor.fetchall()
        results = [{"text": r[0], "size": r[1]} for r in rows]
        
    set_trend_cache(cache_key, results)
    return results



def get_period_comparison() -> Dict[str, Any]:
    """기간별(2024 상반기 vs 하반기 등) 스탠스 및 핵심 화두 변천사 비교"""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # 기간별 영상 수 및 스탠스 분포
        cursor.execute("""
            SELECT o.period_label, v.sentiment_label, COUNT(*)
            FROM videos v
            JOIN analyst_opinions o ON v.video_id = o.video_id
            GROUP BY o.period_label, v.sentiment_label
        """)
        period_data = defaultdict(lambda: {"bullish": 0, "neutral": 0, "caution": 0, "bearish": 0, "total": 0})
        for row in cursor.fetchall():
            period, sentiment, cnt = row[0], row[1], row[2]
            if period:
                period_data[period][sentiment] += cnt
                period_data[period]["total"] += cnt
                
        # 기간별 핵심 화두 키워드 Top 5
        period_keywords = {}
        for period in period_data.keys():
            cursor.execute("""
                SELECT k.keyword, SUM(k.count) as cnt
                FROM video_keywords k
                JOIN videos v ON k.video_id = v.video_id
                JOIN analyst_opinions o ON v.video_id = o.video_id
                WHERE o.period_label = ?
                GROUP BY k.keyword
                ORDER BY cnt DESC
                LIMIT 5
            """, (period,))
            period_keywords[period] = [r[0] for r in cursor.fetchall()]
            
        # 기간별 대표 분석가 합의 요약 매핑
        period_summaries = {
            "2026-10": {
                "theme": "연준 중립금리 안착, HBM4·피지컬 AI 로봇 실적 랠리, 금 3,000$ 돌파",
                "consensus": "2026년 10월 현재 연준의 중립금리 도달에 따른 추가 금리 인하 제한 및 2차 인플레 경계. HBM4 양산과 피지컬 AI(휴머노이드) 실적 확인 장세, 글로벌 탈달러화와 금 3,000달러 돌파, 서울 신축 입주 절벽 현실화."
            },
            "2026-09": {
                "theme": "FOMC 중립금리 3.25% 선언, 피지컬 AI 부품 공급망, 빅테크-원전 PPA",
                "consensus": "연준의 중립금리 영역 안착 공식화. 테슬라 옵티머스 등 휴머노이드 로봇 공장 투입에 따른 부품사 실적 폭증, 데이터센터 전력 대란 해결을 위한 SMR 원전 수주 잭팟."
            },
            "2026-08": {
                "theme": "유가 80$ 재진입과 금리 인하 속도 조절 경계, HBM4 샘플 승인",
                "consensus": "중동 긴장에 따른 유가 반등과 물가 반등 우려. 차세대 HBM4 엔지니어링 샘플 승인과 가을 이사철 서울 아파트 전세 매물 품귀 현상 가시화."
            },
            "2026-H1": {
                "theme": "글로벌 환율 재편 & 코스피 3,200선 돌파 시도",
                "consensus": "일본은행 금리 인상과 엔화 변동성, 밸류업 2년차 주주환원 우수 기업 중심의 코스피 레벨업 및 미국 반도체 수출 호조 지속."
            },
            "2024-H2": {
                "theme": "연준 50bp 빅컷, 경기침체(R의 공포) vs 연착륙 공방",
                "consensus": "연준의 선제적 빅컷 단행과 노동시장 둔화. HBM 반도체 차별화 및 미국 대선 리스크, 환율 1400원선 공방과 부동산 DSR 규제 강화."
            },
            "2024-H1": {
                "theme": "고금리 장기화(Higher for Longer) & AI 엔비디아 독주",
                "consensus": "인플레이션 하방 경직성으로 연준의 조기 인하 기대 축소. AI 데이터센터 및 전력망 인프라 폭증과 코스피 저PBR 밸류업 프로그램 관심 집중."
            }
        }
        
        return {
            "periods": dict(period_data),
            "period_keywords": period_keywords,
            "period_summaries": period_summaries
        }

def get_available_months() -> List[Dict[str, Any]]:
    """수집 및 분석 가능한 모든 연-월(YYYY-MM) 목록과 통계"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SUBSTR(published_at, 1, 7) as ym,
                   COUNT(*) as video_cnt,
                   COUNT(DISTINCT analyst_name) as analyst_cnt,
                   SUM(view_count) as total_views
            FROM videos
            WHERE published_at IS NOT NULL AND published_at != ''
            GROUP BY ym
            ORDER BY ym DESC
        """)
        rows = cursor.fetchall()
        results = []
        for r in rows:
            ym = r[0]
            if len(ym) == 7:
                y, m = ym.split("-")
                label = f"{y}년 {int(m)}월"
                results.append({
                    "month": ym,
                    "label": label,
                    "video_count": r[1],
                    "analyst_count": r[2],
                    "total_views": r[3] or 0
                })
        return results

def get_monthly_analytics(target_month: str) -> Dict[str, Any]:
    """특정 월(YYYY-MM)에 대한 종합 분석 및 전월(MoM) 대비 트렌드 변화"""
    cache_key = f"monthly_analytics_{target_month}"
    cached = get_trend_cache(cache_key)
    if cached:
        return cached

    with get_connection() as conn:
        cursor = conn.cursor()
        
        # 1. 대상 월의 기본 통계
        cursor.execute("""
            SELECT COUNT(*), COUNT(DISTINCT analyst_name), SUM(view_count)
            FROM videos
            WHERE SUBSTR(published_at, 1, 7) = ?
        """, (target_month,))
        row = cursor.fetchone()
        v_count, a_count, total_views = row[0], row[1], row[2] or 0
        
        # 2. 대상 월의 스탠스 분포
        cursor.execute("""
            SELECT sentiment_label, COUNT(*)
            FROM videos
            WHERE SUBSTR(published_at, 1, 7) = ?
            GROUP BY sentiment_label
        """, (target_month,))
        s_counts = {r[0]: r[1] for r in cursor.fetchall()}
        
        # 3. 대상 월의 상위 키워드 Top 10
        cursor.execute("""
            SELECT k.keyword, SUM(k.count) as cnt
            FROM video_keywords k
            JOIN videos v ON k.video_id = v.video_id
            WHERE SUBSTR(v.published_at, 1, 7) = ?
            GROUP BY k.keyword
            ORDER BY cnt DESC
            LIMIT 10
        """, (target_month,))
        curr_keywords = {r[0]: r[1] for r in cursor.fetchall()}
        
        # 4. 직전 월(Previous Month) 계산
        y, m = int(target_month[:4]), int(target_month[5:7])
        prev_m = 12 if m == 1 else m - 1
        prev_y = y - 1 if m == 1 else y
        prev_month = f"{prev_y:04d}-{prev_m:02d}"
        
        # 5. 직전 월의 통계 및 키워드
        cursor.execute("""
            SELECT sentiment_label, COUNT(*)
            FROM videos
            WHERE SUBSTR(published_at, 1, 7) = ?
            GROUP BY sentiment_label
        """, (prev_month,))
        prev_s_counts = {r[0]: r[1] for r in cursor.fetchall()}
        
        cursor.execute("""
            SELECT k.keyword, SUM(k.count) as cnt
            FROM video_keywords k
            JOIN videos v ON k.video_id = v.video_id
            WHERE SUBSTR(v.published_at, 1, 7) = ?
            GROUP BY k.keyword
            ORDER BY cnt DESC
            LIMIT 10
        """, (prev_month,))
        prev_keywords = {r[0]: r[1] for r in cursor.fetchall()}
        
        # 6. 전월 대비 급증(MoM Surge) 키워드 산출
        mom_surging = []
        for kw, curr_cnt in curr_keywords.items():
            prev_cnt = prev_keywords.get(kw, 0)
            diff = curr_cnt - prev_cnt
            mom_surging.append({
                "keyword": kw,
                "curr_count": curr_cnt,
                "prev_count": prev_cnt,
                "growth": diff
            })
        mom_surging.sort(key=lambda x: x["growth"], reverse=True)
        
        # 7. 스탠스 비율 MoM 비교
        curr_total = sum(s_counts.values()) or 1
        prev_total = sum(prev_s_counts.values()) or 1
        curr_bullish_pct = round((s_counts.get("bullish", 0) / curr_total) * 100)
        prev_bullish_pct = round((prev_s_counts.get("bullish", 0) / prev_total) * 100)
        
        # 월간 요약 테마
        y_str, m_str = target_month.split("-")
        label = f"{y_str}년 {int(m_str)}월"
        
        result = {
            "month": target_month,
            "label": label,
            "video_count": v_count,
            "analyst_count": a_count,
            "total_views": total_views,
            "sentiment_distribution": s_counts,
            "bullish_percentage": curr_bullish_pct,
            "prev_month": prev_month,
            "prev_bullish_percentage": prev_bullish_pct,
            "mom_bullish_delta": curr_bullish_pct - prev_bullish_pct,
            "mom_surging_keywords": mom_surging[:6],
            "top_keywords": list(curr_keywords.keys())[:8]
        }
        
    set_trend_cache(cache_key, result)
    return result

def get_analyst_view_timeline(analyst_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """전문가별 시간에 따른 시각 변화 추적 (2024 -> 2026)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT o.analyst_name, o.topic, o.stance, o.core_argument, o.key_quote,
                   o.period_label, v.title, v.published_at, v.video_id, v.video_url
            FROM analyst_opinions o
            JOIN videos v ON o.video_id = v.video_id
            WHERE 1=1
        """
        params = []
        if analyst_name and analyst_name != "all":
            query += " AND o.analyst_name = ?"
            params.append(analyst_name)
            
        query += " ORDER BY o.analyst_name ASC, v.published_at ASC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # 분석가별 그룹핑
        analysts_map = defaultdict(lambda: {"analyst_name": "", "timeline": []})
        for r in rows:
            name = r[0]
            analysts_map[name]["analyst_name"] = name
            analysts_map[name]["timeline"].append({
                "topic": r[1],
                "stance": r[2],
                "core_argument": r[3],
                "key_quote": r[4],
                "period_label": r[5],
                "title": r[6],
                "published_at": r[7],
                "video_id": r[8],
                "video_url": r[9]
            })
            
        return list(analysts_map.values())


def get_analyst_matrix(
    topic: str = "all",
    period: str = "all",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    """분석가별 스탠스 및 최신 의견 매트릭스 테이블 (자유 기간 지원)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT o.analyst_name, o.topic, o.stance, o.core_argument, o.key_quote,
                   o.period_label, v.title, v.channel_title, v.published_at, v.video_url, v.video_id
            FROM analyst_opinions o
            JOIN videos v ON o.video_id = v.video_id
            WHERE 1=1
        """
        params = []
        if topic and topic != "all":
            query += " AND o.topic = ?"
            params.append(topic)
        if start_date:
            query += " AND v.published_at >= ?"
            params.append(start_date)
        if end_date:
            query += " AND v.published_at <= ?"
            params.append(end_date)
        if (not start_date and not end_date) and period and period not in ("all", "custom", "recent-3m"):
            if len(period) == 7 and period[4] == "-":
                query += " AND SUBSTR(v.published_at, 1, 7) = ?"
                params.append(period)
            else:
                query += " AND (o.period_label = ? OR SUBSTR(v.published_at, 1, 7) = ?)"
                params.extend([period, period])
            
        query += " ORDER BY v.published_at DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()

        
        return [
            {
                "analyst_name": r[0],
                "topic": r[1],
                "stance": r[2],
                "core_argument": r[3],
                "key_quote": r[4],
                "period_label": r[5],
                "title": r[6],
                "channel_title": r[7],
                "published_at": r[8],
                "video_url": r[9],
                "video_id": r[10]
            }
            for r in rows
        ]


def get_timeline_trends() -> Dict[str, Any]:
    """월별/시계열 주요 경제 테마별 언급 빈도 추이 (Chart.js 라인 차트용)"""
    themes = {
        "금리/통화정책": ["금리", "연준", "파월", "빅컷", "중립금리", "인플레이션", "물가"],
        "AI/반도체": ["AI", "엔비디아", "반도체", "HBM", "HBM4", "루빈", "로봇", "하이닉스", "전력", "SMR"],
        "국내주식/밸류업": ["코스피", "밸류업", "저PBR", "상법", "금투세", "주주환원"],
        "환율/원자재": ["환율", "달러", "금", "원달러"],
        "부동산/가계부채": ["부동산", "아파트", "DSR", "주담대", "전세"]
    }
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # 월별 라벨 목록 (YYYY-MM)
        cursor.execute("""
            SELECT DISTINCT SUBSTR(published_at, 1, 7) as ym
            FROM videos
            WHERE published_at IS NOT NULL
            ORDER BY ym ASC
        """)
        months = [r[0] for r in cursor.fetchall() if r[0]]
        
        datasets = []
        for theme_name, keywords in themes.items():
            kw_placeholders = ",".join(["?"] * len(keywords))
            counts_per_month = []
            
            for m in months:
                cursor.execute(f"""
                    SELECT COALESCE(SUM(k.count), 0)
                    FROM video_keywords k
                    JOIN videos v ON k.video_id = v.video_id
                    WHERE SUBSTR(v.published_at, 1, 7) = ?
                    AND k.keyword IN ({kw_placeholders})
                """, [m] + keywords)
                val = cursor.fetchone()[0]
                counts_per_month.append(val)
                
            datasets.append({
                "label": theme_name,
                "data": counts_per_month
            })
            
        return {
            "labels": months,
            "datasets": datasets
        }
