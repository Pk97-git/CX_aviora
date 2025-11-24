package middleware

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"io"
	"net/http"

	"github.com/gin-gonic/gin"
)

// ValidateFreshdeskSignature validates Freshdesk webhook HMAC signature
func ValidateFreshdeskSignature(secret string) gin.HandlerFunc {
	return func(c *gin.Context) {
		if secret == "" {
			// No secret configured, skip validation (development mode)
			c.Next()
			return
		}

		signature := c.GetHeader("X-Freshdesk-Signature")
		if signature == "" {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Missing X-Freshdesk-Signature header"})
			c.Abort()
			return
		}

		// Read body
		body, err := io.ReadAll(c.Request.Body)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Failed to read request body"})
			c.Abort()
			return
		}

		// Restore body for downstream handlers
		c.Request.Body = io.NopCloser(io.Reader(c.Request.Body))

		// Compute HMAC
		mac := hmac.New(sha256.New, []byte(secret))
		mac.Write(body)
		expectedSignature := hex.EncodeToString(mac.Sum(nil))

		if !hmac.Equal([]byte(signature), []byte(expectedSignature)) {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid signature"})
			c.Abort()
			return
		}

		c.Next()
	}
}

// ValidateZendeskSignature validates Zendesk webhook Basic Auth
func ValidateZendeskSignature(secret string) gin.HandlerFunc {
	return func(c *gin.Context) {
		if secret == "" {
			// No secret configured, skip validation (development mode)
			c.Next()
			return
		}

		// Zendesk uses HTTP Basic Auth with username and password
		// The secret is typically in the format "username:password"
		auth := c.GetHeader("Authorization")
		if auth == "" {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Missing Authorization header"})
			c.Abort()
			return
		}

		// Expected format: "Basic base64(username:password)"
		expectedAuth := "Basic " + base64.StdEncoding.EncodeToString([]byte(secret))

		if auth != expectedAuth {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid credentials"})
			c.Abort()
			return
		}

		c.Next()
	}
}
