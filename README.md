# HPT Trading System

HPT 알고리즘 기반 주식 초단타 자동거래 시스템

## 개요

한국투자증권 KIS API를 활용한 자동거래 시스템으로, 스캘핑, 기술적 지표, 머신러닝을 결합한 복합 전략을 구현합니다.

## 주요 기능

- **실시간 데이터 수집**: WebSocket을 통한 실시간 시세/호가/체결 데이터 수집
- **백테스팅**: 과거 데이터를 활용한 전략 검증
- **리스크 관리**: 손절/익절, 포지션 관리, 일일 손실 제한
- **자동거래**: 전략 기반 자동 주문 실행
- **모니터링**: 실시간 거래 현황 추적

## 기술 스택

- **Python**: 3.11+
- **패키지 관리**: uv
- **데이터베이스**: SQLite
- **API**: 한국투자증권 KIS REST API & WebSocket

## 프로젝트 구조

```
hpt-trading/
├── src/
│   ├── api/          # KIS API 클라이언트
│   ├── data/         # 데이터 수집 및 저장
│   ├── strategy/     # 트레이딩 전략
│   ├── backtest/     # 백테스팅 엔진
│   ├── risk/         # 리스크 관리
│   └── utils/        # 유틸리티
├── tests/            # 테스트
├── config/           # 설정 파일
├── data/             # 데이터베이스
└── logs/             # 로그 파일
```

## 설치 및 실행

### 1. 프로젝트 클론

```bash
git clone <repository-url>
cd hpt-trading
```

### 2. 가상환경 생성 및 의존성 설치

```bash
# 가상환경 생성
uv venv

# 가상환경 활성화
source .venv/bin/activate  # Mac/Linux

# 의존성 설치
uv pip install -e .

# 개발 의존성 포함 설치
uv pip install -e ".[dev]"
```

### 3. 환경변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집하여 KIS API 인증 정보 입력
# KIS_APP_KEY, KIS_APP_SECRET, KIS_ACCOUNT_NO 등
```

### 4. KIS API 키 발급

1. [한국투자증권 API 포털](https://apiportal.koreainvestment.com) 접속
2. 회원가입 및 로그인
3. API 서비스 신청
4. 앱 키(App Key) 및 앱 시크릿(App Secret) 발급
5. `.env` 파일에 입력

## 사용법

### 실시간 데이터 수집 (예정)

```python
from src.data.collector import DataCollector

# 삼성전자 실시간 시세 수집
collector = DataCollector(['005930'])
collector.start()
```

### 백테스팅 실행 (예정)

```python
from src.backtest.engine import BacktestEngine

engine = BacktestEngine()
results = engine.run(strategy, start_date, end_date)
```

## 개발 로드맵

### Phase 1: 기본 인프라 (진행 중)
- [x] 프로젝트 초기 설정
- [ ] KIS API 연동
- [ ] 실시간 데이터 수집
- [ ] SQLite 저장소 구현

### Phase 2: 전략 및 백테스팅
- [ ] 전략 프레임워크
- [ ] 백테스팅 엔진
- [ ] 리스크 관리

### Phase 3: 자동거래
- [ ] 주문 실행 시스템
- [ ] 포지션 관리
- [ ] 실시간 모니터링

### Phase 4: 고급 기능
- [ ] 스캘핑 전략
- [ ] 기술적 지표 전략
- [ ] 머신러닝 전략
- [ ] 대시보드

## 주의사항

- **모의투자 환경에서 먼저 테스트**: 실전투자 전 반드시 모의투자 환경에서 충분히 테스트하세요
- **API 호출 제한**: KIS API는 초당 20회 호출 제한이 있습니다
- **리스크 관리**: 적절한 손절/익절 설정으로 리스크를 관리하세요
- **민감정보 보호**: `.env` 파일을 절대 커밋하지 마세요

## 법적 고지

이 프로젝트는 교육 및 연구 목적으로 제작되었습니다. 실제 투자에 사용 시 발생하는 손실에 대해 개발자는 책임지지 않습니다. 투자는 본인의 판단과 책임하에 진행하세요.

## 라이센스

MIT License
