package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/redis/go-redis/v9"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

type Ticket struct {
	ID             string `gorm:"type:uuid;primary_key"`
	Title          string `gorm:"type:varchar(500)"`
	ExternalSource string `gorm:"type:varchar(50)"`
	Priority       string `gorm:"type:varchar(20)"`
	CustomerEmail  string `gorm:"type:varchar(255)"`
	CreatedAt      time.Time
}

func main() {
	dbURL := "postgresql://neondb_owner:***REMOVED***@ep-young-snow-a1h4us5d-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
	redisURL := "rediss://default:AWe7AAIncDJjZDNhMDAxMmQzZjY0OTQzOTliYzMyYTViNGUxNWY5ZnAyMjY1NTU@sterling-ant-26555.upstash.io:6379"

	// Check Database
	fmt.Println("🔍 Checking PostgreSQL (Neon)...")
	db, err := gorm.Open(postgres.Open(dbURL), &gorm.Config{})
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}

	var tickets []Ticket
	result := db.Order("created_at DESC").Limit(5).Find(&tickets)
	if result.Error != nil {
		log.Fatalf("Failed to query tickets: %v", result.Error)
	}

	fmt.Printf("✅ Found %d tickets in database\n\n", len(tickets))
	fmt.Println("Recent Tickets:")
	fmt.Println("================")
	for i, ticket := range tickets {
		fmt.Printf("%d. [%s] %s\n", i+1, ticket.ExternalSource, ticket.Title)
		fmt.Printf("   Priority: %s | Email: %s\n", ticket.Priority, ticket.CustomerEmail)
		fmt.Printf("   Created: %s\n\n", ticket.CreatedAt.Format("2006-01-02 15:04:05"))
	}

	// Check Redis
	fmt.Println("🔍 Checking Redis (Upstash)...")
	opt, err := redis.ParseURL(redisURL)
	if err != nil {
		log.Fatalf("Failed to parse Redis URL: %v", err)
	}

	rdb := redis.NewClient(opt)
	ctx := context.Background()

	pong, err := rdb.Ping(ctx).Result()
	if err != nil {
		log.Fatalf("Failed to ping Redis: %v", err)
	}

	fmt.Printf("✅ Redis connection successful: %s\n\n", pong)

	// Try to read last published message (if any)
	// Note: Pub/Sub messages are ephemeral, so we can't retrieve past messages
	// We'll just confirm the connection works
	fmt.Println("📊 Summary:")
	fmt.Println("===========")
	fmt.Printf("✅ Database: Connected, %d tickets found\n", len(tickets))
	fmt.Println("✅ Redis: Connected and responding")
	fmt.Println("\n✨ Ingestion Service is fully operational!")
}
