import os
import statistics
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ["DATABASE_URL"] = "sqlite:///./benchmark_llm_profiler.db"
os.environ["SECRET_KEY"] = "benchmark-secret"
os.environ["GROQ_API_KEY"] = "benchmark-no-live-key"
os.environ["DEBUG"] = "false"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.v1.endpoints import generate as generate_endpoint
from app.db.base import Base
from app.models.request_log import RequestLog
from app.schemas.generate import GenerateRequest
from app.services.analytics_service import AnalyticsService
from app.services.llm_service import MODEL_PRICING
from app.services.rate_limiter import RateLimiter


class InMemoryCache:
    def __init__(self):
        self.store = {}

    def make_key(self, prompt: str, model: str):
        return f"llm:{model}:{hash(prompt)}"

    def get(self, key: str):
        return self.store.get(key)

    def set(self, key: str, value, ttl: int = 300):
        self.store[key] = value


class InMemoryRateLimiter:
    def __init__(self, limit=10):
        self.limit = limit
        self.counts = {}

    def is_allowed(self, user_id: str, limit: int = 10, window: int = 60):
        count = self.counts.get(user_id, 0)
        effective_limit = limit if limit is not None else self.limit
        if count >= effective_limit:
            return False
        self.counts[user_id] = count + 1
        return True


class FakeLLMService:
    def __init__(self):
        self.calls = 0

    def generate(self, prompt: str):
        self.calls += 1
        prompt_tokens = len(prompt.split())
        completion_tokens = 12
        pricing = MODEL_PRICING["llama-3.1-8b-instant"]
        cost = round(
            prompt_tokens * pricing["input"] + completion_tokens * pricing["output"],
            6,
        )
        return {
            "answer": "benchmark response",
            "latency_ms": 0.0,
            "tokens": prompt_tokens + completion_tokens,
            "cost": cost,
        }


class FakeRedis:
    def __init__(self):
        self.values = {}

    def get(self, key):
        return self.values.get(key)

    def set(self, key, value, ex=None):
        self.values[key] = int(value)

    def incr(self, key):
        self.values[key] = int(self.values.get(key, 0)) + 1


def timed_ms(fn, samples=1):
    timings = []
    result = None
    for _ in range(samples):
        start = time.perf_counter()
        result = fn()
        timings.append((time.perf_counter() - start) * 1000)
    return result, timings


def percentile(values, pct):
    if not values:
        return 0.0
    ordered = sorted(values)
    index = round((len(ordered) - 1) * pct)
    return ordered[index]


def summarize_timings(values):
    return {
        "samples": len(values),
        "min_ms": round(min(values), 3),
        "median_ms": round(statistics.median(values), 3),
        "p95_ms": round(percentile(values, 0.95), 3),
        "max_ms": round(max(values), 3),
    }


def benchmark_generate(session):
    fake_cache = InMemoryCache()
    fake_llm = FakeLLMService()
    generate_endpoint.cache_service = fake_cache
    generate_endpoint.rate_limiter = InMemoryRateLimiter()
    generate_endpoint.llm_service = fake_llm

    prompt = "benchmark prompt for cache behavior"

    uncached_response, uncached_timings = timed_ms(
        lambda: generate_endpoint.generate(
            GenerateRequest(prompt=prompt, user_id="bench-generate"), db=session
        )
    )

    cached_timings = []
    cached_responses = []
    for _ in range(50):
        response, timings = timed_ms(
            lambda: generate_endpoint.generate(
                GenerateRequest(prompt=prompt, user_id=f"bench-cache-{time.perf_counter_ns()}"),
                db=session,
            )
        )
        cached_responses.append(response)
        cached_timings.extend(timings)

    return {
        "uncached": {
            "response_cached": uncached_response["cached"],
            "timing": summarize_timings(uncached_timings),
        },
        "cached": {
            "all_responses_cached": all(r["cached"] for r in cached_responses),
            "timing": summarize_timings(cached_timings),
        },
        "llm_calls_made": fake_llm.calls,
        "redundant_llm_calls_prevented": len(cached_responses),
    }


def seed_logs(session, rows=5000):
    batch = []
    for i in range(rows):
        cached = i % 4 == 0
        batch.append(
            RequestLog(
                prompt=f"prompt {i}",
                response=f"response {i}",
                latency_ms=5.0 + (i % 30),
                tokens=100 + (i % 50),
                cost=0.0 if cached else 0.00025,
                estimated_cost=0.00025 if cached else 0.0,
                cached=cached,
            )
        )
    session.bulk_save_objects(batch)
    session.commit()


def benchmark_analytics(session):
    service = AnalyticsService()
    result, timings = timed_ms(lambda: service.get_summary(session), samples=30)
    return {
        "summary": result,
        "timing": summarize_timings(timings),
    }


def benchmark_rate_limiter():
    limiter = RateLimiter()
    limiter.client = FakeRedis()
    outcomes = [limiter.is_allowed("bench-user") for _ in range(12)]
    first_blocked_at = next((i + 1 for i, allowed in enumerate(outcomes) if not allowed), None)
    return {
        "default_limit_per_60s": 10,
        "outcomes": outcomes,
        "first_blocked_request_number": first_blocked_at,
        "allowed_before_block": sum(1 for allowed in outcomes if allowed),
    }


def verify_cost_saved_math(session):
    service = AnalyticsService()
    session.query(RequestLog).delete()
    session.add_all(
        [
            RequestLog(
                prompt="uncached low",
                response="ok",
                latency_ms=10,
                tokens=10,
                cost=0.001,
                estimated_cost=0.0,
                cached=False,
            ),
            RequestLog(
                prompt="uncached high",
                response="ok",
                latency_ms=20,
                tokens=20,
                cost=0.002,
                estimated_cost=0.0,
                cached=False,
            ),
            RequestLog(
                prompt="cached one",
                response="ok",
                latency_ms=1,
                tokens=10,
                cost=0.001,
                estimated_cost=0.001,
                cached=True,
            ),
            RequestLog(
                prompt="cached two",
                response="ok",
                latency_ms=1,
                tokens=20,
                cost=0.002,
                estimated_cost=0.002,
                cached=True,
            ),
        ]
    )
    session.commit()
    summary = service.get_summary(session)
    expected = {
        "total_cost": 0.003,
        "cost_saved": 0.003,
        "cache_hit_rate": 50.0,
    }
    return {
        "summary": summary,
        "expected": expected,
        "matches": all(abs(summary[key] - value) < 0.000001 for key, value in expected.items()),
    }


def main():
    db_path = Path(tempfile.gettempdir()) / f"llm_profiler_benchmark_{os.getpid()}.db"
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    with Session() as session:
        generate_result = benchmark_generate(session)
        session.query(RequestLog).delete()
        session.commit()
        seed_logs(session)
        analytics_result = benchmark_analytics(session)
        rate_limit_result = benchmark_rate_limiter()
        cost_math_result = verify_cost_saved_math(session)

    print("LLM Profiler benchmark results")
    print(f"database={db_path}")
    print(f"generate={generate_result}")
    print(f"analytics={analytics_result}")
    print(f"rate_limiter={rate_limit_result}")
    print(f"cost_math={cost_math_result}")
    print("live_llm_api_keys_used=False")


if __name__ == "__main__":
    main()
