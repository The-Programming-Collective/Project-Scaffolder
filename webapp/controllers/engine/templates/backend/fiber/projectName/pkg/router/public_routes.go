package router

import (
	"github.com/gofiber/fiber/v2";
	"project-name/app/controllers"
)


func PublicRoutes(app *fiber.App) {

	// Create a new route group
	route := app.Group("/api")

	// Define the route for the health check
	// The first parameter is the path of the route
	// The second parameter is the function that will be called when the route is matched
	// The method Get is used to match GET requests
	route.Get("/health", controllers.Health)
}
