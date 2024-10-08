package config

import (
	"log"
	"os"
)

func InitializeConfig() map[string]string {
	// add checks
	initialDownloadDir, err := os.UserHomeDir()

	if err != nil {
		log.Fatalln("Could not get home directory")
		panic(err)
	}

	initialUserConfig := map[string]string{
		"downloadLocation": initialDownloadDir,
		"userEmail":        "",
		"userPassword":     "",
	}

	fileWriteErr := WriteConfigFile(initialUserConfig)

	if fileWriteErr != nil {
		log.Println("Unable to write config file")
		panic(fileWriteErr)
	}

	return initialUserConfig
}
