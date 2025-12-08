package models

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type Ticket struct {
	ID             uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	TenantID       uuid.UUID      `gorm:"type:uuid;not null" json:"tenant_id"`
	ExternalID     string         `gorm:"type:varchar(255)" json:"external_id"`
	ExternalSource string         `gorm:"type:varchar(100)" json:"external_source"`
	Title          string         `gorm:"type:varchar(500)" json:"title"`
	Description    string         `gorm:"type:text" json:"description"`
	Status         string         `gorm:"type:varchar(50);default:'open'" json:"status"`
	Priority       string         `gorm:"type:varchar(50);default:'medium'" json:"priority"`
	Category       string         `gorm:"type:varchar(100)" json:"category"`
	Subcategory    string         `gorm:"type:varchar(100)" json:"subcategory"`
	Intent         string         `gorm:"type:varchar(100)" json:"intent"`
	Sentiment      string         `gorm:"type:varchar(50)" json:"sentiment"`
	UrgencyScore   float64        `gorm:"type:decimal(3,2)" json:"urgency_score"`
	Entities       map[string]any `gorm:"type:jsonb;serializer:json" json:"entities"`
	AssignedTo     *uuid.UUID     `gorm:"type:uuid" json:"assigned_to"`
	CustomerID     *uuid.UUID     `gorm:"type:uuid" json:"customer_id"`
	CustomerEmail  string         `gorm:"type:varchar(255)" json:"customer_email"`
	CustomerName   string         `gorm:"type:varchar(255)" json:"customer_name"`
	SlaDueAt       *time.Time     `json:"sla_due_at"`
	SlaBreached    bool           `gorm:"default:false" json:"sla_breached"`
	Tags           []string       `gorm:"type:text[]" json:"tags"`
	Metadata       map[string]any `gorm:"type:jsonb;serializer:json" json:"metadata"`
	CreatedAt      time.Time      `json:"created_at"`
	UpdatedAt      time.Time      `json:"updated_at"`
	ResolvedAt     *time.Time     `json:"resolved_at"`
	ClosedAt       *time.Time     `json:"closed_at"`
}

// BeforeCreate hook to generate UUID if not present (though DB handles it, good to have in app)
func (t *Ticket) BeforeCreate(tx *gorm.DB) (err error) {
	if t.ID == uuid.Nil {
		t.ID = uuid.New()
	}
	return
}
