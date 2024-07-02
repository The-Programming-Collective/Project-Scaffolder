package utils

import (
	"fmt"
)

// This is a sample utility function that will be used in the application
// This function will take a string as a parameter and return a string
// The function will return the input string with a prefix
func SampleUtil(input string) string {
	return fmt.Sprintf("Prefix: %s", input)
}
