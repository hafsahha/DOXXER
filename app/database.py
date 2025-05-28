from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from urllib.parse import urlparse
from sqlalchemy import create_engine
import os

db = SQLAlchemy()

# Session yang bisa diganti-ganti tergantung domain
SessionLocal = {}

def get_domain_from_url(url):
    parsed = urlparse(url)
    return parsed.netloc.replace("www.", "")

def get_domain_db_path(domain, method):
    return os.path.join('instance', f'{method}-{domain}.db')

def get_session_for_domain(domain, method):
    if domain not in SessionLocal:
        db_path = get_domain_db_path(domain, method)
        engine = create_engine(f'sqlite:///{db_path}')
        session_factory = sessionmaker(bind=engine)
        SessionLocal[domain] = scoped_session(session_factory)
        return SessionLocal[domain], engine
    
    return SessionLocal[domain], SessionLocal[domain].bind
