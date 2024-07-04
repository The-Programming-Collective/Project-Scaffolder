FROM golang:1.22.3-bullseye as builder

WORKDIR /src
COPY . .
RUN go mod download
RUN go mod verify
RUN CGO_ENABLED=1 GOOS=linux go build -o /app -a -ldflags '-linkmode external -extldflags "-static"' .

FROM scratch

COPY --from=builder /app /app

EXPOSE 3000

ENTRYPOINT ["/app"]