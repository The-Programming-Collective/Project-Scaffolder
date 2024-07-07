FROM golang:1.22.4-bullseye as builder

WORKDIR /src
COPY . .
RUN sh ./get_dependencies.sh
RUN go mod download
RUN go mod verify
RUN CGO_ENABLED=1 GOOS=linux go build -o /app -a -ldflags '-linkmode external -extldflags "-static"' .

FROM scratch

COPY --from=builder /app /app

EXPOSE 5000

ENTRYPOINT ["/app"]
