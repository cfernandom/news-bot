"""
Performance monitoring system for PreventIA News Analytics
Tracks scraper performance metrics and provides insights for optimization
"""

import json
import statistics
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from threading import Lock
from typing import Any, Dict, List, Optional

from services.shared.logging.structured_logger import get_logger

logger = get_logger("scraper.performance_monitor")


@dataclass
class PerformanceMetric:
    """Individual performance metric entry"""

    timestamp: datetime
    domain: str
    scraper_name: str
    metric_type: str
    value: float
    unit: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ScraperPerformanceStats:
    """Performance statistics for a scraper"""

    domain: str
    scraper_name: str
    total_runs: int = 0
    successful_runs: int = 0
    failed_runs: int = 0
    total_articles: int = 0
    total_execution_time: float = 0.0

    # Response time metrics
    response_times: deque = field(default_factory=lambda: deque(maxlen=100))
    avg_response_time: float = 0.0
    min_response_time: float = float("inf")
    max_response_time: float = 0.0

    # Throughput metrics
    articles_per_second: float = 0.0
    articles_per_minute: float = 0.0

    # Quality metrics
    articles_with_dates: int = 0
    articles_with_summaries: int = 0
    duplicate_articles: int = 0

    # Error metrics
    error_rate: float = 0.0
    consecutive_failures: int = 0
    last_error: Optional[str] = None
    last_error_time: Optional[datetime] = None

    # Timestamps
    first_run: Optional[datetime] = None
    last_run: Optional[datetime] = None
    last_successful_run: Optional[datetime] = None


class PerformanceMonitor:
    """
    Comprehensive performance monitoring system for scrapers
    """

    def __init__(self, max_metrics_per_domain: int = 1000):
        self.max_metrics_per_domain = max_metrics_per_domain
        self.metrics: Dict[str, deque] = defaultdict(
            lambda: deque(maxlen=max_metrics_per_domain)
        )
        self.stats: Dict[str, ScraperPerformanceStats] = {}
        self.lock = Lock()

        # System-wide metrics
        self.system_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_articles": 0,
            "start_time": datetime.now(),
            "last_activity": datetime.now(),
        }

    def record_metric(
        self,
        domain: str,
        scraper_name: str,
        metric_type: str,
        value: float,
        unit: str = "ms",
        **metadata,
    ):
        """Record a performance metric"""
        with self.lock:
            metric = PerformanceMetric(
                timestamp=datetime.now(),
                domain=domain,
                scraper_name=scraper_name,
                metric_type=metric_type,
                value=value,
                unit=unit,
                metadata=metadata,
            )

            self.metrics[domain].append(metric)
            self.system_stats["last_activity"] = datetime.now()

            logger.debug(
                "Recorded performance metric",
                domain=domain,
                scraper_name=scraper_name,
                metric_type=metric_type,
                value=value,
                unit=unit,
            )

    def start_scraper_run(self, domain: str, scraper_name: str) -> Dict[str, Any]:
        """Start tracking a scraper run"""
        run_id = f"{domain}_{scraper_name}_{int(time.time())}"

        with self.lock:
            if domain not in self.stats:
                self.stats[domain] = ScraperPerformanceStats(
                    domain=domain, scraper_name=scraper_name, first_run=datetime.now()
                )

            stats = self.stats[domain]
            stats.total_runs += 1
            stats.last_run = datetime.now()

            if stats.first_run is None:
                stats.first_run = datetime.now()

            self.system_stats["total_requests"] += 1

        return {
            "run_id": run_id,
            "start_time": time.time(),
            "domain": domain,
            "scraper_name": scraper_name,
        }

    def end_scraper_run(
        self,
        run_context: Dict[str, Any],
        success: bool,
        articles_found: int = 0,
        error_message: str = None,
    ):
        """End tracking a scraper run"""
        execution_time = time.time() - run_context["start_time"]
        domain = run_context["domain"]
        scraper_name = run_context["scraper_name"]

        with self.lock:
            stats = self.stats.get(domain)
            if not stats:
                return

            # Update basic stats
            stats.total_execution_time += execution_time
            stats.total_articles += articles_found

            # Record response time
            stats.response_times.append(execution_time)
            if execution_time < stats.min_response_time:
                stats.min_response_time = execution_time
            if execution_time > stats.max_response_time:
                stats.max_response_time = execution_time

            # Calculate average response time
            if stats.response_times:
                stats.avg_response_time = statistics.mean(stats.response_times)

            # Calculate throughput
            if execution_time > 0:
                stats.articles_per_second = articles_found / execution_time
                stats.articles_per_minute = (articles_found / execution_time) * 60

            # Update success/failure stats
            if success:
                stats.successful_runs += 1
                stats.consecutive_failures = 0
                stats.last_successful_run = datetime.now()
                self.system_stats["successful_requests"] += 1
            else:
                stats.failed_runs += 1
                stats.consecutive_failures += 1
                stats.last_error = error_message
                stats.last_error_time = datetime.now()
                self.system_stats["failed_requests"] += 1

            # Calculate error rate
            stats.error_rate = stats.failed_runs / stats.total_runs

            # Update system stats
            self.system_stats["total_articles"] += articles_found

        # Record metrics
        self.record_metric(
            domain, scraper_name, "execution_time", execution_time, "seconds"
        )
        self.record_metric(
            domain, scraper_name, "articles_found", articles_found, "count"
        )
        self.record_metric(
            domain, scraper_name, "success", 1 if success else 0, "boolean"
        )

        logger.info(
            "Scraper run completed",
            domain=domain,
            scraper_name=scraper_name,
            success=success,
            articles_found=articles_found,
            execution_time=execution_time,
            error_message=error_message,
        )

    def record_article_quality(
        self,
        domain: str,
        scraper_name: str,
        has_date: bool,
        has_summary: bool,
        is_duplicate: bool,
    ):
        """Record article quality metrics"""
        with self.lock:
            stats = self.stats.get(domain)
            if not stats:
                return

            if has_date:
                stats.articles_with_dates += 1
            if has_summary:
                stats.articles_with_summaries += 1
            if is_duplicate:
                stats.duplicate_articles += 1

        # Record individual metrics
        self.record_metric(
            domain, scraper_name, "article_has_date", 1 if has_date else 0, "boolean"
        )
        self.record_metric(
            domain,
            scraper_name,
            "article_has_summary",
            1 if has_summary else 0,
            "boolean",
        )
        self.record_metric(
            domain,
            scraper_name,
            "article_is_duplicate",
            1 if is_duplicate else 0,
            "boolean",
        )

    def get_scraper_stats(self, domain: str) -> Optional[ScraperPerformanceStats]:
        """Get performance statistics for a scraper"""
        with self.lock:
            return self.stats.get(domain)

    def get_all_scraper_stats(self) -> Dict[str, ScraperPerformanceStats]:
        """Get performance statistics for all scrapers"""
        with self.lock:
            return self.stats.copy()

    def get_system_stats(self) -> Dict[str, Any]:
        """Get system-wide performance statistics"""
        with self.lock:
            stats = self.system_stats.copy()

            # Calculate derived metrics
            total_requests = stats["total_requests"]
            if total_requests > 0:
                stats["success_rate"] = stats["successful_requests"] / total_requests
                stats["failure_rate"] = stats["failed_requests"] / total_requests
            else:
                stats["success_rate"] = 0.0
                stats["failure_rate"] = 0.0

            # Calculate uptime
            uptime = datetime.now() - stats["start_time"]
            stats["uptime_seconds"] = uptime.total_seconds()
            stats["uptime_hours"] = uptime.total_seconds() / 3600

            # Calculate overall throughput
            if stats["uptime_seconds"] > 0:
                stats["articles_per_hour"] = stats["total_articles"] / (
                    stats["uptime_seconds"] / 3600
                )
                stats["requests_per_hour"] = total_requests / (
                    stats["uptime_seconds"] / 3600
                )
            else:
                stats["articles_per_hour"] = 0.0
                stats["requests_per_hour"] = 0.0

            return stats

    def get_performance_report(
        self, domain: str = None, hours: int = 24
    ) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        cutoff_time = datetime.now() - timedelta(hours=hours)

        with self.lock:
            if domain:
                # Single domain report
                stats = self.stats.get(domain)
                if not stats:
                    return {"error": f"No stats found for domain {domain}"}

                # Filter recent metrics
                recent_metrics = [
                    m for m in self.metrics[domain] if m.timestamp > cutoff_time
                ]

                return {
                    "domain": domain,
                    "period_hours": hours,
                    "stats": stats,
                    "recent_metrics_count": len(recent_metrics),
                    "performance_grade": self._calculate_performance_grade(stats),
                }
            else:
                # All domains report
                report = {
                    "period_hours": hours,
                    "system_stats": self.get_system_stats(),
                    "scrapers": {},
                }

                for domain, stats in self.stats.items():
                    recent_metrics = [
                        m for m in self.metrics[domain] if m.timestamp > cutoff_time
                    ]

                    report["scrapers"][domain] = {
                        "stats": stats,
                        "recent_metrics_count": len(recent_metrics),
                        "performance_grade": self._calculate_performance_grade(stats),
                    }

                return report

    def _calculate_performance_grade(self, stats: ScraperPerformanceStats) -> str:
        """Calculate performance grade based on metrics"""
        if stats.total_runs == 0:
            return "N/A"

        score = 0
        max_score = 100

        # Success rate (40 points)
        success_rate = stats.successful_runs / stats.total_runs
        score += success_rate * 40

        # Response time (20 points)
        if stats.avg_response_time > 0:
            # Good response time is under 10 seconds
            if stats.avg_response_time <= 10:
                score += 20
            elif stats.avg_response_time <= 30:
                score += 10
            # else: 0 points

        # Article quality (20 points)
        if stats.total_articles > 0:
            date_rate = stats.articles_with_dates / stats.total_articles
            summary_rate = stats.articles_with_summaries / stats.total_articles
            duplicate_rate = stats.duplicate_articles / stats.total_articles

            quality_score = (
                date_rate * 0.4 + summary_rate * 0.4 + (1 - duplicate_rate) * 0.2
            ) * 20
            score += quality_score

        # Consistency (20 points)
        if stats.consecutive_failures == 0:
            score += 20
        elif stats.consecutive_failures <= 3:
            score += 10
        # else: 0 points

        # Convert to letter grade
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def get_metrics_by_type(
        self, domain: str, metric_type: str, hours: int = 24
    ) -> List[PerformanceMetric]:
        """Get metrics of a specific type for a domain"""
        cutoff_time = datetime.now() - timedelta(hours=hours)

        with self.lock:
            domain_metrics = self.metrics.get(domain, [])
            return [
                m
                for m in domain_metrics
                if m.metric_type == metric_type and m.timestamp > cutoff_time
            ]

    def get_trending_metrics(
        self, domain: str, metric_type: str, hours: int = 24
    ) -> Dict[str, Any]:
        """Get trending analysis for a metric"""
        metrics = self.get_metrics_by_type(domain, metric_type, hours)

        if len(metrics) < 2:
            return {"error": "Insufficient data for trending analysis"}

        # Sort by timestamp
        metrics.sort(key=lambda x: x.timestamp)

        # Calculate trend
        values = [m.value for m in metrics]
        timestamps = [m.timestamp for m in metrics]

        # Simple linear trend calculation
        n = len(values)
        sum_x = sum(range(n))
        sum_y = sum(values)
        sum_xy = sum(i * values[i] for i in range(n))
        sum_x2 = sum(i * i for i in range(n))

        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)

        return {
            "domain": domain,
            "metric_type": metric_type,
            "data_points": n,
            "trend_slope": slope,
            "trend_direction": (
                "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable"
            ),
            "current_value": values[-1],
            "previous_value": values[-2],
            "change": values[-1] - values[-2],
            "change_percent": (
                ((values[-1] - values[-2]) / values[-2] * 100) if values[-2] != 0 else 0
            ),
            "min_value": min(values),
            "max_value": max(values),
            "avg_value": statistics.mean(values),
            "period_start": timestamps[0],
            "period_end": timestamps[-1],
        }

    def cleanup_old_metrics(self, days: int = 7):
        """Clean up old metrics to prevent memory issues"""
        cutoff_time = datetime.now() - timedelta(days=days)
        cleaned_count = 0

        with self.lock:
            for domain in self.metrics:
                original_count = len(self.metrics[domain])

                # Keep only recent metrics
                self.metrics[domain] = deque(
                    [m for m in self.metrics[domain] if m.timestamp > cutoff_time],
                    maxlen=self.max_metrics_per_domain,
                )

                cleaned_count += original_count - len(self.metrics[domain])

        if cleaned_count > 0:
            logger.info(
                "Cleaned up old metrics", cleaned_count=cleaned_count, days=days
            )

        return cleaned_count

    def export_metrics(self, domain: str = None, hours: int = 24) -> str:
        """Export metrics as JSON"""
        cutoff_time = datetime.now() - timedelta(hours=hours)

        with self.lock:
            if domain:
                domain_metrics = self.metrics.get(domain, [])
                export_data = {
                    "domain": domain,
                    "period_hours": hours,
                    "metrics": [
                        {
                            "timestamp": m.timestamp.isoformat(),
                            "metric_type": m.metric_type,
                            "value": m.value,
                            "unit": m.unit,
                            "metadata": m.metadata,
                        }
                        for m in domain_metrics
                        if m.timestamp > cutoff_time
                    ],
                }
            else:
                export_data = {"period_hours": hours, "domains": {}}

                for domain, domain_metrics in self.metrics.items():
                    export_data["domains"][domain] = [
                        {
                            "timestamp": m.timestamp.isoformat(),
                            "metric_type": m.metric_type,
                            "value": m.value,
                            "unit": m.unit,
                            "metadata": m.metadata,
                        }
                        for m in domain_metrics
                        if m.timestamp > cutoff_time
                    ]

        return json.dumps(export_data, indent=2)


# Global performance monitor instance
_performance_monitor = PerformanceMonitor()


def get_performance_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance"""
    return _performance_monitor


# Context manager for performance tracking
class PerformanceTracker:
    """Context manager for tracking scraper performance"""

    def __init__(self, domain: str, scraper_name: str):
        self.domain = domain
        self.scraper_name = scraper_name
        self.monitor = get_performance_monitor()
        self.run_context = None

    def __enter__(self):
        self.run_context = self.monitor.start_scraper_run(
            self.domain, self.scraper_name
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        success = exc_type is None
        error_message = str(exc_val) if exc_val else None

        self.monitor.end_scraper_run(
            self.run_context, success, getattr(self, "articles_found", 0), error_message
        )

    def set_articles_found(self, count: int):
        """Set the number of articles found"""
        self.articles_found = count

    def record_article_quality(
        self, has_date: bool, has_summary: bool, is_duplicate: bool
    ):
        """Record article quality metrics"""
        self.monitor.record_article_quality(
            self.domain, self.scraper_name, has_date, has_summary, is_duplicate
        )


if __name__ == "__main__":
    # Example usage
    monitor = get_performance_monitor()

    # Example of tracking a scraper run
    with PerformanceTracker("example.com", "example_scraper") as tracker:
        # Simulate scraping
        time.sleep(1)
        tracker.set_articles_found(10)
        tracker.record_article_quality(True, True, False)

    # Get stats
    stats = monitor.get_scraper_stats("example.com")
    print(f"Scraper stats: {stats}")

    # Get system stats
    system_stats = monitor.get_system_stats()
    print(f"System stats: {system_stats}")

    # Get performance report
    report = monitor.get_performance_report()
    print(f"Performance report: {report}")
