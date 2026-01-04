# HFT Stock Web Application

모바일 최적화 주식 시세 조회 웹 애플리케이션

## 개요

한국투자증권 KIS API 기반 **실시간 주식 시세 조회 웹 서비스**입니다.
**모바일 브라우저 환경에 최적화**된 웹 애플리케이션으로, PC에서도 사용 가능합니다.

### 📱 주요 특징
- **모바일 우선 설계**: 모바일 브라우저에서 최적의 사용자 경험 제공
- **웹 기반**: 별도 앱 설치 없이 모바일 브라우저에서 즉시 실행
- **터치 최적화**: 스와이프, 탭, 드래그 등 모바일 제스처 지원
- **반응형 디자인**: 모바일, 태블릿, PC 모든 화면 크기 대응
- **PWA 지원**: 모바일 홈 화면에 추가하여 앱처럼 사용 가능
- **실시간 시세**: WebSocket 기반 실시간 데이터 업데이트
- **경량 설계**: 모바일 데이터 절약 및 빠른 로딩 속도

### 📊 제공 데이터
- **유가증권(KOSPI), KOSDAQ** 실시간 시세 조회
- **주요 지표** 모니터링 (금, 비트코인, 나스닥, 야간선물)
- **실시간 호가** 및 **체결 내역**
- **차트 및 기술적 지표**

### 🔗 연관 프로젝트
- **Backend (별도 프로젝트)**: Spring Boot 기반 WebSocket 서버
  - KIS API 연동
  - 실시간 데이터 수집 및 배포
  - REST API 제공

## 주요 기능

### 📊 실시간 시세
- **KOSPI/KOSDAQ** 전 종목 실시간 시세 조회
- **현재가, 등락률, 거래량** 실시간 업데이트
- **10호가** 실시간 호가창 제공
- **실시간 체결** 내역 조회

### 🔍 종목 검색 및 관리
- **통합 검색**: 종목명, 종목코드 기반 빠른 검색
- **관심 종목**: 즐겨찾기 등록 및 관리
- **가격 알림**: 목표가 도달 시 알림 (PWA 푸시)

### 📈 차트 및 분석
- **멀티 타임프레임**: 분봉, 일봉, 주봉, 월봉
- **기술적 지표**: 이동평균선, 볼린저밴드, RSI, MACD
- **터치 인터랙션**: 확대/축소, 스크롤, 핀치 제스처

### 📰 정보 제공
- **주요 지표 대시보드**: 금, 비트코인, 나스닥, 야간선물
- **뉴스/공시**: 종목별 실시간 뉴스 및 공시 정보
- **VI 알림**: 변동성완화장치(VI) 발동 실시간 알림
- **시장 시간**: 개장/폐장, 동시호가 시간 표시

## 기술 스택

### 📱 Frontend (Mobile-First Web Application)
- **프레임워크**: React / Next.js (선택 예정)
- **언어**: TypeScript
- **상태 관리**: Redux Toolkit / Zustand
- **UI 라이브러리**:
  - Tailwind CSS (모바일 우선 반응형 스타일링)
  - shadcn/ui (터치 최적화 컴포넌트)
  - Framer Motion (부드러운 모바일 애니메이션)
- **차트**: Lightweight Charts (모바일 터치 제스처 지원)
- **WebSocket**: Socket.IO Client / Native WebSocket API
- **PWA**: Workbox, Service Worker (오프라인 지원, 홈 화면 추가)
- **모바일 최적화**:
  - React Virtual (가상 스크롤 - 성능 최적화)
  - React Spring (터치 인터랙션)
  - Web Vitals (성능 모니터링)
- **빌드 도구**: Vite (빠른 HMR, 최적화된 번들링)
- **배포**: Vercel / Netlify / AWS S3 + CloudFront

### 🔗 Backend (별도 Spring Boot 프로젝트)
- **프레임워크**: Spring Boot 3.x
- **언어**: Java 17+
- **WebSocket**: Spring WebSocket (STOMP)
- **API**: 한국투자증권 KIS REST API & WebSocket
- **데이터베이스**: PostgreSQL / MySQL
- **캐시**: Redis
- **메시징**: Kafka / RabbitMQ (예정)

## 프로젝트 구조

```
hft-web/
├── public/                   # 정적 파일
│   ├── icons/               # PWA 아이콘
│   ├── manifest.json        # PWA 매니페스트
│   └── sw.js                # Service Worker
│
├── src/
│   ├── app/                 # Next.js App Router (선택 시)
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── ...
│   │
│   ├── pages/               # React Router (선택 시)
│   │   ├── Home/            # 홈 화면 (주요 지표, 모바일 대시보드)
│   │   ├── Market/          # 시장 현황 (KOSPI/KOSDAQ, 터치 최적화)
│   │   ├── Stock/           # 종목 상세 (시세/호가/체결, 차트)
│   │   ├── Watchlist/       # 관심 종목 (스와이프 액션)
│   │   └── News/            # 뉴스/공시 (카드 레이아웃)
│   │
│   ├── components/          # 재사용 컴포넌트
│   │   ├── common/          # 공통 컴포넌트 (터치 최적화 Button, Input 등)
│   │   ├── chart/           # 차트 컴포넌트 (터치 제스처 지원)
│   │   ├── stock/           # 주식 관련 컴포넌트 (호가창, 체결 리스트)
│   │   ├── mobile/          # 모바일 전용 컴포넌트 (BottomSheet, PullToRefresh)
│   │   └── layout/          # 레이아웃 컴포넌트 (하단 네비게이션 등)
│   │
│   ├── services/            # API 서비스
│   │   ├── api.ts           # Axios 인스턴스
│   │   ├── websocket.ts     # WebSocket 클라이언트
│   │   ├── stockService.ts  # 종목 API
│   │   └── marketService.ts # 시장 데이터 API
│   │
│   ├── store/               # 상태 관리
│   │   ├── slices/          # Redux slices (또는 Zustand stores)
│   │   │   ├── stockSlice.ts
│   │   │   ├── marketSlice.ts
│   │   │   └── userSlice.ts
│   │   └── index.ts
│   │
│   ├── hooks/               # Custom Hooks
│   │   ├── useWebSocket.ts
│   │   ├── useStock.ts
│   │   └── useMarket.ts
│   │
│   ├── types/               # TypeScript 타입 정의
│   │   ├── stock.ts
│   │   ├── market.ts
│   │   └── api.ts
│   │
│   ├── utils/               # 유틸리티 함수
│   │   ├── format.ts        # 숫자 포맷팅
│   │   ├── date.ts          # 날짜 처리
│   │   └── storage.ts       # 로컬 스토리지
│   │
│   └── styles/              # 스타일
│       ├── globals.css
│       └── tailwind.css
│
├── docs/                     # 문서
│   ├── krx.md               # KRX 시장 구조
│   ├── vi.md                # 변동성완화장치(VI)
│   └── api.md               # API 명세서 (예정)
│
├── .env.example             # 환경변수 예시
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── vite.config.ts (또는 next.config.js)
```

## 설치 및 실행

### 1. 프로젝트 클론

```bash
git clone <repository-url>
cd hft-web
```

### 2. 의존성 설치

```bash
# npm 사용
npm install

# 또는 yarn 사용
yarn install

# 또는 pnpm 사용
pnpm install
```

### 3. 환경변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집
# VITE_API_URL=http://localhost:8080  (백엔드 서버 URL)
# VITE_WS_URL=ws://localhost:8080/ws  (WebSocket 서버 URL)
```

### 4. 개발 서버 실행

```bash
# Vite 사용 시
npm run dev

# Next.js 사용 시
npm run dev

# 브라우저에서 http://localhost:3000 접속
```

### 5. 프로덕션 빌드

```bash
# 빌드
npm run build

# 빌드 파일 미리보기
npm run preview
```

## 백엔드 서버 연동

이 프로젝트는 **별도의 Spring Boot 백엔드 서버**가 필요합니다.

### 백엔드 서버 요구사항
- Spring Boot 3.x
- WebSocket (STOMP) 지원
- 다음 API 엔드포인트 제공:
  - `/api/market/kospi` - KOSPI 지수 조회
  - `/api/market/kosdaq` - KOSDAQ 지수 조회
  - `/api/stock/{code}` - 종목 시세 조회
  - `/api/stock/{code}/orderbook` - 호가 조회
  - `/ws/stock` - 실시간 시세 WebSocket

### 로컬 개발 환경 설정
1. 백엔드 서버를 `http://localhost:8080`에서 실행
2. `.env` 파일의 `VITE_API_URL` 설정 확인
3. 프론트엔드 개발 서버 실행

## 개발 로드맵

### Phase 1: 프로젝트 초기 설정 🚀
- [ ] **프레임워크 선택** (React + Vite / Next.js)
- [ ] **프로젝트 초기 설정**
  - [ ] TypeScript 설정
  - [ ] Tailwind CSS 설정 (모바일 우선 브레이크포인트)
  - [ ] ESLint/Prettier 설정
  - [ ] 상태 관리 라이브러리 설정 (Redux Toolkit / Zustand)
- [ ] **모바일 우선 디자인 시스템**
  - [ ] 컬러 팔레트 정의 (다크 모드 지원)
  - [ ] 타이포그래피 (모바일 가독성)
  - [ ] 터치 친화적 공통 컴포넌트 (Button, Input, Card)
  - [ ] 모바일 레이아웃 컴포넌트 (하단 네비게이션, 헤더)
  - [ ] 터치 영역 최소 크기 설정 (44x44px)
- [ ] **라우팅 설정**
  - [ ] 페이지 전환 애니메이션
  - [ ] 스와이프 백 제스처
- [ ] **API 클라이언트 구축**
  - [ ] Axios 인스턴스 (Timeout, Retry 설정)
  - [ ] 로딩 상태 관리
  - [ ] 에러 핸들링
- [ ] **WebSocket 클라이언트 구축**
  - [ ] 자동 재연결
  - [ ] 연결 상태 모니터링

### Phase 2: 핵심 화면 구현 (모바일 우선) 📱
- [ ] **홈 화면**
  - [ ] 주요 지표 대시보드 (금, 비트코인, 나스닥, 야간선물)
  - [ ] KOSPI/KOSDAQ 지수 표시
  - [ ] 시장 시간 표시
  - [ ] 거래량/등락률 상위 종목 (스와이프 가능한 카드 형식)
  - [ ] Pull-to-Refresh (당겨서 새로고침)
- [ ] **시장 현황 화면**
  - [ ] KOSPI/KOSDAQ 탭 (터치 최적화)
  - [ ] 종목 리스트 (무한 스크롤 + 가상 스크롤)
  - [ ] 정렬 기능 (하단 시트 UI)
  - [ ] 빠른 스크롤 인디케이터
- [ ] **종목 상세 화면**
  - [ ] 종목 정보 (현재가, 등락률, 거래량 등)
  - [ ] 10호가 실시간 표시 (모바일 레이아웃)
  - [ ] 체결 내역 (실시간 애니메이션)
  - [ ] 기본 차트 (핀치 줌, 스와이프 지원)

### Phase 3: 실시간 데이터 연동 ⚡
- [ ] WebSocket 연결 관리
- [ ] 실시간 시세 구독/해제
- [ ] 실시간 호가 업데이트
- [ ] 데이터 캐싱 전략

### Phase 4: 고급 기능 📊
- [ ] **관심 종목 관리**
  - [ ] 스와이프로 추가/삭제
  - [ ] 드래그 앤 드롭으로 순서 변경
  - [ ] 가격 알림 설정 (모바일 친화적 UI)
- [ ] **고급 차트**
  - [ ] Lightweight Charts (터치 제스처 최적화)
  - [ ] 멀티 터치 줌/팬
  - [ ] 차트 타입 전환 (하단 시트)
- [ ] **기술적 지표**
  - [ ] MA, BB, RSI, MACD
  - [ ] 지표 on/off 토글 (모바일 UI)
- [ ] **검색 기능**
  - [ ] 자동완성 (모바일 키보드 최적화)
  - [ ] 최근 검색 (스와이프로 삭제)
- [ ] **뉴스/공시**
  - [ ] 카드 형식 레이아웃
  - [ ] 무한 스크롤

### Phase 5: 모바일 최적화 및 PWA 🔧
- [ ] **PWA 설정**
  - [ ] Service Worker 구현
  - [ ] 오프라인 지원 (캐시 전략)
  - [ ] 홈 화면 추가 배너 (iOS/Android)
  - [ ] 앱 아이콘 및 Manifest 설정
  - [ ] 스플래시 스크린
- [ ] **모바일 성능 최적화**
  - [ ] Code Splitting (라우트별)
  - [ ] Lazy Loading (이미지, 컴포넌트)
  - [ ] 이미지 WebP 포맷 사용
  - [ ] 번들 사이즈 최적화 (Tree Shaking)
  - [ ] 가상 스크롤 (긴 리스트 성능)
  - [ ] 디바운싱/쓰로틀링 (검색, 스크롤)
- [ ] **모바일 UX 개선**
  - [ ] 햅틱 피드백 (진동)
  - [ ] 스켈레톤 로딩
  - [ ] 부드러운 애니메이션 (60fps)
  - [ ] 터치 영역 최적화 (최소 44x44px)
  - [ ] Safe Area 처리 (노치, 홈 인디케이터)
- [ ] **푸시 알림** (FCM)
  - [ ] VI 발동 알림
  - [ ] 가격 알림
  - [ ] 뉴스 알림
  - [ ] 알림 권한 요청 UI
- [ ] **반응형 UI**
  - [ ] 모바일 레이아웃 (320px ~ 480px)
  - [ ] 태블릿 레이아웃 (481px ~ 1024px)
  - [ ] 데스크톱 레이아웃 (1025px ~)
  - [ ] 가로/세로 모드 대응

### Phase 6: 배포 및 운영 🚀
- [ ] **프로덕션 빌드**
  - [ ] 환경별 빌드 설정 (dev, staging, prod)
  - [ ] 최적화 및 압축
- [ ] **배포 환경 설정**
  - [ ] Vercel / Netlify / AWS S3 + CloudFront
  - [ ] 도메인 연결
  - [ ] HTTPS 설정
- [ ] **CI/CD 파이프라인**
  - [ ] GitHub Actions
  - [ ] 자동 테스트
  - [ ] 자동 배포
- [ ] **모니터링 및 분석**
  - [ ] Sentry (에러 트래킹)
  - [ ] Google Analytics (사용자 분석)
  - [ ] 성능 모니터링

## 주의사항

### 🎯 프로젝트 특성
- **모바일 우선**: 이 프로젝트는 **모바일 브라우저에 최적화**된 웹 애플리케이션입니다
- **웹 기반**: 네이티브 앱이 아닌, 브라우저에서 실행되는 웹 서비스입니다
- **PWA**: 모바일 홈 화면에 추가하여 앱처럼 사용할 수 있습니다

### 🔧 기술적 요구사항
- **백엔드 서버 필요**: 별도의 Spring Boot 백엔드 서버가 필요합니다
- **실시간 데이터**: WebSocket 연결을 통해 실시간 시세를 받아옵니다
- **API 호출 제한**: 백엔드 서버에서 KIS API 호출 제한 관리 필요
- **민감정보 보호**: `.env` 파일을 절대 커밋하지 마세요

### 📱 모바일 최적화 권장사항
- **브라우저**: iOS Safari, Android Chrome 최신 버전 권장
- **네트워크**: 4G/5G 또는 Wi-Fi 환경 권장 (3G는 느릴 수 있음)
- **화면 크기**: 최소 320px 이상의 화면 크기
- **터치**: 터치 제스처 지원 기기에서 최적의 경험 제공
- **데이터 절약**: 이미지 압축 및 데이터 캐싱으로 데이터 사용량 최소화

### 🌐 반응형 지원
- **모바일**: 스마트폰 (320px ~ 480px) - **주 타겟**
- **태블릿**: 태블릿 (481px ~ 1024px) - 부가 지원
- **데스크톱**: PC (1025px ~) - 부가 지원

## 법적 고지

이 프로젝트는 교육 및 연구 목적으로 제작되었습니다. 실제 투자에 사용 시 발생하는 손실에 대해 개발자는 책임지지 않습니다. 투자는 본인의 판단과 책임하에 진행하세요.

## 라이센스

MIT License
