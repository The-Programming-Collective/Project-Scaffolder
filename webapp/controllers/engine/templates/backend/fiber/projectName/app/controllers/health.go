package controllers

import (
	"github.com/gofiber/fiber/v2"
)

// To create a new route, we need to create a new function that will be called by the router
// This function will take a fiber.Ctx as a parameter and return an error
// The fiber.Ctx is the context of the request, it contains all the information about the request
// The error will be used to return an error if something goes wrong
// Function to check the health of the application
func Health(c *fiber.Ctx) error {
	// Return a message to the user
	return c.SendString("App is running!")
}
