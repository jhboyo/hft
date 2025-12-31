"""
한국투자증권 KIS API OAuth 2.0 인증 모듈

이 모듈은 한국투자증권의 REST API 인증을 처리합니다.
- OAuth 2.0 Client Credentials 방식 사용
- 액세스 토큰 자동 발급 및 갱신
- 토큰 유효성 검증 및 재사용
- 실전투자/모의투자 환경 분리

참고: https://apiportal.koreainvestment.com

사용 예시:
    # 기본 사용 (환경변수에서 자동 로드)
    auth = KISAuth()
    headers = auth.get_auth_headers()

    # 또는 직접 인자 전달
    auth = KISAuth(
        app_key="your_app_key",
        app_secret="your_app_secret",
        env="virtual"
    )
"""

import os
from datetime import datetime, timedelta
from typing import Optional

import requests
from dotenv import load_dotenv

from src.utils.logger import get_logger

# .env 파일에서 환경변수 로드
# 프로젝트 루트의 .env 파일을 읽어 KIS_APP_KEY, KIS_APP_SECRET 등을 로드
load_dotenv()

# 모듈 레벨 로거 생성
logger = get_logger(__name__)


class KISAuth:
    """
    한국투자증권 KIS API OAuth 2.0 인증 클래스

    이 클래스는 KIS API 호출에 필요한 액세스 토큰을 관리합니다.
    - 토큰 자동 발급 및 갱신
    - 토큰 만료 시간 추적
    - 실전투자/모의투자 환경별 URL 관리

    Attributes:
        app_key (str): KIS API 앱 키
        app_secret (str): KIS API 앱 시크릿
        env (str): 환경 설정 ('real' 또는 'virtual')
        base_url (str): API 베이스 URL

    Example:
        >>> auth = KISAuth(env="virtual")
        >>> token = auth.get_access_token()
        >>> headers = auth.get_auth_headers()
        >>> # API 요청 시 headers 사용
    """

    # KIS API 베이스 URL
    # real: 실전투자용 (실제 거래)
    # virtual: 모의투자용 (테스트)
    BASE_URL = {
        "real": "https://openapi.koreainvestment.com:9443",
        "virtual": "https://openapivt.koreainvestment.com:29443",
    }

    def __init__(
        self,
        app_key: Optional[str] = None,
        app_secret: Optional[str] = None,
        env: str = "virtual",
    ):
        """
        KIS API 인증 초기화

        Args:
            app_key: KIS 앱 키 (None이면 환경변수 KIS_APP_KEY 사용)
            app_secret: KIS 앱 시크릿 (None이면 환경변수 KIS_APP_SECRET 사용)
            env: 환경 설정 ('real' 또는 'virtual', 기본값: virtual)

        Raises:
            ValueError: app_key 또는 app_secret이 제공되지 않은 경우
        """
        # 앱 키: 인자 우선, 없으면 환경변수에서 로드
        self.app_key = app_key or os.getenv("KIS_APP_KEY")

        # 앱 시크릿: 인자 우선, 없으면 환경변수에서 로드
        self.app_secret = app_secret or os.getenv("KIS_APP_SECRET")

        # 환경: 인자 우선, 없으면 환경변수, 최종 기본값은 "virtual"
        self.env = env or os.getenv("KIS_ENV", "virtual")

        # 필수값 검증: 앱 키와 시크릿은 반드시 필요
        if not self.app_key or not self.app_secret:
            raise ValueError(
                "KIS_APP_KEY and KIS_APP_SECRET must be provided or set in environment"
            )

        # 환경에 따른 API 베이스 URL 설정
        self.base_url = self.BASE_URL[self.env]

        # 액세스 토큰 (처음에는 None, 필요 시 발급)
        self._access_token: Optional[str] = None

        # 토큰 만료 시간 (처음에는 None)
        self._token_expires_at: Optional[datetime] = None

        logger.info(f"KISAuth initialized for {self.env} environment")

    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        액세스 토큰을 반환합니다. 토큰이 없거나 만료되었으면 새로 발급받습니다.

        이 메서드는 토큰의 유효성을 자동으로 확인하고,
        필요한 경우에만 새 토큰을 발급받습니다. (토큰 재사용으로 API 호출 최소화)

        Args:
            force_refresh: True면 기존 토큰 무시하고 강제로 재발급

        Returns:
            액세스 토큰 문자열 (Bearer 토큰으로 사용)

        Raises:
            requests.HTTPError: API 호출 실패
            requests.RequestException: 네트워크 오류 등
        """
        # 기존 토큰이 유효하고 강제 갱신이 아니면 재사용
        # 이렇게 하면 매번 API를 호출하지 않아 효율적
        if not force_refresh and self._is_token_valid():
            logger.debug("Using existing valid access token")
            return self._access_token

        # 토큰이 없거나 만료된 경우 새로 발급
        logger.info("Requesting new access token")
        token_data = self._request_token()

        # 응답에서 액세스 토큰 추출
        self._access_token = token_data["access_token"]

        # 토큰 만료 시간 계산
        # KIS API는 기본적으로 24시간(86400초) 유효
        # 안전하게 60초 마진을 두어, 59분 59초 전에 갱신되도록 함
        expires_in = int(token_data.get("expires_in", 86400))
        self._token_expires_at = datetime.now() + timedelta(
            seconds=expires_in - 60
        )

        logger.info(
            f"Access token obtained, expires at {self._token_expires_at}"
        )

        return self._access_token

    def _request_token(self) -> dict:
        """
        KIS API로부터 액세스 토큰을 요청합니다. (내부 메서드)

        OAuth 2.0 Client Credentials Grant 방식으로 토큰을 발급받습니다.
        KIS API의 /oauth2/tokenP 엔드포인트를 호출합니다.

        Returns:
            토큰 응답 데이터 (dict)
            - access_token: 액세스 토큰
            - expires_in: 유효 기간 (초)
            - rt_cd: 응답 코드 ("0"이 성공)

        Raises:
            requests.HTTPError: API 호출 실패 또는 응답 에러
            requests.RequestException: 네트워크 오류
        """
        # OAuth 2.0 토큰 발급 엔드포인트
        url = f"{self.base_url}/oauth2/tokenP"

        # 요청 헤더
        headers = {"content-type": "application/json"}

        # 요청 본문
        # grant_type: OAuth 2.0 인증 방식 (client_credentials)
        # appkey/appsecret: KIS API 인증 정보
        body = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
        }

        try:
            # POST 요청으로 토큰 발급
            # timeout=10: 10초 이내에 응답 없으면 타임아웃
            response = requests.post(url, headers=headers, json=body, timeout=10)

            # HTTP 상태 코드 확인 (4xx, 5xx이면 예외 발생)
            response.raise_for_status()

            # JSON 응답 파싱
            data = response.json()

            # KIS API 응답 코드 확인
            # rt_cd: "0"이면 성공, 그 외는 실패
            if data.get("rt_cd") != "0":
                error_msg = data.get("msg1", "Unknown error")
                logger.error(f"Token request failed: {error_msg}")
                raise requests.HTTPError(f"Token request failed: {error_msg}")

            return data

        except requests.exceptions.RequestException as e:
            # 네트워크 오류, 타임아웃 등 모든 requests 예외 처리
            logger.error(f"Token request exception: {e}")
            raise

    def _is_token_valid(self) -> bool:
        """
        현재 토큰이 유효한지 확인합니다. (내부 메서드)

        토큰이 존재하고 만료 시간이 아직 남아있는지 확인합니다.

        Returns:
            토큰이 유효하면 True, 그렇지 않으면 False
        """
        # 토큰이나 만료 시간이 없으면 무효
        if not self._access_token or not self._token_expires_at:
            return False

        # 현재 시간이 만료 시간보다 이전이면 유효
        # 예: 만료 시간이 2025-12-30 23:00이고 현재가 22:00이면 True
        return datetime.now() < self._token_expires_at

    def get_auth_headers(self) -> dict:
        """
        API 요청에 사용할 인증 헤더를 반환합니다.

        KIS API의 모든 요청에 필요한 헤더를 생성합니다.
        - Authorization: Bearer 토큰
        - appkey/appsecret: API 인증 정보
        - content-type: JSON 요청 타입

        Returns:
            인증 헤더 딕셔너리 (requests 라이브러리에서 사용 가능한 형태)

        Example:
            >>> auth = KISAuth()
            >>> headers = auth.get_auth_headers()
            >>> response = requests.get(url, headers=headers)
        """
        # 토큰 가져오기 (없으면 자동 발급, 만료되었으면 자동 갱신)
        token = self.get_access_token()

        # KIS API 표준 헤더 구성
        return {
            "authorization": f"Bearer {token}",  # OAuth 2.0 Bearer 토큰
            "appkey": self.app_key,  # 앱 키 (일부 API에서 필수)
            "appsecret": self.app_secret,  # 앱 시크릿 (일부 API에서 필수)
            "content-type": "application/json; charset=utf-8",  # JSON 형식
        }

    def revoke_token(self) -> bool:
        """
        현재 액세스 토큰을 폐기합니다.

        토큰을 더 이상 사용하지 않을 때 명시적으로 폐기할 수 있습니다.
        보안상 프로그램 종료 시 호출하는 것이 좋습니다.

        Returns:
            폐기 성공 여부 (True/False)
        """
        # 폐기할 토큰이 없으면 False 반환
        if not self._access_token:
            logger.warning("No token to revoke")
            return False

        # 토큰 폐기 엔드포인트
        url = f"{self.base_url}/oauth2/revokeP"

        headers = {"content-type": "application/json"}

        # 요청 본문: 폐기할 토큰 정보
        body = {
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "token": self._access_token,
        }

        try:
            # 토큰 폐기 요청
            response = requests.post(url, headers=headers, json=body, timeout=10)
            response.raise_for_status()

            data = response.json()

            # 폐기 성공 여부 확인
            if data.get("rt_cd") == "0":
                logger.info("Token revoked successfully")
                # 로컬 토큰 정보 삭제
                self._access_token = None
                self._token_expires_at = None
                return True
            else:
                logger.warning(f"Token revoke failed: {data.get('msg1')}")
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Token revoke exception: {e}")
            return False


# ===== 싱글톤 패턴 (선택적 사용) =====
# 전역 인스턴스를 관리하여 프로그램 전체에서 하나의 KISAuth 객체만 사용
_auth_instance: Optional[KISAuth] = None


def get_auth(
    app_key: Optional[str] = None,
    app_secret: Optional[str] = None,
    env: Optional[str] = None,
) -> KISAuth:
    """
    KISAuth 싱글톤 인스턴스를 반환합니다.

    프로그램 전체에서 하나의 인증 객체만 사용하도록 싱글톤 패턴을 구현합니다.
    여러 모듈에서 이 함수를 호출해도 동일한 KISAuth 인스턴스를 공유합니다.

    Args:
        app_key: KIS 앱 키 (첫 호출 시에만 사용됨)
        app_secret: KIS 앱 시크릿 (첫 호출 시에만 사용됨)
        env: 환경 설정 (첫 호출 시에만 사용됨)

    Returns:
        KISAuth 싱글톤 인스턴스

    Example:
        >>> # 첫 호출: 새 인스턴스 생성
        >>> auth1 = get_auth()
        >>> # 두 번째 호출: 기존 인스턴스 반환
        >>> auth2 = get_auth()
        >>> assert auth1 is auth2  # 동일한 객체
    """
    global _auth_instance

    # 인스턴스가 없으면 새로 생성
    if _auth_instance is None:
        _auth_instance = KISAuth(app_key, app_secret, env)

    # 기존 인스턴스 반환
    return _auth_instance
