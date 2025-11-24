# Build Stage
FROM golang:1.24-alpine AS builder

WORKDIR /app

# Install git for fetching dependencies
RUN apk add --no-cache git

# Copy go mod and sum files
COPY go.mod go.sum ./

# Download all dependencies. Dependencies will be cached if the go.mod and go.sum files are not changed
RUN go mod download

# Copy the source from the current directory to the Working Directory inside the container
COPY . .

# Tidy dependencies
RUN go mod tidy

# Build the Go app
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o ingestion-service ./cmd/server

# Run Stage
FROM alpine:latest  

WORKDIR /root/

# Install CA certificates for SSL connections
RUN apk add --no-cache ca-certificates

# Copy the Pre-built binary from the previous stage
COPY --from=builder /app/ingestion-service .


# Expose port 8080 to the outside world
EXPOSE 8080

# Command to run the executable
CMD ["./ingestion-service"]
