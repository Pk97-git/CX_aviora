package handlers

import (
	"net/http"

	"github.com/Pk97-git/CX_aviora/services/ingestion/internal/database"
	"github.com/Pk97-git/CX_aviora/services/ingestion/internal/services"
	"github.com/Pk97-git/CX_aviora/services/ingestion/pkg/redis"
	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

type WebhookHandler struct {
	DB    *gorm.DB
	Redis *redis.CircuitBreakerClient
}

func NewWebhookHandler(db *gorm.DB, rdb *redis.CircuitBreakerClient) *WebhookHandler {
	return &WebhookHandler{
		DB:    db,
		Redis: rdb,
	}
}

// HandleFreshdeskWebhook processes incoming Freshdesk webhooks
func (h *WebhookHandler) HandleFreshdeskWebhook(c *gin.Context) {
	var payload map[string]interface{}
	if err := c.BindJSON(&payload); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid JSON payload"})
		return
	}

	// Normalize Ticket
	ticket, err := services.NormalizeFreshdeskTicket(payload)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Failed to normalize ticket: " + err.Error()})
		return
	}

	// Check for existing ticket (idempotency)
	existing, err := database.GetTicketByExternalID(h.DB, ticket.ExternalSource, ticket.ExternalID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Database error"})
		return
	}

	if existing != nil {
		// Ticket already exists, return existing ID
		c.JSON(http.StatusOK, gin.H{
			"status":    "already_exists",
			"ticket_id": existing.ID,
			"message":   "Ticket already processed (idempotent)",
		})
		return
	}

	// Save to Database
	if err := database.CreateTicket(h.DB, &ticket); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to save ticket"})
		return
	}

	// Publish to Redis (with circuit breaker protection)
	ctx := c.Request.Context()
	if err := h.Redis.Publish(ctx, "tickets:new", ticket); err != nil {
		// Circuit breaker handled the error, log but continue
		c.JSON(http.StatusAccepted, gin.H{
			"status":    "saved_but_publish_failed",
			"ticket_id": ticket.ID,
			"error":     err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status":    "received",
		"ticket_id": ticket.ID,
	})
}

// HandleZendeskWebhook processes incoming Zendesk webhooks
func (h *WebhookHandler) HandleZendeskWebhook(c *gin.Context) {
	var payload map[string]interface{}
	if err := c.BindJSON(&payload); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid JSON payload"})
		return
	}

	// Normalize Ticket
	ticket, err := services.NormalizeZendeskTicket(payload)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Failed to normalize ticket: " + err.Error()})
		return
	}

	// Check for existing ticket (idempotency)
	existing, err := database.GetTicketByExternalID(h.DB, ticket.ExternalSource, ticket.ExternalID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Database error"})
		return
	}

	if existing != nil {
		// Ticket already exists, return existing ID
		c.JSON(http.StatusOK, gin.H{
			"status":    "already_exists",
			"ticket_id": existing.ID,
			"message":   "Ticket already processed (idempotent)",
		})
		return
	}

	// Save to Database
	if err := database.CreateTicket(h.DB, &ticket); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to save ticket"})
		return
	}

	// Publish to Redis (with circuit breaker protection)
	ctx := c.Request.Context()
	if err := h.Redis.Publish(ctx, "tickets:new", ticket); err != nil {
		// Circuit breaker handled the error, log but continue
		c.JSON(http.StatusAccepted, gin.H{
			"status":    "saved_but_publish_failed",
			"ticket_id": ticket.ID,
			"error":     err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status":    "received",
		"ticket_id": ticket.ID,
	})
}
