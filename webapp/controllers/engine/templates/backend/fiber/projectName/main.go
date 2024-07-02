package main

import (
	"github.com/gofiber/fiber/v2"
	"project-name/pkg/router"
	"project-name/pkg/middleware"
)

func main() {

	app := fiber.New()

	// Add the middleware to the application
	middleware.FiberMiddleware(app)

	// Add the routes to the application
	router.PublicRoutes(app)

	// Add default route
	app.Get("/", func(c *fiber.Ctx) error {
		return c.SendString("Hello user! Test the health of the application by visiting /api/health")
	})

	// Start the application on port 3000
	app.Listen(":3000")

}
