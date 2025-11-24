package config

import (
	"log"

	"github.com/spf13/viper"
)

type Config struct {
	DatabaseURL             string `mapstructure:"DATABASE_URL"`
	RedisURL                string `mapstructure:"REDIS_URL"`
	Port                    string `mapstructure:"PORT"`
	FreshdeskWebhookSecret  string `mapstructure:"FRESHDESK_WEBHOOK_SECRET"`
	ZendeskWebhookSecret    string `mapstructure:"ZENDESK_WEBHOOK_SECRET"`
	RateLimitPerMinute      int    `mapstructure:"RATE_LIMIT_PER_MINUTE"`
	CircuitBreakerThreshold int    `mapstructure:"CIRCUIT_BREAKER_THRESHOLD"`
	CircuitBreakerTimeout   int    `mapstructure:"CIRCUIT_BREAKER_TIMEOUT"` // seconds
}

func LoadConfig() (*Config, error) {
	// Look for .env file in multiple locations
	viper.AddConfigPath(".")     // Look in current directory
	viper.AddConfigPath("../..") // Look in project root (for local dev)
	viper.SetConfigName(".env")
	viper.SetConfigType("env")

	// Enable automatic environment variable reading
	viper.AutomaticEnv()

	// Explicitly bind environment variables to config keys
	// This is CRITICAL for Docker containers where .env file doesn't exist
	viper.BindEnv("DATABASE_URL")
	viper.BindEnv("REDIS_URL")
	viper.BindEnv("PORT")
	viper.BindEnv("FRESHDESK_WEBHOOK_SECRET")
	viper.BindEnv("ZENDESK_WEBHOOK_SECRET")
	viper.BindEnv("RATE_LIMIT_PER_MINUTE")
	viper.BindEnv("CIRCUIT_BREAKER_THRESHOLD")
	viper.BindEnv("CIRCUIT_BREAKER_TIMEOUT")

	// Set defaults
	viper.SetDefault("PORT", "8080")
	viper.SetDefault("RATE_LIMIT_PER_MINUTE", 100)
	viper.SetDefault("CIRCUIT_BREAKER_THRESHOLD", 5)
	viper.SetDefault("CIRCUIT_BREAKER_TIMEOUT", 30)

	// Try to read config file, but don't fail if it doesn't exist
	if err := viper.ReadInConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			log.Println("ℹ️  No .env file found, using environment variables")
		} else {
			log.Printf("⚠️  Warning: Failed to read config file: %v", err)
		}
	}

	var config Config
	if err := viper.Unmarshal(&config); err != nil {
		return nil, err
	}

	return &config, nil
}
