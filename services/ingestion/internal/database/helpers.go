package database

import (
	"time"

	"github.com/Pk97-git/CX_aviora/services/ingestion/internal/metrics"
	"github.com/Pk97-git/CX_aviora/services/ingestion/internal/models"
	"gorm.io/gorm"
)

// GetTicketByExternalID retrieves a ticket by external source and ID (for idempotency)
func GetTicketByExternalID(db *gorm.DB, externalSource, externalID string) (*models.Ticket, error) {
	start := time.Now()
	var ticket models.Ticket

	err := db.Where("external_source = ? AND external_id = ?", externalSource, externalID).First(&ticket).Error

	duration := time.Since(start).Seconds()
	status := "success"
	if err != nil {
		if err == gorm.ErrRecordNotFound {
			status = "not_found"
		} else {
			status = "error"
		}
	}

	metrics.DbOperationsTotal.WithLabelValues("get_by_external_id", status).Inc()
	metrics.DbOperationDuration.WithLabelValues("get_by_external_id").Observe(duration)

	if err == gorm.ErrRecordNotFound {
		return nil, nil // Not an error, just not found
	}

	return &ticket, err
}

// CreateTicket creates a new ticket with metrics
func CreateTicket(db *gorm.DB, ticket *models.Ticket) error {
	start := time.Now()
	err := db.Create(ticket).Error
	duration := time.Since(start).Seconds()

	status := "success"
	if err != nil {
		status = "error"
	}

	metrics.DbOperationsTotal.WithLabelValues("create_ticket", status).Inc()
	metrics.DbOperationDuration.WithLabelValues("create_ticket").Observe(duration)

	return err
}
