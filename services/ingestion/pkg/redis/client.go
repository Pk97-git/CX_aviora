package redis

import (
	"context"
	"encoding/json"
	"log"

	"github.com/redis/go-redis/v9"
)

type Client struct {
	rdb *redis.Client
}

// NewClient initializes a new Redis client
func NewClient(url string) (*Client, error) {
	opt, err := redis.ParseURL(url)
	if err != nil {
		return nil, err
	}

	rdb := redis.NewClient(opt)

	// Verify connection
	ctx := context.Background()
	_, err = rdb.Ping(ctx).Result()
	if err != nil {
		return nil, err
	}

	log.Println("✅ Successfully connected to Redis")
	return &Client{rdb: rdb}, nil
}

// Publish publishes a message to a channel
func (c *Client) Publish(ctx context.Context, channel string, message interface{}) error {
	// Marshal message to JSON
	data, err := json.Marshal(message)
	if err != nil {
		return err
	}
	return c.rdb.Publish(ctx, channel, data).Err()
}

// Close closes the Redis connection
func (c *Client) Close() error {
	return c.rdb.Close()
}
