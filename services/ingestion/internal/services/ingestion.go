package services

import (
	"fmt"
	"time"

	"github.com/Pk97-git/CX_aviora/services/ingestion/internal/models"
	"github.com/google/uuid"
)

// NormalizeFreshdeskTicket converts a Freshdesk payload into a standardized Ticket model
func NormalizeFreshdeskTicket(payload map[string]interface{}) (models.Ticket, error) {
	// Extract ticket data from payload (assuming standard Freshdesk webhook structure)
	// Note: Freshdesk webhooks can be customized. We assume a structure where "freshdesk_webhook" contains the data
	// or the payload itself is the ticket data. Let's assume the payload is the ticket data for simplicity
	// based on common webhook configurations.

	// Helper to safely get string
	getString := func(key string) string {
		if v, ok := payload[key].(string); ok {
			return v
		}
		return ""
	}

	// Helper to safely get int/float and convert to string or use for priority
	// Freshdesk Priority: 1 (Low), 2 (Medium), 3 (High), 4 (Urgent)
	getPriority := func(key string) string {
		val, ok := payload[key]
		if !ok {
			return "medium"
		}
		switch v := val.(type) {
		case float64:
			switch int(v) {
			case 1:
				return "low"
			case 2:
				return "medium"
			case 3:
				return "high"
			case 4:
				return "urgent"
			}
		case string:
			return v
		}
		return "medium"
	}

	ticket := models.Ticket{
		ID:             uuid.New(),
		Title:          getString("subject"),
		Description:    getString("description"),
		ExternalSource: "freshdesk",
		ExternalID:     fmt.Sprintf("%v", payload["id"]), // Handle int or string ID
		Status:         "open",                           // Default to open, map actual status if needed
		Priority:       getPriority("priority"),
		CustomerEmail:  getString("email"),
		CustomerName:   getString("name"),
		CreatedAt:      time.Now(),
		UpdatedAt:      time.Now(),
		Entities:       payload, // Store raw payload
	}

	// If title is empty, try "ticket_subject" (common custom field name)
	if ticket.Title == "" {
		ticket.Title = getString("ticket_subject")
	}
	if ticket.Description == "" {
		ticket.Description = getString("ticket_description")
	}

	return ticket, nil
}

// NormalizeZendeskTicket converts a Zendesk payload into a standardized Ticket model
func NormalizeZendeskTicket(payload map[string]interface{}) (models.Ticket, error) {
	// Zendesk payload usually comes wrapped in "ticket" object, or flat if configured that way.
	// We'll check if "ticket" key exists, otherwise treat root as ticket.
	data := payload
	if t, ok := payload["ticket"].(map[string]interface{}); ok {
		data = t
	}

	getString := func(key string) string {
		if v, ok := data[key].(string); ok {
			return v
		}
		return ""
	}

	ticket := models.Ticket{
		ID:             uuid.New(),
		Title:          getString("subject"),
		Description:    getString("description"),
		ExternalSource: "zendesk",
		ExternalID:     fmt.Sprintf("%v", data["id"]),
		Status:         getString("status"),
		Priority:       getString("priority"),
		CreatedAt:      time.Now(),
		UpdatedAt:      time.Now(),
		Entities:       payload,
	}

	// Handle Requester (often an object)
	if requester, ok := data["requester"].(map[string]interface{}); ok {
		if name, ok := requester["name"].(string); ok {
			ticket.CustomerName = name
		}
		if email, ok := requester["email"].(string); ok {
			ticket.CustomerEmail = email
		}
	}

	return ticket, nil
}
