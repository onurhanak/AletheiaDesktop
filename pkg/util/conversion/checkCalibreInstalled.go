package conversion

import (
	"fmt"
	"log"
	"os/exec"
)

// TODO
// check for windows
// if windows, suppress powershell

func CheckCalibreInstalled() bool {
	cmd := exec.Command("ebook-convert", "--version")
	if err := cmd.Run(); err != nil {
		log.Println(fmt.Sprintf("Calibre is not installed."))
		return false
	}
	return true
}
