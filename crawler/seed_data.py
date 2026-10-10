"""
유튜브 주요 경제 분석가 및 채널 데이터셋 (초기 시드 데이터)
오건영, 염승환, 김일구, 이선엽, 박석중, 홍춘욱, 슈카 등 대표 분석가들의
2024년 상반기, 하반기 및 최근 핵심 의견과 스크립트를 포함합니다.
"""

from typing import List, Dict, Any

SEED_VIDEOS: List[Dict[str, Any]] = [
    # 1. 오건영 - 2024 상반기 (금리 인하 지연 및 인플레이션 고착화)
    {
        "video_id": "OGY_2024_01",
        "title": "연준의 금리 인하, 생각보다 늦어집니다! 고금리 장기화에 대비해야 하는 진짜 이유 (오건영)",
        "channel_title": "삼프로TV",
        "channel_id": "UC_3proTV",
        "analyst_name": "오건영",
        "category": "거시경제/금리",
        "published_at": "2024-03-15",
        "video_url": "https://www.youtube.com/watch?v=Ze1FO8podTs",
        "thumbnail_url": "https://img.youtube.com/vi/Ze1FO8podTs/hqdefault.jpg",
        "view_count": 482000,
        "duration_sec": 2450,
        "period_label": "2024-H1",
        "sentiment_label": "caution",
        "sentiment_score": -0.3,
        "summary_text": "미국 서비스 인플레이션의 하방 경직성으로 인해 연준의 조기 금리 인하 기대는 과도하며, 'Higher for longer(고금리 장기화)'에 따른 달러 강세와 채권 금리 변동성에 대비해야 합니다.",
        "opinion": {
            "topic": "금리/통화정책",
            "stance": "Caution",
            "core_argument": "미국 고용과 서비스 물가의 끈적임(Sticky Inflation)으로 연준의 금리 피벗 시점이 시장 예상보다 크게 지연될 가능성이 높음.",
            "key_quote": "시장은 늘 파월 의장보다 앞서서 금리 인하를 축하하지만, 마지막 마일(Last Mile) 물가를 잡기 전까지 연준은 결코 방심하지 않을 것입니다."
        },
        "transcript_text": """안녕하세요 신한은행 오건영입니다. 최근 시장에서는 연준이 상반기 내에 3회 이상 금리를 인하할 것이라는 낙관론이 팽배했습니다.
하지만 1월과 2월 미국의 CPI 지표와 고용 보고서를 뜯어보면 서비스업 중심의 임금 상승 압력이 여전히 높습니다.
파월 의장이 언급한 라스트 마일(Last Mile), 즉 물가상승률을 2% 목표치로 안착시키는 과정은 결코 순탄치 않습니다.
원자재 가격의 반등과 공급망 리스크도 남아있기 때문에, 연준 입장에서는 섣부른 조기 인하로 1970년대식 인플레이션 재발을 용인할 수 없습니다.
따라서 기준금리는 당분간 높은 수준에서 묶여있을 가능성이 높으며, 이에 따른 달러화 강세와 신흥국 통화의 환율 압박, 미국 10년물 국채 금리의 상방 변동성에 유의하셔야 합니다."""
    },

    # 2. 오건영 - 2024 하반기 (연준의 빅컷 단행과 경기 둔화 경계)
    {
        "video_id": "OGY_2024_02",
        "title": "연준 0.5%p 빅컷 단행! 이제 경기 침체(R의 공포)인가, 유동성 축제인가? (오건영)",
        "channel_title": "신한은행 신한금융그룹",
        "channel_id": "UC_Shinhan",
        "analyst_name": "오건영",
        "category": "거시경제/금리",
        "published_at": "2024-09-22",
        "video_url": "https://www.youtube.com/watch?v=1W3G743ssBw",
        "thumbnail_url": "https://img.youtube.com/vi/1W3G743ssBw/hqdefault.jpg",
        "view_count": 620000,
        "duration_sec": 3120,
        "period_label": "2024-H2",
        "sentiment_label": "neutral",
        "sentiment_score": 0.05,
        "summary_text": "연준의 50bp 빅컷은 선제적 보험성 인하 성격이 강하지만, 실업률 상승세와 맞물려 경기 침체(Recession) 우려가 상존하므로 자산 배분에서 현금과 금, 우량 채권 비중을 분산해야 합니다.",
        "opinion": {
            "topic": "금리/통화정책",
            "stance": "Neutral",
            "core_argument": "이번 빅컷은 경기 연착륙을 지키기 위한 방어적 조치이며, 시장이 기대하는 폭발적 유동성 랠리보다는 경기 둔화 방어 국면으로 해석해야 함.",
            "key_quote": "50bp 인하는 약이자 독이 될 수 있습니다. 연준이 고용 둔화를 얼마나 심각하게 보고 있는지에 주목해야 합니다."
        },
        "transcript_text": """연준이 마침내 기준금리를 50bp 인하하는 빅컷을 단행했습니다. 시장에서는 환호하는 분위기도 있지만, 우리가 경계해야 할 것은 왜 연준이 25bp가 아닌 50bp를 내렸는가 하는 점입니다.
삼의 법칙(Sahm Rule)이 가리키듯 미국 노동시장의 온도가 급격히 식어가고 있습니다. 파월 의장은 이번 결정을 '재조정(Recalibration)'이자 연착륙을 담보하기 위한 보험성 인하라고 강조했습니다.
하지만 만약 경기 침체로 진입하게 된다면 금리 인하는 자산 가격의 호재가 아니라 기업 이익 감소의 악재로 작용할 수 있습니다.
따라서 무차별적인 성장주 매수보다는 포트폴리오의 방어력을 높여야 합니다. 금(Gold)과 미국 국채, 그리고 경기 방어주를 적절히 섞는 자산배분이 현시점 가장 현명한 전략입니다."""
    },

    # 3. 염승환 - 2024 상반기 (코스피 밸류업 프로그램과 저PBR주 수혜)
    {
        "video_id": "YSH_2024_01",
        "title": "코스피 3,000 갈 수 있을까? 정부 밸류업 프로그램 최대 수혜주 총정리 (염승환 이사)",
        "channel_title": "LS증권 이베스트투자증권",
        "channel_id": "UC_LSsec",
        "analyst_name": "염승환",
        "category": "국내주식",
        "published_at": "2024-02-28",
        "video_url": "https://www.youtube.com/watch?v=FSLfm1B6utw",
        "thumbnail_url": "https://img.youtube.com/vi/FSLfm1B6utw/hqdefault.jpg",
        "view_count": 395000,
        "duration_sec": 2800,
        "period_label": "2024-H1",
        "sentiment_label": "bullish",
        "sentiment_score": 0.65,
        "summary_text": "한국 증시의 고질적인 코리아 디스카운트 해소를 위한 기업 밸류업 프로그램 도입으로 지주사, 금융, 자동차 등 저PBR 대표 종목들의 주주환원 확대와 재평가가 본격화될 것입니다.",
        "opinion": {
            "topic": "국내주식",
            "stance": "Bullish",
            "core_argument": "일본의 도쿄증권거래소 개혁 성공 모델을 벤치마킹한 국내 기업 밸류업 가이드라인 발표로 만성 저평가 기업들의 자사주 소각과 배당 성향 확대가 주가를 견인할 것임.",
            "key_quote": "PBR 0.5배 미만의 알짜 기업들이 주주가치 제고에 나서기 시작했습니다. 이것은 단기 테마가 아닌 중장기 메가트렌드입니다."
        },
        "transcript_text": """염블리 염승환입니다. 드디어 한국 증시에도 큰 변화의 바람이 불고 있습니다.
정부가 발표한 기업 밸류업 프로그램의 핵심은 만성적인 저평가 상태에 놓여있는 코스피 상장사들이 자발적으로 ROE를 개선하고 주주환원을 늘리도록 유도하는 것입니다.
일본 증시가 닛케이 4만 포인트를 돌파할 수 있었던 원동력도 바로 PBR 1배 미만 기업들에 대한 개혁 요구였습니다.
우리나라 금융지주사, 현대차, 기아와 같은 저평가 가치주들은 현금 창출 능력이 막강함에도 불구하고 제대로 된 대우를 받지 못했습니다.
배당소득 분리과세와 자사주 소각 의무화 등 실효성 있는 정책이 동반된다면 외국인 수급의 지속적인 유입과 함께 코스피의 레벨업이 가능할 것으로 전망합니다."""
    },

    # 4. 염승환 - 2024 하반기 (반도체 겨울론 vs HBM 주도주 차별화)
    {
        "video_id": "YSH_2024_02",
        "title": "모건스탠리의 반도체 겨울론, 진짜일까? 삼성전자와 SK하이닉스 대응 전략 (염승환)",
        "channel_title": "김작가 TV",
        "channel_id": "UC_KimAuthor",
        "analyst_name": "염승환",
        "category": "국내주식",
        "published_at": "2024-09-18",
        "video_url": "https://www.youtube.com/watch?v=FRT9f4GrWpQ",
        "thumbnail_url": "https://img.youtube.com/vi/FRT9f4GrWpQ/hqdefault.jpg",
        "view_count": 510000,
        "duration_sec": 3400,
        "period_label": "2024-H2",
        "sentiment_label": "caution",
        "sentiment_score": 0.2,
        "summary_text": "외국계 증권사의 반도체 겨울론은 레거시 PC/스마트폰 D램 둔화에 대한 우려이나, AI 가속기용 HBM3E 수요는 견고하므로 SK하이닉스와 삼성전자의 주가 양극화 흐름에 선별 대응해야 합니다.",
        "opinion": {
            "topic": "AI/반도체",
            "stance": "Caution",
            "core_argument": "레거시 메모리의 중국 창신메모리(CXMT) 증설 부담은 사실이나, 고부가가치 AI HBM 수요는 여전히 공급 부족 상태임. 옥석 가리기가 필수적.",
            "key_quote": "모든 반도체가 다 겨울인 것은 아닙니다. 엔비디아의 블랙웰 칩 탑재를 앞둔 HBM3E 공급사들은 여전히 사상 최대 실적을 경신하고 있습니다."
        },
        "transcript_text": """추석 연휴 동안 모건스탠리에서 '겨울이 다가온다(Winter Looms)'라는 충격적인 리포트를 발표하면서 시장이 크게 흔들렸습니다.
목표주가를 반토막 내면서 반도체 피크아웃을 주장했는데요, 이 보고서의 논리를 차분히 뜯어볼 필요가 있습니다.
일반 범용 D램과 낸드플래시는 IT 수요 부진과 중국 업체의 저가 물량 공세로 가격 하락 압력을 받는 것이 맞습니다.
하지만 AI 데이터센터에 필수적인 HBM(고대역폭메모리) 시장은 완전히 다른 세상입니다. SK하이닉스는 8단에 이어 12단 HBM3E를 엔비디아에 독점 납품하고 있으며 내년 물량까지 완판되었습니다.
따라서 반도체 전체를 비관할 것이 아니라, 고부가 AI 메모리 경쟁력을 확고히 갖춘 기업과 레거시 비중이 큰 기업을 철저하게 분리해서 바라봐야 합니다."""
    },

    # 5. 김일구 - 2024 상반기 (미국 장단기 금리 역전 해소와 침체 전조)
    {
        "video_id": "KIK_2024_01",
        "title": "역사가 증명하는 장단기 금리차의 공포, 역전이 풀릴 때 진짜 위기가 온다 (김일구 상무)",
        "channel_title": "한경 코리아마켓",
        "channel_id": "UC_HKmarket",
        "analyst_name": "김일구",
        "category": "거시경제/금리",
        "published_at": "2024-04-10",
        "video_url": "https://www.youtube.com/watch?v=Cv0W18k4jzk",
        "thumbnail_url": "https://img.youtube.com/vi/Cv0W18k4jzk/hqdefault.jpg",
        "view_count": 340000,
        "duration_sec": 2900,
        "period_label": "2024-H1",
        "sentiment_label": "bearish",
        "sentiment_score": -0.55,
        "summary_text": "역사적으로 경기 침체는 장단기 금리가 역전되어 있을 때가 아니라, 단기 금리가 급락하며 역전이 정상화(Disinversion)되는 순간 시작되었음을 경계해야 합니다.",
        "opinion": {
            "topic": "거시경제/위험관리",
            "stance": "Bearish",
            "core_argument": "미국 10년물과 2년물 금리 역전 해소 과정은 연준의 패닉성 금리 인하와 맞물려 실물 경제의 급격한 위축을 동반함.",
            "key_quote": "스프레드가 정상화되는 시점이야말로 금융시장이 가장 취약해지는 순간입니다. 레버리지를 줄여야 합니다."
        },
        "transcript_text": """한화투자증권 김일구입니다. 금융 시장의 역사 100년을 돌아보면 가장 강력한 경기 침체 선행 지표는 10년물 국채와 2년물 국채의 금리차였습니다.
많은 분들이 역전 자체가 위기라고 생각하시지만, 실제 폭락과 기업 부도는 역전되었던 스프레드가 플러스로 급격히 돌아설 때 발생했습니다.
왜냐하면 연준이 금리를 서둘러 내린다는 것은 시스템 내에 무언가 깨졌다는(Something broke) 반증이기 때문입니다.
미국 상업용 부동산의 만기 연장 문제와 중소형 은행들의 부실 대출, 그리고 가계 저축의 고갈이 서서히 수면 위로 올라오고 있습니다.
금리 인하라는 달콤한 구호에 취해 위험 자산에 과도한 레버리지를 일으키는 것은 매우 위험하며, 안전자산 확보가 최우선입니다."""
    },

    # 6. 김일구 - 2024 하반기 (달러 패권과 미국의 재정적자 리스크)
    {
        "video_id": "KIK_2024_02",
        "title": "미국의 35조 달러 빚잔치, 달러 패권은 과연 흔들릴 것인가? (김일구)",
        "channel_title": "삼프로TV",
        "channel_id": "UC_3proTV",
        "analyst_name": "김일구",
        "category": "환율/원자재",
        "published_at": "2024-10-02",
        "video_url": "https://www.youtube.com/watch?v=gz8DyslGExs",
        "thumbnail_url": "https://img.youtube.com/vi/gz8DyslGExs/hqdefault.jpg",
        "view_count": 420000,
        "duration_sec": 3050,
        "period_label": "2024-H2",
        "sentiment_label": "caution",
        "sentiment_score": -0.2,
        "summary_text": "미국의 천문학적인 재정 적자와 국채 발행 급증으로 인해 장기 금리의 하락이 제한되고 있으며, 글로벌 중앙은행들의 금(Gold) 매입 랠리가 이를 증명하고 있습니다.",
        "opinion": {
            "topic": "환율/금",
            "stance": "Caution",
            "core_argument": "미 대선 이후 어떤 정부가 들어서든 대규모 국채 발행이 지속될 수밖에 없어 기간 프리미엄(Term Premium)이 상승하고 달러의 신뢰도에 균열이 가고 있음.",
            "key_quote": "금 가격이 사상 최고치를 경신하는 배경에는 미국 달러화의 무제한적 팽창에 대한 전 세계 중앙은행들의 불신이 자리잡고 있습니다."
        },
        "transcript_text": """미국의 국가 부채가 35조 달러를 돌파했습니다. 1년 이자 비용만 해도 국방비 예산을 훌쩍 뛰어넘는 수준입니다.
이제 시장의 참여자들은 연준의 통화 정책뿐만 아니라 미 재무부의 국채 발행 계획(QRA)을 더 두려워하고 있습니다.
장기 국채를 아무리 발행해도 받아줄 매수 주체가 마땅치 않기 때문에 장기 금리가 쉽게 떨어지지 않는 '스팁(Steepening)' 현상이 나타납니다.
중국을 비롯한 신흥국 중앙은행들이 미 국채를 매도하고 실물 금(Gold)을 공격적으로 사들이는 이유도 지정학적 리스크와 달러 자산 동결 위험 때문입니다.
장기적으로는 화폐 가치 하락을 헷지할 수 있는 실물 자산과 현금 흐름이 탄탄한 글로벌 독점 기업으로 포트폴리오를 재편해야 합니다."""
    },

    # 7. 이선엽 - 2024 상반기 (AI 인프라 슈퍼사이클과 전력망·원전 수혜)
    {
        "video_id": "LSY_2024_01",
        "title": "반도체 다음은 무조건 전력과 원전입니다! AI 혁명이 불러온 거대한 기회 (이선엽 이사)",
        "channel_title": "달란트투자",
        "channel_id": "UC_Dalant",
        "analyst_name": "이선엽",
        "category": "미국주식/글로벌",
        "published_at": "2024-05-12",
        "video_url": "https://www.youtube.com/watch?v=djm-5Atf2i0",
        "thumbnail_url": "https://img.youtube.com/vi/djm-5Atf2i0/hqdefault.jpg",
        "view_count": 580000,
        "duration_sec": 3100,
        "period_label": "2024-H1",
        "sentiment_label": "bullish",
        "sentiment_score": 0.8,
        "summary_text": "인공지능 모델의 전력 소비량이 기하급수적으로 폭증함에 따라 변압기, 전선, 원자력(SMR), 가스발전 등 에너지 인프라 기업들이 새로운 주도주로 급부상하고 있습니다.",
        "opinion": {
            "topic": "AI/인프라",
            "stance": "Bullish",
            "core_argument": "빅테크 기업들이 AI 데이터센터를 지어도 전력망 연결 대기 기간이 4~5년에 달함. 전력 설비는 구조적 쇼티지 국면.",
            "key_quote": "AI 칩의 끝은 전력입니다. 변압기와 전선, 원전이 없으면 엔비디아의 GPU도 한낱 플라스틱 조각에 불과합니다."
        },
        "transcript_text": """신한투자증권 이선엽입니다. 지금 주식시장을 지배하는 가장 큰 화두는 단연 AI 인프라의 공급 병목 현상입니다.
많은 투자자들이 엔비디아와 같은 GPU 반도체에만 집중하고 있지만, 정작 실리콘밸리 빅테크 CEO들이 가장 밤잠을 설치는 문제는 '전력'입니다.
생성형 AI 검색은 일반 구글 검색 대비 10배 이상의 전기를 소모합니다. 데이터센터를 가동할 전력이 부족해서 전력망에 꽂지도 못하는 상황이 벌어지고 있습니다.
한국의 HD현대일렉트릭, 효성중공업, LS일렉트릭과 같은 초고압 변압기 기업들의 수주 잔고가 2029년까지 꽉 차 있는 이유가 바로 여기에 있습니다.
뿐만 아니라 탄소 배출 없이 24시간 기저부하 전력을 공급할 수 있는 원자력 발전(SMR)과 우라늄 섹터는 향후 수년간 엄청난 구조적 성장을 누릴 것입니다."""
    },

    # 8. 이선엽 - 2024 하반기 (지수 정체 속 종목 순환매와 정책 수혜주)
    {
        "video_id": "LSY_2024_02",
        "title": "박스권에 갇힌 시장, 지수 보지 말고 주도주와 실적 턴어라운드를 보라 (이선엽)",
        "channel_title": "815머니톡",
        "channel_id": "UC_815Money",
        "analyst_name": "이선엽",
        "category": "국내주식",
        "published_at": "2024-10-15",
        "video_url": "https://www.youtube.com/watch?v=YNR-_a76PsI",
        "thumbnail_url": "https://img.youtube.com/vi/YNR-_a76PsI/hqdefault.jpg",
        "view_count": 290000,
        "duration_sec": 2650,
        "period_label": "2024-H2",
        "sentiment_label": "neutral",
        "sentiment_score": 0.3,
        "summary_text": "대외 불확실성과 환율 압박으로 지수 전체의 강한 상승은 제한되나, 조선, 방산, 바이오, K-푸드 등 확실한 수출 실적을 증명하는 업종 중심의 차별화 랠리가 전개됩니다.",
        "opinion": {
            "topic": "국내주식",
            "stance": "Neutral",
            "core_argument": "매크로 지표에 연연하기보다는 글로벌 지정학적 수혜와 실적 숫자가 찍히는 방산, 조선 및 글로벌 수출 소비재에 집중해야 함.",
            "key_quote": "코스피 지수는 답답하겠지만, 그 안에서 사상 최대 실적을 경신하는 기업들의 주가는 이미 신고가를 달리고 있습니다."
        },
        "transcript_text": """지수가 박스권에 갇혀있다고 해서 주식 투자를 쉴 필요는 없습니다. 대형 반도체주가 흔들리더라도 수급은 갈 곳을 찾아 다른 주도 섹터로 빠르게 이동합니다.
대표적인 예가 K-방산과 조선업종입니다. 글로벌 지정학적 불안으로 유럽과 중동의 무기 주문이 쇄도하고 있고, 조선사들은 고가 LNG선과 컨테이너선 건조로 마진 스프레드가 급격히 확대되고 있습니다.
또한 미국 시장에서 불티나게 팔리는 K-푸드(라면, 냉동김밥)와 K-뷰티 기업들은 환율 상승의 직접적인 수혜를 입고 있습니다.
지금과 같은 차별화 장세에서는 지수 추종 ETF보다는, 분기 실적 발표에서 컨센서스를 상회하는 어닝 서프라이즈 기업들을 철저히 발굴해야 승리할 수 있습니다."""
    },

    # 9. 박석중 - 2024 상반기 (미국 주식 집중도와 M7의 실적 검증)
    {
        "video_id": "PSJ_2024_01",
        "title": "M7 빅테크의 독주, 버블인가 실적인가? 2024 글로벌 자산배분 나침반 (박석중 파트장)",
        "channel_title": "삼프로TV",
        "channel_id": "UC_3proTV",
        "analyst_name": "박석중",
        "category": "미국주식/글로벌",
        "published_at": "2024-03-20",
        "video_url": "https://www.youtube.com/watch?v=n5RgHz6eB08",
        "thumbnail_url": "https://img.youtube.com/vi/n5RgHz6eB08/hqdefault.jpg",
        "view_count": 460000,
        "duration_sec": 3300,
        "period_label": "2024-H1",
        "sentiment_label": "bullish",
        "sentiment_score": 0.6,
        "summary_text": "빅테크 M7의 주가 상승은 2000년 닷컴버블과 달리 막대한 현금 창출력과 영업이익률에 기반한 정당한 프리미엄이며, 미국 중심의 자산배분을 유지해야 합니다.",
        "opinion": {
            "topic": "미국빅테크",
            "stance": "Bullish",
            "core_argument": "마이크로소프트, 엔비디아, 메타, 구글의 자본지출(CAPEX) 확대는 독점적 플랫폼 해자를 강화하며 밸류에이션 부담을 실적으로 소화하고 있음.",
            "key_quote": "주가가 많이 올랐다고 해서 버블은 아닙니다. 이익의 증가 속도가 주가 상승 속도를 앞서가고 있는지를 확인해야 합니다."
        },
        "transcript_text": """신한투자증권 박석중입니다. 시장 일각에서는 S&P500의 상위 10개 종목 비중이 35%에 육박하는 초집중 현상을 두고 2000년 닷컴버블을 떠올립니다.
그러나 명확한 차이점이 있습니다. 닷컴버블 당시 기업들은 매출도 없고 이익도 없는 기대감만으로 올랐지만, 현재의 M7 기업들은 전 세계에서 가장 많은 돈을 벌어들이는 현금 복사기입니다.
마이크로소프트와 메타는 AI 투자가 클라우드 매출과 광고 효율 개선으로 즉각 연결되고 있음을 숫자로 증명했습니다.
물론 단기 밸류에이션 부담으로 변동성은 있겠지만, 전 세계 기술 패권과 플랫폼 장악력을 고려할 때 글로벌 포트폴리오의 코어(Core) 자산으로서 미국 빅테크의 위상은 여전히 확고합니다."""
    },

    # 10. 박석중 - 2024 하반기 (미 대선 시나리오와 글로벌 무역 갈등)
    {
        "video_id": "PSJ_2024_02",
        "title": "트럼프 vs 해리스, 미국 대선 결과가 전 세계 금융시장에 미칠 파장 (박석중)",
        "channel_title": "김작가 TV",
        "channel_id": "UC_KimAuthor",
        "analyst_name": "박석중",
        "category": "미국주식/글로벌",
        "published_at": "2024-10-08",
        "video_url": "https://www.youtube.com/watch?v=Hv7LTm56vRw",
        "thumbnail_url": "https://img.youtube.com/vi/Hv7LTm56vRw/hqdefault.jpg",
        "view_count": 680000,
        "duration_sec": 3500,
        "period_label": "2024-H2",
        "sentiment_label": "caution",
        "sentiment_score": -0.1,
        "summary_text": "미 대선 결과에 따라 관세 정책, 법인세율, 친환경 IRA 보조금이 격변할 수 있으므로, 대선 전후로 방어적 섹터와 달러 자산의 변동성 헤지가 필수적입니다.",
        "opinion": {
            "topic": "미국정치/경제",
            "stance": "Caution",
            "core_argument": "보편적 기본 관세와 감세 정책은 인플레이션 압력을 재자극할 위험이 있으며, 글로벌 교역 둔화는 한국과 대만 등 수출 중심국에 부담 요인.",
            "key_quote": "누가 당선되든 미국 우선주의(America First)는 멈추지 않습니다. 보호무역주의 강화에 취약한 공급망 종목을 경계해야 합니다."
        },
        "transcript_text": """11월 미국 대선이 코앞으로 다가왔습니다. 금융시장은 트럼프 2기 가능성에 따른 '트럼프 트레이드'를 가격에 반영하기 시작했습니다.
만약 공화당이 백악관과 상하원을 모두 장악하는 레드 스윕(Red Sweep)이 일어난다면 법인세 인하 기대감으로 미국 주식 시장은 단기 랠리를 펼칠 수 있습니다.
그러나 그 이면에는 10~20%의 보편적 관세 부과와 대중국 60% 관세 폭탄이라는 무서운 인플레이션 트리거가 숨어있습니다.
이로 인해 연준의 금리 인하 경로가 막히고 미 국채 금리가 다시 치솟을 수 있습니다.
따라서 무차별적인 추격 매수보다는 변동성에 강한 헬스케어, 필수소비재 등 방어적 가치주를 담아두고 불확실성이 걷힐 때까지 현금 비중을 유지하는 방망이를 짧게 잡는 전략이 요구됩니다."""
    },

    # 11. 홍춘욱 - 2024 상반기 (원달러 환율 1400원 돌파와 달러 스위칭 전략)
    {
        "video_id": "HCW_2024_01",
        "title": "원달러 환율 1,400원 시대! 지금 달러를 사야 할까, 팔아야 할까? (홍춘욱 박사)",
        "channel_title": "매부리TV",
        "channel_id": "UC_Maeburi",
        "analyst_name": "홍춘욱",
        "category": "환율/원자재",
        "published_at": "2024-04-18",
        "video_url": "https://www.youtube.com/watch?v=2R0pEflchiY",
        "thumbnail_url": "https://img.youtube.com/vi/2R0pEflchiY/hqdefault.jpg",
        "view_count": 380000,
        "duration_sec": 2700,
        "period_label": "2024-H1",
        "sentiment_label": "neutral",
        "sentiment_score": 0.1,
        "summary_text": "원달러 환율 1400원은 위기 국면의 신호이기도 하지만, 기존에 보유한 달러 자산을 차익 실현하여 저평가된 한국 우량주나 배당주로 갈아타는 '달러 스위칭'의 결정적 기회입니다.",
        "opinion": {
            "topic": "환율/달러자산",
            "stance": "Neutral",
            "core_argument": "환율이 급등할 때 뒤늦게 달러를 추격 매수하기보다는, 달러 자산의 환차익을 실현하고 공포에 질린 국내 자산을 분할 매수하는 역발상 투자가 주효함.",
            "key_quote": "달러는 평소 환율이 낮을 때 보험처럼 사두고, 1400원처럼 환율이 치솟아 모두가 공포에 떨 때 원화 자산으로 바꾸는 자산배분의 도구입니다."
        },
        "transcript_text": """프리즘투자자문 홍춘욱입니다. 중동 지정학적 충돌과 미국의 금리 인하 지연으로 환율이 심리적 저항선인 1400원을 터치했습니다.
국민연금과 한국은행의 외환스왑이 가동될 만큼 외환당국의 긴장감도 극에 달해 있습니다.
여기서 일반 투자자들이 가장 많이 저지르는 실수가 있습니다. 바로 환율이 꼭대기에 도달했을 때 달러 예금에 가입하거나 달러 ETF를 사는 것입니다.
역사적으로 환율 1400원은 달러를 매수할 타이밍이 아니라 분할 매도하여 큰 환차익을 챙길 타이밍입니다.
이렇게 챙긴 원화 현금으로 코스피가 폭락했을 때 바닥에 떨어진 삼성전자나 현대차, 배당주를 헐값에 매수하는 '달러 스위칭 전략'이야말로 경제 위기 속에서 자산을 퀀텀 점프시키는 최고의 비결입니다."""
    },

    # 12. 홍춘욱 - 2024 하반기 (부동산 양극화와 주담대 대출 규제의 여파)
    {
        "video_id": "HCW_2024_02",
        "title": "서울 아파트 신고가 행진과 2단계 스트레스 DSR, 부동산 시장의 미래는? (홍춘욱)",
        "channel_title": "월급쟁이부자들TV",
        "channel_id": "UC_Weolbu",
        "analyst_name": "홍춘욱",
        "category": "부동산",
        "published_at": "2024-09-05",
        "video_url": "https://www.youtube.com/watch?v=VnrkN0o_6Do",
        "thumbnail_url": "https://img.youtube.com/vi/VnrkN0o_6Do/hqdefault.jpg",
        "view_count": 450000,
        "duration_sec": 3100,
        "period_label": "2024-H2",
        "sentiment_label": "caution",
        "sentiment_score": -0.15,
        "summary_text": "신축 아파트 공급 절벽으로 서울 핵심지 신축 선호는 지속되겠으나, 2단계 스트레스 DSR 대출 조이기로 중저가 외곽 지역의 거래량 급감 및 가격 양극화가 심화될 것입니다.",
        "opinion": {
            "topic": "부동산",
            "stance": "Caution",
            "core_argument": "입주 물량 부족에 따른 전세가 상승이 하방을 지지하지만, 금융당국의 가계대출 총량 규제로 매수 심리가 일시 냉각되며 똘똘한 한 채 쏠림 가속화.",
            "key_quote": "전국 부동산이 다 오르는 시대는 끝났습니다. 공급 부족이 확실한 강남3구와 마용성 신축만이 살아남는 초양극화 장세입니다."
        },
        "transcript_text": """9월부터 2단계 스트레스 DSR이 본격 시행되면서 은행권의 주택담보대출 한도가 수천만 원씩 깎이고 있습니다.
이로 인해 올여름 뜨겁게 달아올랐던 서울 아파트 매수 열기도 한풀 꺾이는 조정을 겪고 있습니다.
하지만 우리가 놓치지 말아야 할 구조적 팩트가 있습니다. 바로 향후 3~4년간 서울의 아파트 입주 물량이 반토막 난다는 사실입니다.
공사비 폭등으로 재건축 재개발 조합들이 시공사와 분쟁을 겪으며 착공을 못 하고 있습니다.
대출 규제로 인해 단기적인 거래 절벽은 불가피하겠지만, 전세 가격의 구조적 상승이 매매 가격의 하방을 단단하게 지지할 것입니다.
지방과 수도권 외곽의 미분양은 늘어나고 서울 핵심지는 매물 부족이 이어지는 '디커플링'에 대비하셔야 합니다."""
    },

    # 13. 슈카 - 2024 상반기 (엔비디아 시총 1위와 AI 패권 전쟁)
    {
        "video_id": "SYK_2024_01",
        "title": "엔비디아 전 세계 시총 1위 등극! 젠슨 황의 독점은 영원할 수 있을까? (슈카월드)",
        "channel_title": "슈카월드",
        "channel_id": "UC_Syuka",
        "analyst_name": "슈카",
        "category": "미국주식/글로벌",
        "published_at": "2024-06-20",
        "video_url": "https://www.youtube.com/watch?v=LU6GPSKaFnk",
        "thumbnail_url": "https://img.youtube.com/vi/LU6GPSKaFnk/hqdefault.jpg",
        "view_count": 1250000,
        "duration_sec": 3600,
        "period_label": "2024-H1",
        "sentiment_label": "bullish",
        "sentiment_score": 0.5,
        "summary_text": "엔비디아가 마이크로소프트와 애플을 제치고 전 세계 시총 1위에 등극했으며, 쿠다(CUDA) 생태계를 기반으로 한 AI 하드웨어 독점권이 언제까지 유지될지가 핵심 쟁점입니다.",
        "opinion": {
            "topic": "AI/빅테크",
            "stance": "Bullish",
            "core_argument": "단순한 칩 제조사가 아니라 소프트웨어 쿠다 플랫폼과 네트워킹(인피니밴드)을 장악한 인프라 제국으로서의 독점 프리미엄.",
            "key_quote": "과거 골드러시 때 청바지와 곡괭이를 판 리바이스처럼, 지금 AI 골드러시의 모든 돈은 엔비디아의 금고로 빨려 들어가고 있습니다."
        },
        "transcript_text": """여러분 안녕하십니까 슈카입니다. 드디어 역사적인 날이 왔습니다. 엔비디아 시가총액이 3조 3천억 달러를 찍으면서 마이크로소프트와 애플을 제치고 전 세계에서 가장 비싼 회사가 되었습니다.
불과 2년 전만 해도 코인 채굴 끝나서 그래픽카드 재고 쌓인다고 조롱받던 회사가 말이죠.
어떻게 이런 일이 가능했을까요? 젠슨 황이 15년 전부터 적자를 감수하며 밀어붙인 쿠다(CUDA)라는 소프트웨어 플랫폼 때문입니다.
전 세계 모든 AI 연구자들의 코드가 쿠다에 묶여있어서 다른 AMD나 인텔 칩을 쓰고 싶어도 쓸 수가 없는 락인(Lock-in) 효과가 발생한 겁니다.
물론 빅테크들이 자체 칩(ASIC)을 개발하며 반(反) 엔비디아 동맹을 구축하고 있지만, 적어도 차세대 블랙웰(Blackwell) 아키텍처가 시장을 지배하는 1~2년 동안은 엔비디아의 독주 체제를 깨뜨리기가 대단히 어려워 보입니다."""
    },

    # 14. 슈카 - 2024 하반기 (금융투자소득세 논란과 코리아 디스카운트)
    {
        "video_id": "SYK_2024_02",
        "title": "금투세 폐지 확정! 그런데도 왜 한국 주식만 떨어질까? 국장의 씁쓸한 현실 (슈카)",
        "channel_title": "슈카월드",
        "channel_id": "UC_Syuka",
        "analyst_name": "슈카",
        "category": "국내주식",
        "published_at": "2024-11-05",
        "video_url": "https://www.youtube.com/watch?v=6N3btEOu9W4",
        "thumbnail_url": "https://img.youtube.com/vi/6N3btEOu9W4/hqdefault.jpg",
        "view_count": 1420000,
        "duration_sec": 3800,
        "period_label": "2024-H2",
        "sentiment_label": "bearish",
        "sentiment_score": -0.6,
        "summary_text": "금투세 폐지 결정에도 불구하고 코스피가 반등하지 못하는 본질은, 물적분할과 대주주 이익 우선주의 등 일반 주주를 보호하지 못하는 한국 상법 구조와 거버넌스 후진성 때문입니다.",
        "opinion": {
            "topic": "국내주식/제도개선",
            "stance": "Bearish",
            "core_argument": "세금 이슈는 표면적인 요인일 뿐이며, 일반 주주에 대한 이사의 충실 의무 명시와 같은 근본적인 상법 개정이 없이는 해외 주식으로의 서학개미 이탈을 막을 수 없음.",
            "key_quote": "돈을 벌면 물적분할로 쪼개서 상장하고, 회사가 유상증자로 일반 주주 지분을 희석시키는데 누가 국장에 장기 투자를 하겠습니까?"
        },
        "transcript_text": """슈카입니다. 많은 분들이 기다리셨던 금융투자소득세(금투세)가 결국 백지화 폐지되는 방향으로 결론이 났습니다.
시장에선 불확실성이 해소되었으니 코스피가 떡상할 것이라 기대했죠. 하지만 뚜껑을 열어보니 어땠습니까? 미국 S&P500과 나스닥이 사상 최고치를 달릴 때 코스피는 연중 신저가를 헤매고 있습니다.
투자자들의 절망감이 커지고 있는데요, 사실 세금은 핑계였을 뿐입니다.
진짜 문제는 '기업 거버넌스'입니다. 한국 상법 382조 3항에 이사의 충실의무 대상이 오직 '회사'로만 되어 있어서, 대주주의 지배력을 위해 일반 주주에게 손해를 끼쳐도 법적으로 배임죄 처벌을 못 받습니다.
알짜 사업부를 쪼개서 중복 상장하고, 합병 비율을 대주주에게 유리하게 조작하는 일이 반복되니 서학개미들이 국장을 버리고 미장으로 탈출하는 것입니다."""
    },

    # 15. 강환국 - 2024 상반기 (계절성 11월-4월 효과와 자산배분 전략)
    {
        "video_id": "KHK_2024_01",
        "title": "5월엔 주식을 팔고 떠나라(Sell in May)? 통계가 증명하는 퀀트 투자 법칙 (강환국)",
        "channel_title": "할 수 있다! 알고 투자",
        "channel_id": "UC_KangAlgo",
        "analyst_name": "강환국",
        "category": "거시경제/금리",
        "published_at": "2024-04-25",
        "video_url": "https://www.youtube.com/watch?v=yXErJWoxO6o",
        "thumbnail_url": "https://img.youtube.com/vi/yXErJWoxO6o/hqdefault.jpg",
        "view_count": 210000,
        "duration_sec": 1950,
        "period_label": "2024-H1",
        "sentiment_label": "neutral",
        "sentiment_score": 0.0,
        "summary_text": "역사적으로 11월~4월 수익률이 5월~10월보다 월등히 높은 '핼러윈 효과'가 존재하므로, 5월부터는 주식 비중을 줄이고 단기 채권 및 금 자산으로 피신하는 계절성 전략이 유리합니다.",
        "opinion": {
            "topic": "퀀트/계절성",
            "stance": "Neutral",
            "core_argument": "감정적 매매를 배제하고 지난 100년간 검증된 계절성 통계와 동적 자산배분(Dynamic Asset Allocation) 규칙을 따르는 것이 장기 복리 승리의 지름길.",
            "key_quote": "주식시장에서 가장 확실한 엣지(Edge) 중 하나는 계절성입니다. 5월부터 10월까지는 현금 보유가 주식보다 마음도 편하고 수익률도 좋습니다."
        },
        "transcript_text": """안녕하세요 퀀트 투자자 강환국입니다. 월가의 오래된 격언 중에 'Sell in May and Go Away'라는 말이 있습니다.
한국 증시와 미국 증시의 1980년대 이후 데이터를 백테스트해보면 놀랍게도 11월 1일부터 다음 해 4월 30일까지의 수익률이 1년 전체 수익률의 80% 이상을 차지합니다.
반대로 5월부터 10월까지는 횡보하거나 급락장이 자주 발생했습니다.
여름 휴가철 거래량 감소와 기업 실적 공백기가 맞물리기 때문입니다.
따라서 적극적인 주식 비중 확대는 11월로 미루고, 5월부터는 미국 초단기 국채(SGOV)나 단기 예금, 금(Gold)에 자금을 파킹해 두는 것이 리스크 대비 수익률을 극대화하는 정석 퀀트 전략입니다."""
    },

    # =========================================================================
    # 2026년 10월 현재 기준 최신 데이터 (Current October 2026 Records)
    # =========================================================================

    # 16. 오건영 - 2026년 10월 (연준 중립금리 도달과 2차 인플레 경계)
    {
        "video_id": "OGY_2026_10",
        "title": "2026년 10월 연준 중립금리 도달과 2차 인플레 경계: 금리 인하 사이클 끝났나? (오건영)",
        "channel_title": "삼프로TV",
        "channel_id": "UC_3proTV",
        "analyst_name": "오건영",
        "category": "거시경제/금리",
        "published_at": "2026-10-05",
        "video_url": "https://www.youtube.com/watch?v=UKkhP-56TSc",
        "thumbnail_url": "https://img.youtube.com/vi/UKkhP-56TSc/hqdefault.jpg",
        "view_count": 540000,
        "duration_sec": 3200,
        "period_label": "2026-10",
        "sentiment_label": "caution",
        "sentiment_score": -0.25,
        "summary_text": "2024~2025년의 완화 사이클을 거쳐 연준 기준금리가 3%대 초반 중립금리에 안착했으나, 중동 지정학적 유가 불안과 재정적자로 인한 2차 인플레이션 압력으로 추가 금리 인하는 제한적입니다.",
        "opinion": {
            "topic": "금리/통화정책",
            "stance": "Caution",
            "core_argument": "연준의 금리 인하 사이클은 사실상 마무리 단계에 진입했으며, 실질 금리의 상방 압력과 국채 발행 부담에 대비한 보수적 자산배분이 필요함.",
            "key_quote": "금리 인하의 단물은 이제 끝났습니다. 2026년 가을부터는 재정 인플레이션과 실질 금리의 균형점을 주시해야 합니다."
        },
        "transcript_text": """신한은행 오건영입니다. 2026년 10월 현재, 금융시장은 중요한 분곡점에 서 있습니다.
연준이 지난 2년간 누적 200bp가 넘는 금리 인하를 단행하면서 기준금리는 마침내 연준이 산정하는 중립금리(3.0~3.25%) 영역에 도달했습니다.
문제는 시장이 기대하는 2%대 초저금리로의 복귀는 구조적으로 불가능하다는 점입니다.
미국의 만성적인 재정적자와 국채 발행 급증, 그리고 공급망 블록화로 인해 기간 프리미엄이 다시 상승하고 있습니다.
게다가 최근 중동 원유 수송로 긴장으로 국제유가가 배럴당 85달러선을 위협하면서 '2차 인플레이션 반등(Second Wave)'에 대한 연준 위원들의 경계감이 극에 달해 있습니다.
따라서 추가 인하를 기대한 위험자산 추격 매수보다는, 단기 국채와 실물 금, 배당 현금흐름이 탄탄한 가치주 비중을 유지하는 방어적 스탠스가 절실합니다."""
    },

    # 17. 염승환 - 2026년 10월 (HBM4 본격 양산과 피지컬 AI 로봇 수혜)
    {
        "video_id": "YSH_2026_10",
        "title": "HBM4 첫 양산 돌입과 피지컬 AI 로봇 수혜주! 2026년 4분기 코스피 주도주 총정리 (염승환)",
        "channel_title": "LS증권 이베스트투자증권",
        "channel_id": "UC_LSsec",
        "analyst_name": "염승환",
        "category": "국내주식",
        "published_at": "2026-10-08",
        "video_url": "https://www.youtube.com/watch?v=WuMG-B8wiKo",
        "thumbnail_url": "https://img.youtube.com/vi/WuMG-B8wiKo/hqdefault.jpg",
        "view_count": 610000,
        "duration_sec": 3500,
        "period_label": "2026-10",
        "sentiment_label": "bullish",
        "sentiment_score": 0.75,
        "summary_text": "차세대 엔비디아 루빈(Rubin) 플랫폼에 탑재될 16단 HBM4 메모리의 국내 기업 독점 공급과 휴머노이드 로봇(피지컬 AI) 감속기·액추에이터 부품사들의 본격적인 양산 실적 랠리가 시작됩니다.",
        "opinion": {
            "topic": "AI/반도체",
            "stance": "Bullish",
            "core_argument": "2024년이 HBM3E 학습용 AI였다면, 2026년 10월은 HBM4 커스텀 베이스다이 공정과 피지컬 AI 로봇 실적 상용화의 폭발적 원년임.",
            "key_quote": "2026년 4분기는 기대감이 아닌 수주 잔고와 분기 흑자로 입증되는 피지컬 AI 하드웨어 슈퍼사이클입니다."
        },
        "transcript_text": """염블리 염승환입니다. 2026년 10월 국내 증시에서 가장 뜨거운 모멘텀은 단연 6세대 고대역폭메모리인 HBM4의 첫 양산 출하입니다.
기존 HBM3E까지는 메모리 공정으로만 만들어졌지만, HBM4부터는 TSMC와 삼성전자 파운드리의 첨단 로직 공정을 활용한 맞춤형(Customized) 베이스다이가 적용됩니다.
SK하이닉스와 삼성전자가 엔비디아 루빈 GPU 공급망을 확고히 장악하고 있으며, 대만 파운드리와의 협력도 사상 최고 수준입니다.
여기에 테슬라의 옵티머스 3세대와 현대차의 보스턴다이내믹스 아틀라스 로봇이 공장에 대량 투입되면서, 감속기, 관절 모터, 초소형 센서를 공급하는 국내 로봇 밸류체인의 주문이 폭발하고 있습니다.
지수 박스권에 갇히지 말고 HBM4와 피지컬 AI 밸류체인 핵심 대장주를 적극 비중 확대하시기 바랍니다."""
    },

    # 18. 김일구 - 2026년 10월 (금 3,000달러 돌파와 글로벌 탈달러화)
    {
        "video_id": "KIK_2026_10",
        "title": "금(Gold) 3,000달러 시대의 경고, 달러 패권의 다극화와 글로벌 화폐 질서의 재편 (김일구)",
        "channel_title": "한경 코리아마켓",
        "channel_id": "UC_HKmarket",
        "analyst_name": "김일구",
        "category": "환율/원자재",
        "published_at": "2026-10-03",
        "video_url": "https://www.youtube.com/watch?v=x6g1lo6pYT4",
        "thumbnail_url": "https://img.youtube.com/vi/x6g1lo6pYT4/hqdefault.jpg",
        "view_count": 490000,
        "duration_sec": 3100,
        "period_label": "2026-10",
        "sentiment_label": "caution",
        "sentiment_score": -0.2,
        "summary_text": "국제 금 가격이 사상 최초로 온스당 3,000달러를 돌파한 것은 전 세계 중앙은행들의 통화 발행 불신과 지정학적 달러 무기화에 대한 구조적 저항의 결과입니다.",
        "opinion": {
            "topic": "환율/금",
            "stance": "Caution",
            "core_argument": "미국 재정적자 고착화와 국채 이자 비용 폭증으로 글로벌 기축통화 단일 체제가 흔들리고 있으며, 실물 자산으로의 구조적 자금 이동이 가속화됨.",
            "key_quote": "금 가격이 3,000달러를 뚫었다는 것은 화폐 시스템에 대한 전 세계의 불신이 구조적으로 고착화되었음을 의미합니다."
        },
        "transcript_text": """한화투자증권 김일구입니다. 2026년 10월 첫째 주, 금융 역사상 기념비적인 이정표가 세워졌습니다. 바로 금 가격이 온스당 3,000달러 고지를 넘어섰습니다.
많은 이들이 이를 단순한 원자재 투기나 단기 인플레이션 헤지로 보지만 본질은 전혀 다릅니다.
중국, 인도, 사우디 등 비서방 신흥국 중앙은행들이 미 국채 보유량을 줄이고 대신 외환보유액의 실물 금 비중을 20% 이상으로 끌어올리고 있습니다.
달러화의 일방적 독점 질서가 다극화(Multipolar) 통화 체제로 이행하고 있는 증거입니다.
미국의 부채는 37조 달러를 넘어서고 있습니다. 장기 금리의 하방은 단단히 막혀 있으며, 화폐 가치의 영구적 절하를 방어할 수 있는 실물 금과 독점적 비즈니스 모델을 갖춘 핵심 기업 보유가 필수적입니다."""
    },

    # 19. 이선엽 - 2026년 10월 (AI 에이전트 소프트웨어와 소형원전 SMR 실적 장세)
    {
        "video_id": "LSY_2026_10",
        "title": "AI 에이전트와 소형원전 SMR이 이끄는 실적 장세! 2026년 10월 주도 섹터 톱픽 (이선엽)",
        "channel_title": "달란트투자",
        "channel_id": "UC_Dalant",
        "analyst_name": "이선엽",
        "category": "미국주식/글로벌",
        "published_at": "2026-10-07",
        "video_url": "https://www.youtube.com/watch?v=HEKkMZD0aYU",
        "thumbnail_url": "https://img.youtube.com/vi/HEKkMZD0aYU/hqdefault.jpg",
        "view_count": 670000,
        "duration_sec": 3300,
        "period_label": "2026-10",
        "sentiment_label": "bullish",
        "sentiment_score": 0.8,
        "summary_text": "빅테크 기업들이 AI 데이터센터 전력 확보를 위해 원전 스타트업 및 한전·두산에너빌리티의 SMR에 20년 장기 전력구매계약(PPA)을 맺으면서 원전 르네상스가 실적으로 확인되고 있습니다.",
        "opinion": {
            "topic": "AI/에너지인프라",
            "stance": "Bullish",
            "core_argument": "2024년 변압기 쇼티지에 이어 2026년은 SMR 원전과 초고압 직류송전(HVDC), 자율 AI 에이전트 소프트웨어 기업들이 실적 어닝 서프라이즈를 주도함.",
            "key_quote": "빅테크들이 전력 확보를 위해 원전을 통째로 사들이고 있습니다. 2026년은 상상이 실적 숫자로 증명되는 실적 장세입니다."
        },
        "transcript_text": """신한투자증권 이선엽입니다. 2026년 10월 시장을 관통하는 최대의 키워드는 '전력 독점'과 '자율 AI 에이전트'입니다.
오픈AI, 구글, 마이크로소프트가 발표한 자율 에이전트들은 이제 단순한 대화형 챗봇을 넘어 코딩, 회계, 법률 업무를 스스로 처리하는 실질적 생산성 도구로 자리잡았습니다.
이로 인해 데이터센터 전력 소모량은 2024년 대비 3배 이상 폭증했습니다.
해결책은 24시간 청정 기저부하를 공급하는 소형모듈원전(SMR)뿐입니다. 아마존과 구글이 수조 원대 원전 PPA 계약을 발표하면서 한국의 원전 기자재와 주기기 공급사들의 수주 파이프라인이 2030년까지 매진되었습니다.
테마성 급등락을 넘어 실제 영업이익이 폭증하는 SMR과 전력망, 엔터프라이즈 AI 에이전트 종목군을 놓쳐선 안 됩니다."""
    },

    # 20. 박석중 - 2026년 10월 (글로벌 공급망 블록화와 4분기 글로벌 자산배분)
    {
        "video_id": "PSJ_2026_10",
        "title": "2026년 미국 신정부 관세 전쟁 2년차, 글로벌 공급망 블록화와 4분기 자산배분 (박석중)",
        "channel_title": "김작가 TV",
        "channel_id": "UC_KimAuthor",
        "analyst_name": "박석중",
        "category": "미국주식/글로벌",
        "published_at": "2026-10-06",
        "video_url": "https://www.youtube.com/watch?v=AL127vDKsRU",
        "thumbnail_url": "https://img.youtube.com/vi/AL127vDKsRU/hqdefault.jpg",
        "view_count": 720000,
        "duration_sec": 3600,
        "period_label": "2026-10",
        "sentiment_label": "caution",
        "sentiment_score": -0.1,
        "summary_text": "미국 신정부의 전방위 보편관세 시행 2년차를 맞아 글로벌 교역량이 둔화되고 있으며, 공급망 블록화 속에서 미국 내 자체 생산 거점을 확보한 현지화 완결형 기업 중심의 압축 전략이 필수적입니다.",
        "opinion": {
            "topic": "글로벌자산배분",
            "stance": "Caution",
            "core_argument": "자유무역 체제의 완전한 종언과 무역 장벽 심화로 수출 의존도가 높은 국가들은 구조적 밸류에이션 디스카운트를 겪을 수밖에 없음.",
            "key_quote": "글로벌 분업의 시대는 영구히 끝났습니다. 프렌드쇼어링(Friendshoring)과 현지화 완결형 기업만이 살아남습니다."
        },
        "transcript_text": """신한투자증권 박석중입니다. 2026년 10월 글로벌 경제를 조망할 때 가장 무서운 변수는 공급망의 진영화와 관세 장벽의 일상화입니다.
보편관세와 대중국 추가 관세가 법제화되면서 전 세계 교역 탄력성이 뚜렷하게 둔화되고 있습니다.
한국, 대만, 유럽과 같은 대외 수출 의존도가 높은 국가의 기업들은 미국 현지 공장 없이는 관세 폭탄을 감당할 수 없는 구조가 고착화되었습니다.
반면 미국 내 현지 생산 투자를 선제적으로 완료한 반도체, 자동차, 바이오 위탁생산(CDMO) 대형사들은 오히려 경쟁사 대비 시장 점유율을 독식하고 있습니다.
따라서 글로벌 포트폴리오를 구성할 때는 단순 국가별 비중이 아니라, '관세 회피 능력과 현지 제조 생태계를 구축했는가'를 절대적 기준으로 삼아야 합니다."""
    },

    # 21. 홍춘욱 - 2026년 10월 (서울 입주 절벽 현실화와 전세가율 상승)
    {
        "video_id": "HCW_2026_10",
        "title": "2026년 서울 아파트 입주 절벽 현실화! 전세가 급등과 스트레스 DSR 3단계 후폭풍 (홍춘욱)",
        "channel_title": "월급쟁이부자들TV",
        "channel_id": "UC_Weolbu",
        "analyst_name": "홍춘욱",
        "category": "부동산",
        "published_at": "2026-10-04",
        "video_url": "https://www.youtube.com/watch?v=8oJt0qKzrPo",
        "thumbnail_url": "https://img.youtube.com/vi/8oJt0qKzrPo/hqdefault.jpg",
        "view_count": 580000,
        "duration_sec": 3200,
        "period_label": "2026-10",
        "sentiment_label": "neutral",
        "sentiment_score": 0.1,
        "summary_text": "2023~2024년 착공 절벽의 청구서가 2026년 서울 아파트 입주 물량 급감으로 돌아왔으며, 전세가율 상승이 매매가 하방을 지지하지만 대출 한도 축소로 똘똘한 한 채 초양극화가 전개됩니다.",
        "opinion": {
            "topic": "부동산",
            "stance": "Neutral",
            "core_argument": "서울 신축의 절대적 공급 부족으로 전세가 상승세가 꺾이지 않고 있으나, 스트레스 DSR 3단계 전면 도입으로 매수 여력이 고소득층으로 제한되며 가격 양극화 심화.",
            "key_quote": "공급이 없는 곳에 가격 폭락은 없습니다. 서울 핵심 신축과 외곽 구축 간의 디커플링은 2026년 가을 더욱 극단적으로 벌어지고 있습니다."
        },
        "transcript_text": """프리즘투자자문 홍춘욱입니다. 과거 2~3년 전부터 수없이 경고했던 '2026년 서울 입주 절벽'이 지금 현실의 숫자로 눈앞에 펼쳐지고 있습니다.
올해 2026년 서울 아파트 입주 물량은 연간 1만 가구 수준으로 떨어져 통계 작성 이래 최저치를 기록했습니다.
공사비 갈등으로 재건축이 멈췄던 결과가 지금의 공급 공백을 만든 것입니다.
이로 인해 서울 주요 선호 지역의 전세가율이 60%를 넘어서며 매매 가격을 밀어 올리는 지지선 역할을 하고 있습니다.
다만 가계대출을 옥죄는 스트레스 DSR 3단계 규제가 완전 정착되었기 때문에, 과거처럼 무차별적인 갭투자는 원천 차단되었습니다.
결국 자금 여력이 되는 실수요자들이 강남3구와 마용성, 한강변 신축으로 몰리며 초양극화가 고착화되고 있습니다."""
    },

    # 22. 슈카 - 2026년 10월 (AI 데이터센터 전력 대란과 밸류업 2년 성적표)
    {
        "video_id": "SYK_2026_10",
        "title": "2026년 AI 데이터센터 전력 대란과 빅테크 원전 쇼핑, 그리고 코리아 밸류업 2년의 현실 (슈카)",
        "channel_title": "슈카월드",
        "channel_id": "UC_Syuka",
        "analyst_name": "슈카",
        "category": "국내주식",
        "published_at": "2026-10-09",
        "video_url": "https://www.youtube.com/watch?v=Ruy1k7ym4VI",
        "thumbnail_url": "https://img.youtube.com/vi/Ruy1k7ym4VI/hqdefault.jpg",
        "view_count": 1580000,
        "duration_sec": 3950,
        "period_label": "2026-10",
        "sentiment_label": "neutral",
        "sentiment_score": 0.2,
        "summary_text": "아마존과 마이크로소프트가 원전을 통째로 인수할 정도로 2026년 AI 전력 대란이 현실화되었으며, 국내 밸류업 2년차를 맞아 주주환원 우수 기업과 만성 저평가 기업의 양극화가 뚜렷해졌습니다.",
        "opinion": {
            "topic": "국내주식/AI트렌드",
            "stance": "Neutral",
            "core_argument": "전력망과 원자력 발전은 AI 패권의 필수 인프라로 확고히 자리 잡았으며, 상법 개정과 배당 분리과세를 적극 수용한 국내 상장사들만이 리레이팅에 성공함.",
            "key_quote": "AI가 전기를 너무 먹어서 빅테크들이 원전을 통째로 사들이는 세상입니다. 변화에 적응하는 기업과 과거에 안주하는 시장의 격차가 극명해졌습니다."
        },
        "transcript_text": """여러분 안녕하십니까 슈카입니다. 2026년 10월 지금 전 세계 테크 판에서 가장 황당하면서도 거대한 뉴스는 바로 빅테크들의 '원전 쇼핑'입니다.
AI 모델 파라미터가 수십조 개로 커지고 추론 데이터센터가 전 세계에 깔리다 보니 전력망이 버티질 못하는 겁니다.
결국 아마존과 마이크로소프트는 폐쇄되었던 원전을 재가동하고 SMR 기업에 수십조 원을 쏟아붓고 있습니다. 기술의 끝판왕이 결국 1950년대의 원자력 에너지로 회귀한 셈이죠.
한편 한국 증시를 돌아보면 정부가 밸류업 프로그램을 시작한 지 벌써 2년 반이 흘렀습니다.
자사주를 소각하고 배당 성향을 40% 이상으로 끌어올린 알짜 기업들은 외국인 매수세와 함께 52주 신고가를 쓰고 있지만, 여전히 대주주 이익만 챙기는 구태 기업들은 서학개미들의 철저한 외면을 받고 있습니다.
이제 국장에서도 옥석 가리기가 완전히 자리 잡은 2026년의 가을입니다."""
    },

    # 23. 강환국 - 2026년 10월 (11월 랠리 D-28 계절성 퀀트 매수 시그널)
    {
        "video_id": "KHK_2026_10",
        "title": "드디어 11월 핼러윈 랠리 D-28! 2026년 가을 퀀트 모멘텀 종목 대공개 (강환국)",
        "channel_title": "할 수 있다! 알고 투자",
        "channel_id": "UC_KangAlgo",
        "analyst_name": "강환국",
        "category": "거시경제/금리",
        "published_at": "2026-10-02",
        "video_url": "https://www.youtube.com/watch?v=_6xMEAPEWOA",
        "thumbnail_url": "https://img.youtube.com/vi/_6xMEAPEWOA/hqdefault.jpg",
        "view_count": 280000,
        "duration_sec": 2100,
        "period_label": "2026-10",
        "sentiment_label": "bullish",
        "sentiment_score": 0.85,
        "summary_text": "5~10월의 지루한 박스권 계절성을 지나 통계적으로 가장 높은 승률(82%)을 자랑하는 11월~4월 랠리 진입 직전으로, 10월 하순이 연중 최고의 분할 매수 적기입니다.",
        "opinion": {
            "topic": "퀀트/계절성",
            "stance": "Bullish",
            "core_argument": "지난 100년간 검증된 11월-4월 효과는 2026년에도 유효하며, 12개월 모멘텀 상위 팩터와 영업이익 흑자전환 소형주에 자금을 투입할 타이밍.",
            "key_quote": "지루했던 여름장이 끝나고 10월 바닥 확인 후 11월부터는 계절성 퀀트의 골든 타임입니다. 지금이 주식을 주워 담을 시점입니다."
        },
        "transcript_text": """안녕하세요 퀀트 투자자 강환국입니다. 2026년 10월이 시작되었습니다.
올해 5월부터 9월까지 제 말 듣고 현금이나 미국 단기채에 파킹해 두셨던 분들은 변동성 피하고 이자 잘 챙기셨을 겁니다.
하지만 이제 방어 모드를 해제하고 공격 모드로 전환할 때가 왔습니다. 11월 1일부터 시작되는 '11월~4월 핼러윈 효과'가 코앞으로 다가왔기 때문입니다.
미국 S&P500이든 코스닥이든 10월 중순부터 기관과 펀드의 연말 윈도우드레싱과 계절적 자금 유입이 시작됩니다.
현재 백테스트 상으로 가장 유망한 팩터는 최근 1년간 주가 상승률 상위(12M 모멘텀)이면서 2026년 3분기 실적이 컨센서스를 상회한 기업들입니다.
감정에 휘둘리지 말고 10월 한 달 동안 원칙대로 분할 매수해 두면 내년 봄에 활짝 웃으실 수 있습니다."""
    },

    # 24. 오건영 - 2026년 상반기 (글로벌 환율 전쟁과 엔화·위안화의 향방)
    {
        "video_id": "OGY_2026_01",
        "title": "2026년 글로벌 환율 전쟁과 엔화·위안화의 향방, 한은의 금리 딜레마 (오건영)",
        "channel_title": "삼프로TV",
        "channel_id": "UC_3proTV",
        "analyst_name": "오건영",
        "category": "거시경제/금리",
        "published_at": "2026-04-18",
        "video_url": "https://www.youtube.com/watch?v=iGZDaJ14hZs",
        "thumbnail_url": "https://img.youtube.com/vi/iGZDaJ14hZs/hqdefault.jpg",
        "view_count": 470000,
        "duration_sec": 2850,
        "period_label": "2026-H1",
        "sentiment_label": "neutral",
        "sentiment_score": 0.0,
        "summary_text": "일본은행의 추가 금리 인상과 중국의 경기부양책이 맞물리며 아시아 통화 가치가 급변하는 가운데, 한국은행의 가계부채 관리와 내수 부양 간의 정책 딜레마를 진단합니다.",
        "opinion": {
            "topic": "환율/외환",
            "stance": "Neutral",
            "core_argument": "엔화 강세 전환과 미 금리 격차 축소에도 불구하고, 내수 부진과 부동산 PF 연착륙 과제로 인해 한은의 정책 금리 인하 속도는 조절될 수밖에 없음.",
            "key_quote": "환율을 잡자니 내수가 울고, 금리를 내리자니 수도권 부동산과 환율이 불안해지는 복합 방정식입니다."
        },
        "transcript_text": """신한은행 오건영입니다. 2026년 상반기 외환시장의 가장 큰 충격은 일본은행(BOJ)의 정책금리 인상 기조와 엔 캐리 트레이드 청산 압력입니다.
엔달러 환율이 140엔대 초반으로 내려앉으면서 원달러 환율도 연동되어 변동성을 키우고 있습니다.
한국은행 입장에서는 수출 기업들의 가격 경쟁력과 내수 자영업자들의 고통을 덜어주기 위해 금리를 낮추고 싶지만, 서울 아파트값 자극 우려와 한미 금리 역전차 때문에 운신의 폭이 좁습니다.
다각적인 환율 시나리오에 대비한 포트폴리오 헤지가 필요합니다."""
    },

    # 25. 염승환 - 2026년 상반기 (코스피 3,200선 돌파 시도와 밸류업 2년차)
    {
        "video_id": "YSH_2026_01",
        "title": "2026년 코스피 3,200선 돌파 시도와 밸류업 2년차 주주환원 우수기업 (염승환)",
        "channel_title": "LS증권 이베스트투자증권",
        "channel_id": "UC_LSsec",
        "analyst_name": "염승환",
        "category": "국내주식",
        "published_at": "2026-03-25",
        "video_url": "https://www.youtube.com/watch?v=SfA_jWUXu6c",
        "thumbnail_url": "https://img.youtube.com/vi/SfA_jWUXu6c/hqdefault.jpg",
        "view_count": 520000,
        "duration_sec": 3100,
        "period_label": "2026-H1",
        "sentiment_label": "bullish",
        "sentiment_score": 0.7,
        "summary_text": "밸류업 지수 2년차 편입 종목들의 본격적인 자사주 매입·소각과 배당 확대 효과로 코스피 지수가 3,200선 돌파를 시도하며 만성 저평가 탈출에 시동을 걸고 있습니다.",
        "opinion": {
            "topic": "국내주식",
            "stance": "Bullish",
            "core_argument": "주주환원율 35% 이상 기업들에 대한 기관·외국인 패시브 수급 유입이 안정적으로 지속되면서 코스피 밸류에이션 밴드 상단이 열리고 있음.",
            "key_quote": "약속을 지키는 밸류업 기업들의 주가는 이미 레벨업되었습니다. 주주를 대우하는 기업이 이기는 시대가 왔습니다."
        },
        "transcript_text": """염블리 염승환입니다. 2026년 봄, 우리 코스피 시장이 드디어 3,200포인트 벽을 두드리고 있습니다.
2년 전 시작된 기업 밸류업 프로그램이 이제 실질적인 자본 효율성 개선으로 나타나고 있습니다.
배당소득 분리과세와 감액 배당 비과세 혜택을 등에 업고 금융, 지주, 자동차 기업들의 배당 수익률이 연 6~7%대에 달하면서 배당 재투자 선순환이 형성되었습니다.
여기에 반도체 수출 호조까지 더해져 외국인 순매수가 코스피로 집중되고 있습니다.
실적과 주주환원이 겸비된 밸류업 우수 기업들을 중심으로 포트폴리오를 꾸려가시기 바랍니다."""
    },

    # 26. 오건영 - 2026년 8월 (유가 급등과 연준 완화 속도 조절)
    {
        "video_id": "OGY_2026_08",
        "title": "중동 지정학적 긴장과 국제 유가 급등: 연준의 추가 금리 인하에 급제동 걸리나? (오건영)",
        "channel_title": "삼프로TV",
        "channel_id": "UC_3proTV",
        "analyst_name": "오건영",
        "category": "거시경제/금리",
        "published_at": "2026-08-15",
        "video_url": "https://www.youtube.com/watch?v=c20HyMONItU",
        "thumbnail_url": "https://img.youtube.com/vi/c20HyMONItU/hqdefault.jpg",
        "view_count": 460000,
        "duration_sec": 3000,
        "period_label": "2026-08",
        "sentiment_label": "caution",
        "sentiment_score": -0.3,
        "summary_text": "원유 수송로 분쟁으로 인한 유가 80달러선 재진입과 물가 반등 우려로, 연준의 하반기 추가 금리 인하 경로에 경계 신호가 켜졌습니다.",
        "opinion": {
            "topic": "금리/인플레이션",
            "stance": "Caution",
            "core_argument": "기대 인플레이션이 다시 고개를 들 경우 연준은 금리 인하 일시정지(Pause) 카드를 꺼낼 수밖에 없음.",
            "key_quote": "유가와 원자재는 인플레이션의 도화선입니다. 연준의 완화 사이클이 예상보다 일찍 멈출 가능성을 열어두어야 합니다."
        },
        "transcript_text": """신한은행 오건영입니다. 2026년 8월, 여름 휴가철 동안 국제 원유 시장에 심상치 않은 기류가 흐르고 있습니다.
호르무즈 해협을 둘러싼 지정학적 마찰로 유가가 배럴당 80달러를 돌파하면서 미국의 헤드라인 CPI 반등 우려가 커졌습니다.
연준은 물가가 완전히 잡히지 않은 상태에서 금리를 급격히 내리는 것을 극도로 두려워합니다.
만약 8월 고용과 물가 지표가 예상보다 견고하다면 가을 FOMC에서 금리 동결 신호가 나올 수 있습니다. 채권 금리 변동성과 달러화 반등에 유의하셔야 합니다."""
    },

    # 27. 염승환 - 2026년 8월 (HBM4 샘플 테스트와 소부장 수혜)
    {
        "video_id": "YSH_2026_08",
        "title": "HBM4 샘플 테스트 통과와 국내 소부장 수혜주: 차세대 AI 메모리 랠리 전초전 (염승환)",
        "channel_title": "LS증권 이베스트투자증권",
        "channel_id": "UC_LSsec",
        "analyst_name": "염승환",
        "category": "국내주식",
        "published_at": "2026-08-20",
        "video_url": "https://www.youtube.com/watch?v=p61QUjftYr0",
        "thumbnail_url": "https://img.youtube.com/vi/p61QUjftYr0/hqdefault.jpg",
        "view_count": 550000,
        "duration_sec": 3200,
        "period_label": "2026-08",
        "sentiment_label": "bullish",
        "sentiment_score": 0.8,
        "summary_text": "글로벌 빅테크 고객사의 HBM4 엔지니어링 샘플 승인 소식과 함께, 하이브리드 본딩 및 첨단 패키징 장비주들의 실적 반등이 가시화되고 있습니다.",
        "opinion": {
            "topic": "AI/반도체",
            "stance": "Bullish",
            "core_argument": "기존 본딩 방식을 뛰어넘는 하이브리드 본딩과 첨단 전공정 부품사들의 구조적 실적 도약이 임박함.",
            "key_quote": "HBM4는 기술 난이도가 극도로 높아 공급 과잉 우려가 없습니다. 기술 장벽을 뚫은 국내 소부장 기업들의 가치가 재평가될 것입니다."
        },
        "transcript_text": """염블리 염승환입니다. 2026년 8월 국내 반도체 섹터의 결정적 분기점은 HBM4 샘플 인증 완료입니다.
단순히 속도만 빠른 것이 아니라 발열과 전력 효율을 30% 이상 개선하면서 엔비디아의 차세대 루빈 GPU 성능을 온전히 구현할 유일한 대안으로 공인받았습니다.
특히 하이브리드 본딩 장비와 특수 CMP 슬러리 국산화에 성공한 중소형 소부장주들의 수주 모멘텀이 3분기부터 숫자로 찍히기 시작합니다. 가을 장세를 앞두고 눌림목 분할 매수 기회입니다."""
    },

    # 28. 홍춘욱 - 2026년 8월 (가을 이사철 전세 품귀와 신축 프리미엄)
    {
        "video_id": "HCW_2026_08",
        "title": "가을 이사철 앞둔 전세 매물 품귀와 신축 프리미엄: 서울 부동산 하반기 분기점 (홍춘욱)",
        "channel_title": "매부리TV",
        "channel_id": "UC_Maeburi",
        "analyst_name": "홍춘욱",
        "category": "부동산",
        "published_at": "2026-08-10",
        "video_url": "https://www.youtube.com/watch?v=MgfFrw0E7Q0",
        "thumbnail_url": "https://img.youtube.com/vi/MgfFrw0E7Q0/hqdefault.jpg",
        "view_count": 480000,
        "duration_sec": 2900,
        "period_label": "2026-08",
        "sentiment_label": "neutral",
        "sentiment_score": 0.05,
        "summary_text": "서울 아파트 입주 물량 급감으로 전세 매물 부족이 심화되며 신축 대단지 아파트의 전세가 상승세가 매매 가격의 하방 안전판 역할을 하고 있습니다.",
        "opinion": {
            "topic": "부동산",
            "stance": "Neutral",
            "core_argument": "대출 규제로 폭발적 상승은 제약되나, 입주 절벽에 따른 전세가 상승이 가격 방어막을 형성함.",
            "key_quote": "전세가 오르면 집값은 쉽게 빠지지 않습니다. 2026년 가을 이사철은 공급 부족의 위력을 실감하는 시기가 될 것입니다."
        },
        "transcript_text": """프리즘투자자문 홍춘욱입니다. 8월에 접어들며 서울 주요 학군지와 신축 밀집 지역의 전세 매물이 바닥을 드러내고 있습니다.
금리 인하 기조로 전세대출 이자 부담이 줄어든 반면, 2026년 서울 신규 입주 아파트는 극소수에 불과하기 때문입니다.
스트레스 DSR 규제로 매매 대출은 까다롭지만, 전세가율 상승이 갭을 좁히며 실수요 매수를 뒷받침하고 있습니다."""
    },

    # 29. 오건영 - 2026년 9월 (연준 중립금리 3.25% 안착 선언)
    {
        "video_id": "OGY_2026_09",
        "title": "연준 FOMC 성명서 분석: 중립금리 3.25% 안착 선언과 2027년 전망 (오건영)",
        "channel_title": "신한은행 신한금융그룹",
        "channel_id": "UC_Shinhan",
        "analyst_name": "오건영",
        "category": "거시경제/금리",
        "published_at": "2026-09-18",
        "video_url": "https://www.youtube.com/watch?v=1W3G743ssBw",
        "thumbnail_url": "https://img.youtube.com/vi/1W3G743ssBw/hqdefault.jpg",
        "view_count": 510000,
        "duration_sec": 3150,
        "period_label": "2026-09",
        "sentiment_label": "neutral",
        "sentiment_score": 0.0,
        "summary_text": "9월 FOMC 점도표는 장기 중립금리를 3.0~3.25% 수준으로 확정하며, 무차별적 유동성 완화가 아닌 정밀한 경기 연착륙 관리 체제로의 전환을 공식화했습니다.",
        "opinion": {
            "topic": "금리/통화정책",
            "stance": "Neutral",
            "core_argument": "연준의 금리 인하 사이클이 3%대 초반에서 마무리 수순을 밟고 있으며, 시장은 이제 금리 인하 폭보다는 실물 이익 체력에 집중해야 함.",
            "key_quote": "중립금리 선언은 게임의 규칙이 바뀌었음을 의미합니다. 저금리 착시에서 벗어나 기업의 순현금 체력을 보아야 합니다."
        },
        "transcript_text": """신한은행 오건영입니다. 2026년 9월 FOMC 회의는 연준의 통화정책사에서 중요한 마침표를 찍었습니다.
파월 의장은 기자회견에서 현재의 정책금리가 완전고용과 물가안정을 동시에 달성할 수 있는 '중립 영역'에 도달했다고 공식 선언했습니다.
이는 2024년 가을의 50bp 빅컷으로 시작된 완화 사이클이 사실상 정상화 국면에 안착했음을 뜻합니다.
더 이상의 공격적 인하는 없으며, 인플레이션의 돌발 반등 가능성에 대비해 장기 금리는 일정 수준의 프리미엄을 유지할 것입니다."""
    },

    # 30. 염승환 - 2026년 9월 (피지컬 AI 로봇 양산과 부품주 실적 폭발)
    {
        "video_id": "YSH_2026_09",
        "title": "테슬라 옵티머스 3세대 공장 실전 배치와 국내 로봇 액추에이터 기업 실적 급증 (염승환)",
        "channel_title": "김작가 TV",
        "channel_id": "UC_KimAuthor",
        "analyst_name": "염승환",
        "category": "국내주식",
        "published_at": "2026-09-25",
        "video_url": "https://www.youtube.com/watch?v=9iDF7PdaTIo",
        "thumbnail_url": "https://img.youtube.com/vi/9iDF7PdaTIo/hqdefault.jpg",
        "view_count": 630000,
        "duration_sec": 3400,
        "period_label": "2026-09",
        "sentiment_label": "bullish",
        "sentiment_score": 0.85,
        "summary_text": "글로벌 완성차 및 테크 제조 공장에 수천 대 규모의 휴머노이드 로봇이 실전 투입되면서, 감속기와 서보모터 등 정밀 구동계 부품을 납품하는 국내 로봇 기업들의 실적이 퀀텀 점프하고 있습니다.",
        "opinion": {
            "topic": "AI/로봇",
            "stance": "Bullish",
            "core_argument": "소프트웨어 AI를 넘어 물리적 세계에서 작업을 수행하는 피지컬 AI 하드웨어 양산 사이클이 본격 개막됨.",
            "key_quote": "로봇이 실제로 물건을 조립하고 돈을 벌어다 주는 시대가 열렸습니다. K-부품 밸류체인의 재평가가 시작됩니다."
        },
        "transcript_text": """염블리 염승환입니다. 2026년 9월 주식시장의 핵심 화두는 피지컬 AI(Physical AI)입니다.
미국과 한국의 스마트 팩토리에 휴머노이드 로봇이 본격 도입되면서 부품 쇼티지가 나타나고 있습니다.
로봇 한 대당 수십 개가 들어가는 정밀 감속기와 고출력 토크 모터 분야에서 한국 기업들의 수주가 쇄도하고 있습니다.
2024년의 엔비디아 GPU 랠리를 놓치셨다면, 2026년 가을부터 시작되는 로봇 하드웨어 실적 랠리를 반드시 주목하셔야 합니다."""
    },

    # 31. 김일구 - 2026년 9월 (금 2,900달러 돌파와 미 국채 10년물 금리의 버티기)
    {
        "video_id": "KIK_2026_09",
        "title": "금 2,900달러 돌파 직전, 미 국채 10년물 금리의 버티기와 인플레 2차 파동 (김일구)",
        "channel_title": "삼프로TV",
        "channel_id": "UC_3proTV",
        "analyst_name": "김일구",
        "category": "환율/원자재",
        "published_at": "2026-09-22",
        "video_url": "https://www.youtube.com/watch?v=Cv0W18k4jzk",
        "thumbnail_url": "https://img.youtube.com/vi/Cv0W18k4jzk/hqdefault.jpg",
        "view_count": 470000,
        "duration_sec": 3050,
        "period_label": "2026-09",
        "sentiment_label": "caution",
        "sentiment_score": -0.2,
        "summary_text": "기준금리 인하에도 불구하고 미 10년물 국채 금리가 4%선 아래로 쉽게 내려오지 않는 것은 미국의 재정적자와 금(Gold) 랠리가 가리키는 화폐 신뢰도 저하 때문입니다.",
        "opinion": {
            "topic": "채권/금",
            "stance": "Caution",
            "core_argument": "채권 금리의 기간 프리미엄 상승과 안전자산으로서의 금 매집 경쟁은 통화 시스템의 구조적 균열을 반영함.",
            "key_quote": "중앙은행들이 금을 살 때 개인 투자자들은 그 경고를 결코 무시해선 안 됩니다."
        },
        "transcript_text": """한화투자증권 김일구입니다. 9월 금리가 내려갔음에도 장기 국채 금리는 여전히 끈적하게 버티고 있습니다.
왜 그럴까요? 매달 수천억 달러씩 쏟아져 나오는 미국 국채를 받아줄 해외 투자자가 부족하기 때문입니다.
대신 전 세계 큰손들은 달러 채권 대신 금으로 피신하고 있습니다.
금값이 온스당 2,900달러를 돌파하며 3,000달러를 목전에 둔 것은 바로 이 실질 금리의 왜곡을 헤지하기 위함입니다."""
    },

    # 32. 이선엽 - 2026년 9월 (빅테크-원전 PPA 체결과 SMR 수주 잭팟)
    {
        "video_id": "LSY_2026_09",
        "title": "빅테크-원전 PPA 체결 릴레이와 한국 SMR 기업들의 수주 잭팟 (이선엽)",
        "channel_title": "815머니톡",
        "channel_id": "UC_815Money",
        "analyst_name": "이선엽",
        "category": "미국주식/글로벌",
        "published_at": "2026-09-28",
        "video_url": "https://www.youtube.com/watch?v=HEKkMZD0aYU",
        "thumbnail_url": "https://img.youtube.com/vi/HEKkMZD0aYU/hqdefault.jpg",
        "view_count": 590000,
        "duration_sec": 3150,
        "period_label": "2026-09",
        "sentiment_label": "bullish",
        "sentiment_score": 0.8,
        "summary_text": "빅테크 기업들이 AI 데이터센터 전력 공급을 위해 차세대 원자로 제조사들과 대규모 장기 계약을 연이어 발표하며, 한국 SMR 공급망의 실적 성장성이 증명되고 있습니다.",
        "opinion": {
            "topic": "AI/에너지",
            "stance": "Bullish",
            "core_argument": "전력 쇼티지 해결의 유일한 해법인 원자력 및 SMR 주기기 공급사들의 수주 잔고가 사상 최대를 경신 중.",
            "key_quote": "AI 시대의 진짜 금맥은 데이터센터의 콘센트를 책임지는 전력 인프라와 원자력 발전입니다."
        },
        "transcript_text": """신한투자증권 이선엽입니다. 9월 말 구글과 아마존이 잇달아 소형모듈원전(SMR) 개발사들과 수 기가와트 규모의 전력구매계약을 체결했습니다.
AI 모델의 추론 연산이 일상화되면서 데이터센터 전력망은 포화 상태에 이르렀습니다.
탄소 배출이 없으면서도 24시간 풀가동할 수 있는 발전원은 원전뿐입니다. 한국 기업들의 제작 기술력과 공기 준수 역량은 세계 최고 수준이므로 장기 구조적 성장을 누릴 것입니다."""
    }
]


