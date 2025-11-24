package middleware

import (
	"strconv"
	"time"

	"github.com/Pk97-git/CX_aviora/services/ingestion/internal/metrics"
	"github.com/gin-gonic/gin"
)

// MetricsMiddleware records HTTP metrics for Prometheus
func MetricsMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		start := time.Now()

		// Increment in-flight requests
		metrics.HttpRequestsInFlight.Inc()
		defer metrics.HttpRequestsInFlight.Dec()

		// Process request
		c.Next()

		// Record metrics
		duration := time.Since(start).Seconds()
		status := strconv.Itoa(c.Writer.Status())

		metrics.HttpRequestsTotal.WithLabelValues(
			c.Request.Method,
			c.FullPath(),
			status,
		).Inc()

		metrics.HttpRequestDuration.WithLabelValues(
			c.Request.Method,
			c.FullPath(),
		).Observe(duration)
	}
}
