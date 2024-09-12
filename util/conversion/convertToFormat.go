package conversion

import (
	"AletheiaDesktop/search"
	"os/exec"
	"path"
	"strings"
)

func ConvertToFormat(targetFormat string, book search.Book) bool {
	existingFilepath := book.Filepath
	extension := path.Ext(existingFilepath)
	outfile := existingFilepath[0:len(existingFilepath)-len(extension)] + "." + strings.ToLower(targetFormat)
	cmd := exec.Command("ebook-convert", book.Filepath, outfile)
	if err := cmd.Run(); err != nil {
		return false
	}
	return true
}
