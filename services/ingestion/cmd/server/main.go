package main

import (
	"log"
	"time"

	"github.com/Pk97-git/CX_aviora/services/ingestion/internal/config"
	"github.com/Pk97-git/CX_aviora/services/ingestion/internal/database"
	"github.com/Pk97-git/CX_aviora/services/ingestion/internal/handlers"
	"github.com/Pk97-git/CX_aviora/services/ingestion/internal/middleware"
	"github.com/Pk97-git/CX_aviora/services/ingestion/internal/models"
	"github.com/Pk97-git/CX_aviora/services/ingestion/internal/utils"
	"github.com/Pk97-git/CX_aviora/services/ingestion/pkg/redis"
	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

func main() {
	// 1. Initialize Logger
	utils.InitLogger()
	log.Println("🚀 Starting Ingestion Service...")

	// 2. Load Config
	cfg, err := config.LoadConfig()
	if err != nil {
		log.Fatalf("❌ Failed to load configuration: %v", err)
	}
	log.Printf("🔧 Config Loaded. Port: %s, DB URL Length: %d", cfg.Port, len(cfg.DatabaseURL))

	// 3. Connect to Database
	log.Println("🔌 Connecting to Database...")
	db, err := database.Connect(cfg.DatabaseURL)
	if err != nil {
		log.Fatalf("❌ Failed to connect to database: %v", err)
	}

	// 4. Auto-Migrate Ticket Model (Verify Schema)
	if err := db.AutoMigrate(&models.Ticket{}); err != nil {
		log.Fatalf("❌ Failed to migrate database: %v", err)
	}
	log.Println("✅ Database Schema Verified")

	// 5. Connect to Redis with Circuit Breaker
	timeout := time.Duration(cfg.CircuitBreakerTimeout) * time.Second
	rdb, err := redis.NewCircuitBreakerClient(
		cfg.RedisURL,
		uint32(cfg.CircuitBreakerThreshold),
		timeout,
	)
	if err != nil {
		log.Fatalf("❌ Failed to connect to Redis: %v", err)
	}
	defer rdb.Close()

	log.Println("✨ Ingestion Service Core Initialized Successfully!")

	// 6. Setup HTTP Server
	r := gin.Default()

	// Apply global middleware
	r.Use(middleware.MetricsMiddleware())

	// Create rate limiter
	rateLimiter := middleware.NewRateLimiter(cfg.RateLimitPerMinute)
	r.Use(rateLimiter.Middleware())

	// Health Check
	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "ok", "service": "ingestion"})
	})

	// Prometheus Metrics Endpoint
	r.GET("/metrics", gin.WrapH(promhttp.Handler()))

	// Initialize Handlers
	webhookHandler := handlers.NewWebhookHandler(db, rdb)

	// Register Webhook Routes with Authentication
	api := r.Group("/api/v1/ingest")
	{
		api.POST("/webhook/freshdesk",
			middleware.ValidateFreshdeskSignature(cfg.FreshdeskWebhookSecret),
			webhookHandler.HandleFreshdeskWebhook,
		)
		api.POST("/webhook/zendesk",
			middleware.ValidateZendeskSignature(cfg.ZendeskWebhookSecret),
			webhookHandler.HandleZendeskWebhook,
		)
	}

	// 7. Start Server
	log.Printf("👂 Listening on port %s...", cfg.Port)
	log.Printf("📊 Metrics available at http://localhost:%s/metrics", cfg.Port)
	log.Printf("🔒 Webhook signature validation: %s",
		map[bool]string{true: "ENABLED", false: "DISABLED (dev mode)"}[cfg.FreshdeskWebhookSecret != ""])
	log.Printf("⏱️  Rate limit: %d requests/minute", cfg.RateLimitPerMinute)

	if err := r.Run(":" + cfg.Port); err != nil {
		log.Fatalf("❌ Failed to start server: %v", err)
	}
}
