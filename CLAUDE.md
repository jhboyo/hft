# HFT Trading System - Claude Assistant Guide

## 프로젝트 개요

**HFT 알고리즘 기반 주식 초단타 자동거래 시스템**

이 프로젝트는 한국투자증권 KIS API를 활용한 자동거래 시스템입니다. 스캘핑, 기술적 지표, 머신러닝을 결합한 복합 전략을 구현하며, 실시간 데이터 수집, 백테스팅, 리스크 관리 기능을 제공합니다.

### 핵심 기술 스택
- **언어**: Python 3.11+
- **패키지 관리**: uv (editable mode 사용)
- **API**: 한국투자증권 KIS REST API & WebSocket
- **데이터베이스**: SQLite
- **주요 라이브러리**: requests, websocket-client, pandas, pydantic

### 환경
- **개발 환경**: Mac/Linux (크로스 플랫폼)
- **API 환경**: 모의투자(virtual) / 실전투자(real)

---

## 프로젝트 구조

hft/
├── src/                        # 소스 코드 (editable mode로 설치됨)
│   ├── api/                    # KIS API 클라이언트
│   │   ├── __init__.py
│   │   ├── auth.py            # OAuth 2.0 인증
│   │   ├── kis_api.py         # REST API 클라이언트 (예정)
│   │   └── websocket_client.py # WebSocket 클라이언트 (예정)
│   ├── data/                   # 데이터 수집 및 관리
│   │   ├── __init__.py
│   │   ├── models.py          # Pydantic 데이터 모델 (예정)
│   │   ├── storage.py         # SQLite 저장소 (예정)
│   │   └── collector.py       # 실시간 데이터 수집기 (예정)
│   └── utils/                  # 유틸리티
│       ├── __init__.py
│       ├── logger.py          # 로깅 시스템
│       └── helpers.py         # 공통 함수 (예정)
├── tests/                      # 테스트 코드
│   ├── test_api/
│   └── test_data/
├── config/                     # 설정 파일
│   └── config.yaml            # 시스템 설정
├── data/                       # 데이터 저장소 (SQLite DB)
├── logs/                       # 로그 파일
├── .venv/                      # uv 가상환경 (Git 제외)
├── .env                        # 환경변수 (Git 제외)
├── .env.example               # 환경변수 템플릿
├── .gitignore
├── pyproject.toml             # uv 프로젝트 설정
├── README.md                  # 프로젝트 설명
└── CLAUDE.md                  # 이 파일
```

---

## 개발 원칙 및 가이드라인

### 1. 코드 작성 원칙

#### **최소주의 원칙**
- ✅ **요청된 것만 구현**: "Do what has been asked; nothing more, nothing less"
- ❌ 요청되지 않은 기능, 리팩토링, 최적화 금지
- ❌ 문서화 파일(*.md, README 등) 자동 생성 금지
- ✅ 기존 파일 편집 우선, 새 파일 생성 최소화

#### **주석 작성**
- ✅ 모든 모듈에 docstring 작성
- ✅ 클래스/함수에 상세한 docstring (Args, Returns, Raises, Example)
- ✅ 핵심 로직마다 인라인 주석 (`# 설명`) 추가
- ✅ 복잡한 알고리즘은 단계별 주석 작성
- ❌ 자명한 코드에 불필요한 주석 금지

#### **에러 처리**
- ✅ 모든 외부 API 호출에 try-except 사용
- ✅ 명확한 에러 메시지와 로깅
- ✅ 적절한 예외 타입 사용 (ValueError, HTTPError 등)
- ✅ 네트워크 오류 시 재시도 로직 구현

### 2. 코딩 컨벤션

#### **명명 규칙**
- **파일명**: `snake_case.py` (예: `kis_api.py`, `data_collector.py`)
- **클래스명**: `PascalCase` (예: `KISAuth`, `DataCollector`)
- **함수/변수명**: `snake_case` (예: `get_access_token`, `stock_code`)
- **상수**: `UPPER_SNAKE_CASE` (예: `BASE_URL`, `MAX_RETRIES`)
- **Private 멤버**: `_leading_underscore` (예: `_access_token`)

#### **Import 순서**
```python
# 1. 표준 라이브러리
import os
from datetime import datetime
from typing import Optional

# 2. 서드파티 라이브러리
import requests
from pydantic import BaseModel

# 3. 로컬 모듈
from src.utils.logger import get_logger
```

#### **타입 힌팅**
```python
# 모든 함수 시그니처에 타입 힌트 사용
def get_access_token(self, force_refresh: bool = False) -> str:
    pass

# Optional 사용
from typing import Optional
def process_data(data: Optional[dict] = None) -> list:
    pass
```

### 3. 로깅 사용법

```python
from src.utils.logger import get_logger

# 모듈 레벨에서 로거 생성
logger = get_logger(__name__)

# 로그 레벨별 사용
logger.debug("디버깅 정보 (개발 중)")
logger.info("일반 정보 (운영)")
logger.warning("경고 (문제 가능성)")
logger.error("에러 발생", exc_info=True)  # 스택 트레이스 포함
logger.critical("치명적 오류")
```

### 4. 환경변수 사용

```python
import os
from dotenv import load_dotenv

# .env 파일 로드 (모듈 최상단)
load_dotenv()

# 환경변수 읽기
app_key = os.getenv("KIS_APP_KEY")
env = os.getenv("KIS_ENV", "virtual")  # 기본값 지정
```

### 5. 설정 파일 사용

```python
import yaml

# config.yaml 읽기
with open("config/config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
    log_level = config.get("logging", {}).get("level", "INFO")
```

---

## 아키텍처 및 설계 원칙

### 1. 모듈 분리

- **api/**: 외부 API 연동만 담당 (비즈니스 로직 포함 금지)
- **data/**: 데이터 수집, 저장, 조회만 담당
- **strategy/**: 트레이딩 전략 로직 (예정)
- **risk/**: 리스크 관리 로직 (예정)
- **utils/**: 공통 유틸리티 (로깅, 헬퍼 함수)

### 2. 인증 처리

```python
# 싱글톤 패턴 사용
from src.api.auth import get_auth

# 전역 인증 객체 (프로그램 전체에서 공유)
auth = get_auth()
headers = auth.get_auth_headers()

# 또는 독립 인스턴스
from src.api.auth import KISAuth
auth = KISAuth(env="virtual")
```

### 3. 데이터 모델

```python
# Pydantic 사용 (예정)
from pydantic import BaseModel
from datetime import datetime

class TickData(BaseModel):
    timestamp: datetime
    stock_code: str
    price: int
    volume: int
```

### 4. 에러 처리 패턴

```python
# KIS API 호출 표준 패턴
try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # HTTP 에러 체크

    data = response.json()

    # KIS API 응답 코드 체크
    if data.get("rt_cd") != "0":
        error_msg = data.get("msg1", "Unknown error")
        logger.error(f"API error: {error_msg}")
        raise requests.HTTPError(f"API failed: {error_msg}")

    return data

except requests.exceptions.Timeout:
    logger.error("Request timeout")
    raise
except requests.exceptions.RequestException as e:
    logger.error(f"Request failed: {e}")
    raise
```

---

## 개발 워크플로우

### 1. 새로운 기능 추가

```bash
# 1. 의존성 확인 및 설치
source .venv/bin/activate
uv pip install -e .

# 2. 코드 작성 (editable mode라 즉시 반영)
# src/api/new_feature.py 작성

# 3. 수동 테스트
python -c "from src.api.new_feature import ..."

# 4. 커밋 (사용자 요청 시에만)
# git add, git commit
```

### 2. 환경 설정

```bash
# .env 파일 생성 (최초 1회)
cp .env.example .env
# .env 파일 편집 (API 키 입력)

# 가상환경 활성화
source .venv/bin/activate

# 의존성 설치
uv pip install -e .
```

### 3. 로그 확인

```bash
# 실시간 로그 모니터링
tail -f logs/trading.log

# 최근 로그 확인
tail -n 100 logs/trading.log
```

---

## KIS API 특성 및 제약사항

### 1. API 호출 제한
- **REST API**: 초당 20회 제한
- **WebSocket**: 별도 제한 없음 (연결당)
- ⚠️ Rate Limiting 구현 필수

### 2. 인증
- **방식**: OAuth 2.0 Client Credentials
- **토큰 유효기간**: 24시간 (86400초)
- **자동 갱신**: 만료 60초 전 갱신 권장

### 3. 응답 코드
```python
# 모든 KIS API 응답에 공통 포함
{
    "rt_cd": "0",       # "0": 성공, 그 외: 실패
    "msg_cd": "...",    # 메시지 코드
    "msg1": "...",      # 에러 메시지
    # ... 실제 데이터
}
```

### 4. 환경 분리
- **모의투자(virtual)**: 테스트 환경, 실제 거래 없음
- **실전투자(real)**: 실제 거래, 실제 돈 사용
- ⚠️ 개발 중에는 반드시 `KIS_ENV=virtual` 사용

---

## 보안 및 주의사항

### 1. 민감정보 보호
```bash
# 절대 커밋 금지
.env                    # API 키, 시크릿
*.log                   # 로그 파일 (개인정보 포함 가능)
data/*.db               # 데이터베이스 (거래 내역)

# .gitignore에 포함 확인
```

### 2. API 키 관리
- ✅ 환경변수로만 관리 (.env)
- ❌ 코드에 하드코딩 절대 금지
- ❌ 로그에 API 키 출력 금지

### 3. 리스크 관리
- ✅ 모의투자에서 충분히 테스트
- ✅ 손절/익절 로직 반드시 구현
- ✅ 일일 최대 손실 제한 설정
- ⚠️ 실전투자 전 사용자 확인 필수

---

## 테스트 가이드라인

### 1. 테스트 작성 (예정)

```python
# tests/test_api/test_auth.py
import pytest
from src.api.auth import KISAuth

def test_auth_initialization():
    auth = KISAuth(
        app_key="test_key",
        app_secret="test_secret",
        env="virtual"
    )
    assert auth.env == "virtual"

def test_token_request():
    # 실제 API 호출은 모킹 필요
    pass
```

### 2. 수동 테스트

```python
# 인증 테스트
python -c "
from src.api.auth import KISAuth
auth = KISAuth()
token = auth.get_access_token()
print(f'Token: {token[:20]}...')
"
```

---

## 문제 해결 가이드

### 1. 일반적인 오류

#### `ImportError: No module named 'src'`
```bash
# editable mode로 재설치
source .venv/bin/activate
uv pip install -e .
```

#### `ValueError: KIS_APP_KEY must be provided`
```bash
# .env 파일 확인
cat .env  # KIS_APP_KEY 값 확인
# .env 파일이 프로젝트 루트에 있는지 확인
```

#### `yaml 모듈 import 오류`
```bash
# PyYAML 설치 확인
uv pip install PyYAML
```

### 2. API 오류

#### 401 Unauthorized
- API 키/시크릿 확인
- 환경(real/virtual) 확인
- 토큰 만료 여부 확인

#### 429 Too Many Requests
- Rate Limiting 초과
- 초당 20회 제한 준수

---

## Claude가 코드 작성 시 체크리스트

작업 전 반드시 확인:

- [ ] 사용자가 **정확히 요청한 것**만 구현하는가?
- [ ] 요청되지 않은 **추가 기능/리팩토링**을 하지 않는가?
- [ ] **기존 파일 편집**을 우선하고, 새 파일은 꼭 필요할 때만 생성하는가?
- [ ] **상세한 주석**을 모든 코드에 추가했는가?
- [ ] **docstring**을 모든 함수/클래스에 작성했는가?
- [ ] **타입 힌트**를 모든 함수 시그니처에 추가했는가?
- [ ] **에러 처리**를 적절히 구현했는가?
- [ ] **로깅**을 주요 지점에 추가했는가?
- [ ] **환경변수**를 하드코딩하지 않고 사용했는가?
- [ ] **.gitignore**에 민감정보가 제외되어 있는가?
- [ ] **모의투자 환경**을 기본으로 설정했는가?

---

## 추가 리소스

- **KIS API 문서**: https://apiportal.koreainvestment.com
- **프로젝트 계획**: `/Users/joonho/.claude/plans/eager-beaming-widget.md`
- **README**: `README.md` - 사용자용 프로젝트 설명
- **설정 예시**: `.env.example`, `config/config.yaml`

---

## 현재 구현 상태 (2025-12-30)

### ✅ 완료
- uv 프로젝트 초기화
- 기본 디렉토리 구조
- 로깅 시스템 (`src/utils/logger.py`)
- KIS API 인증 (`src/api/auth.py`)
- 설정 파일 (`config/config.yaml`, `.env.example`)
- 코드 주석 보강

### 🚧 진행 예정
- REST API 클라이언트 (`src/api/kis_api.py`)
- WebSocket 클라이언트 (`src/api/websocket_client.py`)
- 데이터 모델 (`src/data/models.py`)
- SQLite 저장소 (`src/data/storage.py`)
- 데이터 수집기 (`src/data/collector.py`)
- 전략 프레임워크
- 백테스팅 엔진
- 자동거래 실행기

---

**Last Updated**: 2025-12-30
**Project Phase**: Phase 1 - 기본 인프라 구축 중
