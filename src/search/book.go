package search

import (
	"AletheiaDesktop/src/util/cache"
	"AletheiaDesktop/src/util/config"
	"fmt"
	"github.com/onurhanak/libgenapi"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

type Book struct {
	libgenapi.Book // extend libgenapi.Book
	Filename       string
	Filepath       string
	CoverPath      string
	Downloaded     bool
	DownloadFolder string // for tests
}

func (book *Book) ConstructFilename() string {
	filename := fmt.Sprintf("%s - %s.%s", book.Author, book.Title, book.Extension)
	// sanitize filename for Windows
	filename = strings.ReplaceAll(filename, "/", "_")
	filename = strings.ReplaceAll(filename, "\\", "_")
	filename = strings.ReplaceAll(filename, ":", "_")
	filename = strings.ReplaceAll(filename, "*", "_")
	filename = strings.ReplaceAll(filename, "?", "_")
	filename = strings.ReplaceAll(filename, "\"", "_")
	filename = strings.ReplaceAll(filename, "<", "_")
	filename = strings.ReplaceAll(filename, ">", "_")
	filename = strings.ReplaceAll(filename, "|", "_")

	filename = strings.TrimSpace(filename)
	book.Filename = filename
	return filename
}

func (book *Book) ConstructFilepath() string {
	downloadPath := config.GetCurrentDownloadFolder()
	filepath := filepath.Join(downloadPath, book.ConstructFilename())
	book.Filepath = filepath
	return filepath
}

func (book *Book) ConstructCoverPath() string {
	aletheiaCachePath := cache.GetAletheiaCache()
	book.CoverPath = filepath.Join(aletheiaCachePath, book.ID)
	return book.CoverPath
}

func (book *Book) SaveToFile(response *http.Response) bool {
	// create the file
	out, err := os.Create(book.Filepath)
	if err != nil {
		log.Println(fmt.Sprintf("Could not create a file for the book: %s", err))
		return false
	}
	defer out.Close()

	// copy the contents to the
	// newly created file
	_, err = io.Copy(out, response.Body)
	if err != nil {
		log.Println(err)
		return false
	}

	return true
}

func (book *Book) Download() bool {
	book.ConstructFilepath()
	response, err := http.Get(book.DownloadLink)
	if err != nil {
		log.Println("Could not download book")
	}
	defer response.Body.Close()

	if response.StatusCode != http.StatusOK {
		log.Println(fmt.Errorf("failed to download file: %s", response.Status))
		return false
	}

	book.Downloaded = book.SaveToFile(response)

	return book.Downloaded
}
