package redis

import (
	"context"
	"encoding/json"
	"log"
	"time"

	"github.com/Pk97-git/CX_aviora/services/ingestion/internal/metrics"
	goredis "github.com/redis/go-redis/v9"
	"github.com/sony/gobreaker"
)

type CircuitBreakerClient struct {
	rdb *goredis.Client
	cb  *gobreaker.CircuitBreaker
}

// NewCircuitBreakerClient wraps Redis client with circuit breaker
func NewCircuitBreakerClient(url string, threshold uint32, timeout time.Duration) (*CircuitBreakerClient, error) {
	opt, err := goredis.ParseURL(url)
	if err != nil {
		return nil, err
	}

	rdb := goredis.NewClient(opt)

	// Verify connection
	ctx := context.Background()
	_, err = rdb.Ping(ctx).Result()
	if err != nil {
		return nil, err
	}

	// Configure circuit breaker
	settings := gobreaker.Settings{
		Name:        "RedisCircuitBreaker",
		MaxRequests: 3,
		Interval:    time.Minute,
		Timeout:     timeout,
		ReadyToTrip: func(counts gobreaker.Counts) bool {
			return counts.ConsecutiveFailures >= threshold
		},
		OnStateChange: func(name string, from gobreaker.State, to gobreaker.State) {
			log.Printf("🔌 Circuit Breaker [%s]: %s → %s", name, from, to)

			// Update metrics
			var state float64
			switch to {
			case gobreaker.StateClosed:
				state = 0
			case gobreaker.StateOpen:
				state = 1
			case gobreaker.StateHalfOpen:
				state = 2
			}
			metrics.CircuitBreakerState.WithLabelValues(name).Set(state)
		},
	}

	cb := gobreaker.NewCircuitBreaker(settings)

	log.Println("✅ Successfully connected to Redis with Circuit Breaker")
	return &CircuitBreakerClient{rdb: rdb, cb: cb}, nil
}

// Publish publishes a message to a channel with circuit breaker protection
func (c *CircuitBreakerClient) Publish(ctx context.Context, channel string, message interface{}) error {
	_, err := c.cb.Execute(func() (interface{}, error) {
		// Marshal message to JSON
		data, err := json.Marshal(message)
		if err != nil {
			return nil, err
		}

		start := time.Now()
		err = c.rdb.Publish(ctx, channel, data).Err()
		duration := time.Since(start).Seconds()

		// Record metrics
		status := "success"
		if err != nil {
			status = "error"
		}
		metrics.RedisOperationsTotal.WithLabelValues("publish", status).Inc()
		metrics.RedisOperationDuration.WithLabelValues("publish").Observe(duration)

		return nil, err
	})

	if err != nil {
		// Circuit breaker is open or operation failed
		log.Printf("⚠️  Redis publish failed (circuit breaker may be open): %v", err)
		// Don't return error - allow request to succeed even if Redis is down
		return nil
	}

	return nil
}

// Close closes the Redis connection
func (c *CircuitBreakerClient) Close() error {
	return c.rdb.Close()
}
