import importlib.util
import os
import socket
from pathlib import Path
from urllib.parse import urlparse, urlunparse


def _running_in_docker():
    return os.path.exists('/.dockerenv')


def _module_available(module_name):
    return importlib.util.find_spec(module_name) is not None


def _mysql_reachable(host, port, timeout_seconds=1.0):
    try:
        with socket.create_connection((host, port), timeout=timeout_seconds):
            return True
    except OSError:
        return False


def _default_sqlite_url():
    base_dir = Path(__file__).resolve().parent
    instance_dir = base_dir / 'instance'
    instance_dir.mkdir(exist_ok=True)
    db_path = instance_dir / 'holiday_booking.db'
    return f"sqlite:///{db_path.as_posix()}"

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key_change_this_in_prod'
    # Local default used when not running in Docker.
    _default_local_db_url = 'mysql+pymysql://root:pahulpreetbcasem1@localhost/holiday_booking'
    _sqlite_fallback_url = os.environ.get('SQLITE_FALLBACK_URL') or _default_sqlite_url()
    _db_fallback_reason = None
    _db_fallback_enabled = os.environ.get('DISABLE_DB_FALLBACK', '').lower() not in ('1', 'true', 'yes')
    # Supports Docker ("db" host) and local runs.
    _db_url = os.environ.get('DATABASE_URL') or _default_local_db_url
    _parsed = urlparse(_db_url)
    _in_docker = _running_in_docker()
    if _parsed.hostname == 'db' and not _in_docker:
        # When launched locally, a Docker-style DATABASE_URL usually has Docker-only creds/hostname.
        # Prefer explicit LOCAL_DATABASE_URL, otherwise use the local default URL.
        _local_override = os.environ.get('LOCAL_DATABASE_URL')
        if _local_override:
            _db_url = _local_override
        else:
            _db_url = _default_local_db_url
    elif _parsed.hostname == 'db' and _parsed.port and not _in_docker:
        # Safety fallback for odd db-host URLs with port info.
        _host = f'localhost:{_parsed.port}'
        if _parsed.username and _parsed.password:
            _auth = f'{_parsed.username}:{_parsed.password}@{_host}'
        elif _parsed.username:
            _auth = f'{_parsed.username}@{_host}'
        else:
            _auth = _host
        _db_url = urlunparse((_parsed.scheme, _auth, _parsed.path, _parsed.params, _parsed.query, _parsed.fragment))

    _parsed = urlparse(_db_url)
    _using_mysql = _parsed.scheme.startswith('mysql')
    _host = _parsed.hostname
    _port = _parsed.port or 3306

    if _db_fallback_enabled and _using_mysql and not _module_available('pymysql'):
        _db_fallback_reason = 'PyMySQL dependency is not installed.'
        _db_url = _sqlite_fallback_url
    elif (
        _db_fallback_enabled
        and _using_mysql
        and not _in_docker
        and _host in ('localhost', '127.0.0.1', 'db')
        and not _mysql_reachable('localhost' if _host == 'db' else _host, _port)
    ):
        _db_fallback_reason = f'MySQL is not reachable on {_host}:{_port}.'
        _db_url = _sqlite_fallback_url

    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_FALLBACK_REASON = _db_fallback_reason
