import os
import re
import json
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Any, Optional
import requests

from db.database import save_video, save_analyst_opinion, get_video_by_id
from crawler.transcript_extractor import extract_transcript
from crawler.seed_data import SEED_VIDEOS

# 유튜브 주요 경제 채널 매핑 (확장)
TARGET_CHANNELS = [
    {"name": "삼프로TV", "channel_id": "UChlv4GSd7OQl3js-jkLOnFA", "default_cat": "거시경제/금리"},
    {"name": "슈카월드", "channel_id": "UCsJ6RuBiTVWRX156FVbeaGg", "default_cat": "미국주식/글로벌"},
    {"name": "815머니톡", "channel_id": "UC6x7_2W3S21F5n8-W7z255w", "default_cat": "국내주식"},
    {"name": "매부리TV", "channel_id": "UCCt6iN6nJemSe_OHRihYBAQ", "default_cat": "부동산"},
    {"name": "한국경제TV", "channel_id": "UC-hjg339zutA8pZ3pZ7t1CA", "default_cat": "국내주식"},
    {"name": "전인구경제연구소", "channel_id": "UC_jeoningu_dummy", "default_cat": "거시경제/금리"},
    {"name": "월급쟁이부자들", "channel_id": "UC_weolbu_dummy", "default_cat": "부동산"},
    {"name": "신사임당", "channel_id": "UC_sinsaimdang_dummy", "default_cat": "거시경제/금리"},
    {"name": "이효석아카데미", "channel_id": "UC_leehyoseok_dummy", "default_cat": "국내주식"}
]

# 제목 및 설명에서 주요 분석가 탐지 정규식 (대폭 확장)
ANALYST_PATTERNS = {
    "오건영": [r"오건영", r"신한.*오건영"],
    "염승환": [r"염승환", r"염블리", r"이베스트.*염승환", r"LS.*염승환"],
    "김일구": [r"김일구", r"한화.*김일구"],
    "이선엽": [r"이선엽", r"신한.*이선엽"],
    "박석중": [r"박석중", r"신한.*박석중"],
    "홍춘욱": [r"홍춘욱", r"프리즘.*홍춘욱"],
    "슈카": [r"슈카", r"슈카월드", r"전석재"],
    "전인구": [r"전인구", r"전인구경제연구소"],
    "이효석": [r"이효석", r"업사이드", r"이효석아카데미"],
    "강환국": [r"강환국", r"알고투자", r"퀀트.*강환국"],
    "채상욱": [r"채상욱", r"커넥티드.*채상욱"],
    "곽상준": [r"곽상준", r"신한.*곽상준", r"증시각도기"],
    "최준철": [r"최준철", r"VIP.*최준철"],
    "안유화": [r"안유화", r"성균관대.*안유화"],
    "강영현": [r"강영현", r"유진.*강영현"],
    "김동환": [r"김동환", r"김프로"]
}

CATEGORY_KEYWORDS = {
    "거시경제/금리": ["금리", "연준", "파월", "인플레이션", "cpi", "물가", "경기침체", "fomc", "통화정책", "채권", "양적완화", "기준금리", "피벗"],
    "국내주식": ["코스피", "코스닥", "삼성전자", "sk하이닉스", "밸류업", "저pbr", "상법", "금투세", "국장", "배당", "주주환원", "2차전지", "현대차"],
    "미국주식/글로벌": ["나스닥", "엔비디아", "빅테크", "s&p500", "m7", "애플", "마이크로소프트", "미 대선", "트럼프", "ai 랠리", "빅쇼트", "월가"],
    "부동산": ["부동산", "아파트", "전세", "청약", "재건축", "분양", "스트레스 dsr", "주담대", "집값", "공급부족", "신생아특례"],
    "환율/원자재": ["환율", "달러", "원달러", "금", "gold", "원유", "유가", "은", "구리", "엔화", "엔캐리", "엔저"]
}

def detect_analyst(text: str, channel_title: str = "") -> str:
    """텍스트에서 분석가 이름 탐지 (채널/키워드 연동)"""
    for name, patterns in ANALYST_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, text, re.IGNORECASE):
                return name
    if channel_title:
        for name, patterns in ANALYST_PATTERNS.items():
            for pat in patterns:
                if re.search(pat, channel_title, re.IGNORECASE):
                    return name
        return f"{channel_title} 분석팀"
    return "거시경제 분석팀"

def detect_category(text: str, default_cat: str = "거시경제/금리") -> str:
    """텍스트 키워드 기반 카테고리 자동 분류"""
    text_lower = text.lower()
    score_map = {}
    for cat, kws in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in kws if kw in text_lower)
        if score > 0:
            score_map[cat] = score
    if score_map:
        return max(score_map.items(), key=lambda x: x[1])[0]
    return default_cat

def initialize_seed_database() -> int:
    """초기 시드 데이터베이스 적재"""
    saved = 0
    for item in SEED_VIDEOS:
        existing = get_video_by_id(item["video_id"])
        if not existing:
            success = save_video({
                "video_id": item["video_id"],
                "title": item["title"],
                "channel_title": item["channel_title"],
                "channel_id": item.get("channel_id", ""),
                "analyst_name": item.get("analyst_name", "경제전문가"),
                "category": item.get("category", "거시경제/금리"),
                "published_at": item.get("published_at"),
                "video_url": item.get("video_url"),
                "thumbnail_url": item.get("thumbnail_url", ""),
                "view_count": item.get("view_count", 0),
                "duration_sec": item.get("duration_sec", 0),
                "summary_text": item.get("summary_text", ""),
                "transcript_text": item.get("transcript_text", ""),
                "sentiment_label": item.get("sentiment_label", "neutral"),
                "sentiment_score": item.get("sentiment_score", 0.0),
                "processed": 1
            })
            if success:
                saved += 1
                op = item.get("opinion")
                if op:
                    save_analyst_opinion(
                        video_id=item["video_id"],
                        analyst_name=item["analyst_name"],
                        topic=op.get("topic", "거시경제"),
                        stance=op.get("stance", "Neutral"),
                        core_argument=op.get("core_argument", ""),
                        key_quote=op.get("key_quote", ""),
                        period_label=item.get("period_label", "2024-H2")
                    )
    print(f"[Collector] Loaded {saved} seed videos into database.")
    return saved

def fetch_channel_rss(channel_id: str, channel_name: str = "", default_cat: str = "거시경제/금리") -> List[Dict[str, Any]]:
    """유튜브 채널 공개 RSS 피드에서 최신 영상 메타데이터 수집 (브라우저 User-Agent 적용)"""
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    videos = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(rss_url, headers=headers, timeout=10)
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'yt': 'http://www.youtube.com/xml/schemas/2015',
                'media': 'http://search.yahoo.com/mrss/'
            }
            
            for entry in root.findall('atom:entry', ns):
                video_id_elem = entry.find('yt:videoId', ns)
                title_elem = entry.find('atom:title', ns)
                pub_elem = entry.find('atom:published', ns)
                author_elem = entry.find('atom:author/atom:name', ns)
                
                if video_id_elem is not None and title_elem is not None:
                    vid = video_id_elem.text
                    title = title_elem.text
                    pub_date = pub_elem.text[:10] if pub_elem is not None else datetime.now().strftime("%Y-%m-%d")
                    ch_title = author_elem.text if author_elem is not None else channel_name
                    
                    media_group = entry.find('media:group', ns)
                    thumb_url = f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
                    if media_group is not None:
                        thumb_elem = media_group.find('media:thumbnail', ns)
                        if thumb_elem is not None:
                            thumb_url = thumb_elem.attrib.get('url', thumb_url)
                            
                    analyst = detect_analyst(title, ch_title)
                    category = detect_category(title, default_cat=default_cat)
                    
                    videos.append({
                        "video_id": vid,
                        "title": title,
                        "channel_title": ch_title,
                        "channel_id": channel_id,
                        "analyst_name": analyst,
                        "category": category,
                        "published_at": pub_date,
                        "video_url": f"https://www.youtube.com/watch?v={vid}",
                        "thumbnail_url": thumb_url,
                        "view_count": 0,
                        "duration_sec": 0,
                        "summary_text": "",
                        "transcript_text": "",
                        "processed": 0
                    })
    except Exception as e:
        print(f"[Collector] RSS fetch error for {channel_id}: {e}")
    return videos

def search_youtube_videos(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """유튜브 검색(Search) 결과를 스크래핑하여 실제 영상 메타데이터 대량 수집 (RSS 15개 한계 돌파)"""
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    videos = []
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            html = resp.text
            m = re.search(r'var ytInitialData = ({.*?});</script>', html) or re.search(r'ytInitialData = ({.*?});', html)
            if m:
                data = json.loads(m.group(1))
                contents = data.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [])
                for section in contents:
                    item_section = section.get('itemSectionRenderer', {}).get('contents', [])
                    for item in item_section:
                        vr = item.get('videoRenderer')
                        if vr:
                            vid = vr.get('videoId')
                            title = vr.get('title', {}).get('runs', [{}])[0].get('text', '')
                            channel = vr.get('ownerText', {}).get('runs', [{}])[0].get('text', '경제채널')
                            
                            if vid and title and len(vid) == 11:
                                analyst = detect_analyst(title, channel)
                                category = detect_category(title)
                                videos.append({
                                    "video_id": vid,
                                    "title": title,
                                    "channel_title": channel,
                                    "channel_id": "",
                                    "analyst_name": analyst,
                                    "category": category,
                                    "published_at": datetime.now().strftime("%Y-%m-%d"),
                                    "video_url": f"https://www.youtube.com/watch?v={vid}",
                                    "thumbnail_url": f"https://img.youtube.com/vi/{vid}/hqdefault.jpg",
                                    "view_count": 0,
                                    "duration_sec": 0,
                                    "summary_text": "",
                                    "transcript_text": "",
                                    "processed": 0
                                })
                                if len(videos) >= max_results:
                                    return videos
    except Exception as e:
        print(f"[Collector] Search error for query '{query}': {e}")
    return videos

def collect_latest_youtube_videos(limit_per_channel: int = 5) -> int:
    """주요 경제 채널들의 최신 영상을 RSS 및 유튜브 검색을 통해 대량 수집"""
    total_added = 0
    # 1. RSS 기반 수집
    for ch in TARGET_CHANNELS:
        ch_videos = fetch_channel_rss(ch["channel_id"], ch["name"], ch["default_cat"])
        for v in ch_videos[:limit_per_channel]:
            if not get_video_by_id(v["video_id"]):
                transcript = extract_transcript(v["video_id"])
                if transcript:
                    v["transcript_text"] = transcript
                if save_video(v):
                    total_added += 1
                    
    # 2. 거시경제 주요 쿼리 검색 기반 보충 수집
    search_queries = [
        "2026 경제 전망", "금리 인하 연준 피벗", "반도체 HBM 코스피", "부동산 DSR 대출", "환율 달러 전망"
    ]
    for q in search_queries:
        s_videos = search_youtube_videos(q, max_results=5)
        for v in s_videos:
            if not get_video_by_id(v["video_id"]):
                transcript = extract_transcript(v["video_id"])
                if transcript:
                    v["transcript_text"] = transcript
                if save_video(v):
                    total_added += 1
                    
    print(f"[Collector] Collected total {total_added} new videos from YouTube RSS & Search.")
    return total_added

def collect_by_month(target_month: str, limit_per_channel: int = 5) -> int:
    """특정 연-월(YYYY-MM)에 해당하는 영상을 채널 RSS 및 검색을 통해 대량 수집"""
    print(f"[Collector] '{target_month}' 월간 경제 영상 대량 수집 시작...")
    total_added = 0
    
    # 1. RSS 피드 검색
    for ch in TARGET_CHANNELS:
        ch_videos = fetch_channel_rss(ch["channel_id"], ch["name"], ch["default_cat"])
        for v in ch_videos:
            pub_date = v.get("published_at", "")
            if pub_date.startswith(target_month):
                if not get_video_by_id(v["video_id"]):
                    transcript = extract_transcript(v["video_id"])
                    if transcript:
                        v["transcript_text"] = transcript
                    v["period_label"] = target_month
                    if save_video(v):
                        total_added += 1
                        
    # 2. RSS에 부족할 경우 유튜브 검색 엔진으로 타겟 월 관련 경제 영상 보충
    if total_added < 15:
        search_queries = [
            f"{target_month} 경제 전망",
            f"{target_month} 금리 주식",
            f"오건영 {target_month}",
            f"염승환 {target_month}",
            f"슈카 {target_month}"
        ]
        for q in search_queries:
            s_videos = search_youtube_videos(q, max_results=6)
            for v in s_videos:
                if not get_video_by_id(v["video_id"]):
                    v["published_at"] = f"{target_month}-15"
                    v["period_label"] = target_month
                    transcript = extract_transcript(v["video_id"])
                    if transcript:
                        v["transcript_text"] = transcript
                    if save_video(v):
                        total_added += 1
                        if total_added >= 30:
                            break
                            
    print(f"[Collector] '{target_month}' 월간 {total_added}건 신규 수집 완료.")
    return total_added
