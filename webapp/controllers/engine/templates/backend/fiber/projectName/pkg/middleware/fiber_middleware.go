package middleware

// Add the necessary imports
import (
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/logger"

)

// FiberMiddleware is a function that will be called by the router}
func FiberMiddleware(app *fiber.App) {
	// Add middleware to the application
	// The order of the middleware is important
	// The middleware will be executed in the order they are added
	// The cors middleware will add the necessary headers to allow cross-origin requests
	// The logger middleware will log the requests to the console
	app.Use(cors.New(), logger.New())
}
