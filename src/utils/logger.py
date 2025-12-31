"""
로깅 시스템 설정 모듈

이 모듈은 HPT Trading System의 통합 로깅 시스템을 제공합니다.
- 콘솔 출력: 개발 중 실시간 로그 확인
- 파일 로테이션: 로그 파일 크기 관리 및 자동 백업
- 설정 기반: YAML 파일로 로그 레벨, 포맷 등 커스터마이징

사용 예시:
    from src.utils.logger import get_logger

    logger = get_logger(__name__)
    logger.info("Trading started")
    logger.error("Order failed", exc_info=True)
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional

import yaml


def setup_logger(
    name: str = "hpt_trading",
    config_path: Optional[str] = None,
    log_level: Optional[str] = None,
) -> logging.Logger:
    """
    로거를 설정하고 반환합니다.

    이 함수는 config/config.yaml 파일의 설정을 기반으로 로거를 초기화합니다.
    콘솔 출력과 파일 출력(로테이션)을 모두 지원하며, 중복 초기화를 방지합니다.

    Args:
        name: 로거 이름 (보통 __name__ 또는 "hpt_trading")
        config_path: 설정 파일 경로 (기본값: config/config.yaml)
        log_level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                   이 인자가 제공되면 환경변수/설정파일보다 우선 적용됨

    Returns:
        설정된 logging.Logger 객체

    Raises:
        없음 (설정 파일이 없어도 기본값으로 동작)

    Example:
        >>> logger = setup_logger("my_module", log_level="DEBUG")
        >>> logger.debug("디버그 메시지")
    """
    # 로거 인스턴스 가져오기 (이미 존재하면 재사용)
    logger = logging.getLogger(name)

    # 중복 초기화 방지: 핸들러가 이미 설정되어 있으면 기존 로거 반환
    # 이렇게 하면 동일한 로거를 여러 번 setup_logger로 호출해도 안전함
    if logger.handlers:
        return logger

    # ===== 1. 설정 파일 로드 =====
    if config_path is None:
        config_path = "config/config.yaml"

    try:
        # YAML 파일에서 로깅 설정 읽기
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            log_config = config.get("logging", {})
    except FileNotFoundError:
        # 설정 파일이 없으면 빈 딕셔너리 사용 (기본값으로 동작)
        log_config = {}

    # ===== 2. 로그 레벨 설정 =====
    # 우선순위: 함수 인자 > 환경변수(LOG_LEVEL) > 설정파일 > 기본값(INFO)
    if log_level:
        # 함수 인자로 레벨이 제공된 경우 (최우선)
        level = log_level.upper()
    else:
        # 환경변수 또는 설정 파일에서 로드
        level = (
            os.getenv("LOG_LEVEL")  # 환경변수 우선
            or log_config.get("level", "INFO")  # 설정파일 또는 기본값
        ).upper()

    # 로거의 최소 로그 레벨 설정
    # 예: INFO로 설정하면 DEBUG는 무시되고 INFO 이상만 출력됨
    logger.setLevel(getattr(logging, level))

    # ===== 3. 로그 포맷 설정 =====
    # 포맷 문자열: "시간 - 로거명 - 레벨 - 메시지"
    # 예: "2025-12-30 20:30:15 - hpt_trading - INFO - Trading started"
    log_format = log_config.get(
        "format",
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    formatter = logging.Formatter(log_format)

    # ===== 4. 콘솔 핸들러 설정 =====
    # 터미널/콘솔에 로그를 실시간으로 출력
    console_config = log_config.get("console", {"enabled": True})
    if console_config.get("enabled", True):
        # StreamHandler: stdout으로 로그 출력
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)  # 포맷 적용
        logger.addHandler(console_handler)

    # ===== 5. 파일 핸들러 설정 (로테이션) =====
    # 로그를 파일에 저장하며, 파일 크기가 일정 이상이 되면 자동으로 백업
    file_config = log_config.get("file", {})
    if file_config.get("enabled", False):  # 기본값은 비활성화
        log_file = file_config.get("path", "logs/trading.log")

        # 로그 디렉토리가 없으면 생성
        # 예: logs/trading.log → logs/ 디렉토리 생성
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)

        # 로테이션 설정
        max_bytes = file_config.get("max_bytes", 10485760)  # 10MB
        backup_count = file_config.get("backup_count", 5)  # 최대 5개 백업

        # RotatingFileHandler: 로그 파일이 max_bytes를 초과하면
        # trading.log.1, trading.log.2, ... 형태로 백업 파일 생성
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",  # 한글 지원
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # ===== 6. 로거 전파 방지 =====
    # False로 설정하면 상위 로거(root logger)로 로그가 전파되지 않음
    # 이렇게 하면 로그가 중복으로 출력되는 것을 방지
    logger.propagate = False

    # 로거 초기화 완료 로그
    logger.info(f"Logger '{name}' initialized with level {level}")

    return logger


def get_logger(name: str = "hpt_trading") -> logging.Logger:
    """
    기존 로거를 반환하거나 없으면 새로 생성합니다.

    이 함수는 로거를 가져올 때 사용하는 편의 함수입니다.
    setup_logger()와 달리 매번 설정을 다시 읽지 않고, 이미 초기화된
    로거가 있으면 그것을 재사용합니다.

    Args:
        name: 로거 이름 (모듈별로 다른 이름 사용 권장)
              예: get_logger(__name__)

    Returns:
        logging.Logger 객체 (설정된 핸들러 포함)

    Example:
        >>> # 각 모듈에서 사용
        >>> logger = get_logger(__name__)
        >>> logger.info("모듈 시작")
        >>>
        >>> # 또는 전역 로거 사용
        >>> logger = get_logger("hpt_trading")
        >>> logger.debug("디버그 정보")
    """
    # 기존 로거 인스턴스 가져오기
    logger = logging.getLogger(name)

    # 로거가 아직 설정되지 않았으면 (핸들러가 없으면) setup 호출
    # 이미 설정되어 있으면 기존 로거를 그대로 반환
    if not logger.handlers:
        return setup_logger(name)

    return logger
