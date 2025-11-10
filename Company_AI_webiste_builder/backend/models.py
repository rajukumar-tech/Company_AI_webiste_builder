# models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

def gen_uuid():
    return str(uuid.uuid4())

class Page(Base):
    __tablename__ = "pages"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    content = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Job(Base):
    __tablename__ = "jobs"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    title = Column(String(255), nullable=False)
    skills = Column(String(500))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Application(Base):
    __tablename__ = "applications"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    name = Column(String(200))
    email = Column(String(200))
    job_title = Column(String(200))
    resume_path = Column(String(1000))
    parsed = Column(JSON)
    score = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Portfolio(Base):
    __tablename__ = "portfolios"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    html = Column(Text)
    meta = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BlogPost(Base):
    __tablename__ = "blog_posts"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    title = Column(String(255))
    content = Column(Text)
    summary = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Testimonial(Base):
    __tablename__ = "testimonials"
    id = Column(String(36), primary_key=True, default=gen_uuid)
    client = Column(String(200))
    quote = Column(Text)
    author = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Analytics(Base):
    __tablename__ = "analytics"
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True)
    value = Column(JSON)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
