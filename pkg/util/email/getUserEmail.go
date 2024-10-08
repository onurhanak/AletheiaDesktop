package email

import (
	"AletheiaDesktop/pkg/util/config"
	"fmt"
	"log"
)

func GetUserEmail() string {
	existingUserConfig, configErr := config.ReadConfigFile()

	if configErr != nil {
		log.Println(fmt.Sprintf("Error reading config file: %s", configErr))
	}
	userEmail := existingUserConfig["userEmail"]
	if userEmail == "" {
		return "Your email address"
	}
	userEmailText := fmt.Sprintf("%s", userEmail)
	return userEmailText
}
