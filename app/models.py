"""Database models for SiteCheck."""

from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Site(Base):
    """A website owned and monitored by a user."""

    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    hostname: Mapped[str] = mapped_column(String(255), nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verify_token: Mapped[str | None] = mapped_column(String(64), nullable=True)
    verify_method: Mapped[str | None] = mapped_column(String(16), nullable=True)
    check_interval_s: Mapped[int] = mapped_column(Integer, default=300, nullable=False)
    scan_interval_h: Mapped[int] = mapped_column(Integer, default=24, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)

    checks: Mapped[list["Check"]] = relationship(
        back_populates="site", cascade="all, delete-orphan"
    )
    scans: Mapped[list["Scan"]] = relationship(back_populates="site", cascade="all, delete-orphan")
    incidents: Mapped[list["Incident"]] = relationship(
        back_populates="site", cascade="all, delete-orphan"
    )
    alert_channels: Mapped[list["AlertChannel"]] = relationship(
        back_populates="site", cascade="all, delete-orphan"
    )


class Check(Base):
    """One uptime probe."""

    __tablename__ = "checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"), nullable=False, index=True)
    ts: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    ok: Mapped[bool] = mapped_column(Boolean, nullable=False)
    status_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    dns_ms: Mapped[float | None] = mapped_column(nullable=True)
    ttfb_ms: Mapped[float | None] = mapped_column(nullable=True)
    total_ms: Mapped[float | None] = mapped_column(nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)

    site: Mapped["Site"] = relationship(back_populates="checks")


class Scan(Base):
    """One passive security scan."""

    __tablename__ = "scans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"), nullable=False, index=True)
    ts: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    grade: Mapped[str] = mapped_column(String(1), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    site: Mapped["Site"] = relationship(back_populates="scans")
    findings: Mapped[list["Finding"]] = relationship(
        back_populates="scan", cascade="all, delete-orphan"
    )


class Finding(Base):
    """A result from a security check."""

    __tablename__ = "findings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scans.id"), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(16), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False)
    fix: Mapped[str] = mapped_column(Text, nullable=False)
    check_id: Mapped[str] = mapped_column(String(64), nullable=False)

    scan: Mapped["Scan"] = relationship(back_populates="findings")


class Incident(Base):
    """A continuous uptime incident."""

    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"), nullable=False, index=True)
    started_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(nullable=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)

    site: Mapped["Site"] = relationship(back_populates="incidents")


class AlertChannel(Base):
    """A destination for alert notifications."""

    __tablename__ = "alert_channels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(16), nullable=False)
    target: Mapped[str] = mapped_column(Text, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    min_severity: Mapped[str] = mapped_column(String(16), default="low", nullable=False)

    site: Mapped["Site"] = relationship(back_populates="alert_channels")
