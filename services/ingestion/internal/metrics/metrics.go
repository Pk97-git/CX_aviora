package metrics

import (
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
)

var (
	// HTTP Metrics
	HttpRequestsTotal = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "ingestion_http_requests_total",
			Help: "Total number of HTTP requests",
		},
		[]string{"method", "endpoint", "status"},
	)

	HttpRequestDuration = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "ingestion_http_request_duration_seconds",
			Help:    "HTTP request latency in seconds",
			Buckets: prometheus.DefBuckets, // 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10
		},
		[]string{"method", "endpoint"},
	)

	HttpRequestsInFlight = promauto.NewGauge(
		prometheus.GaugeOpts{
			Name: "ingestion_http_requests_in_flight",
			Help: "Current number of HTTP requests being processed",
		},
	)

	// Database Metrics
	DbOperationDuration = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "ingestion_db_operation_duration_seconds",
			Help:    "Database operation latency in seconds",
			Buckets: []float64{0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5},
		},
		[]string{"operation"},
	)

	DbOperationsTotal = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "ingestion_db_operations_total",
			Help: "Total number of database operations",
		},
		[]string{"operation", "status"},
	)

	// Redis Metrics
	RedisOperationDuration = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "ingestion_redis_operation_duration_seconds",
			Help:    "Redis operation latency in seconds",
			Buckets: []float64{0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5},
		},
		[]string{"operation"},
	)

	RedisOperationsTotal = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "ingestion_redis_operations_total",
			Help: "Total number of Redis operations",
		},
		[]string{"operation", "status"},
	)

	// Circuit Breaker Metrics
	CircuitBreakerState = promauto.NewGaugeVec(
		prometheus.GaugeOpts{
			Name: "ingestion_circuit_breaker_state",
			Help: "Circuit breaker state (0=closed, 1=open, 2=half-open)",
		},
		[]string{"name"},
	)

	// Rate Limiter Metrics
	RateLimitExceeded = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "ingestion_rate_limit_exceeded_total",
			Help: "Total number of rate limit exceeded events",
		},
		[]string{"endpoint"},
	)
)
