package config

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
)

func ReadConfigFile() (map[string]string, error) {

	configPath, configPathConstructionErr := ConstructConfigLocation()

	if configPathConstructionErr != nil {
		log.Fatalln(configPathConstructionErr.Error())
	}

	userConfigContent := map[string]string{}
	file, readFileErr := os.ReadFile(configPath)
	if readFileErr != nil {
		log.Fatalln(fmt.Errorf("Read config file error: %v", readFileErr))
		return nil, readFileErr
	}

	unmarshalErr := json.Unmarshal(file, &userConfigContent)
	if unmarshalErr != nil {
		log.Println(fmt.Sprintf("Creating a new config file. Unmarshal config file error: %v", unmarshalErr))
		userConfigContent = InitializeConfig()
		return userConfigContent, unmarshalErr
	}
	return userConfigContent, nil
}
