package email

import (
	"AletheiaDesktop/internal/models"
	"github.com/wneessen/go-mail"
	"log"
)

func composeSendMessage(userEmail string, userPassword string, book models.Book) bool {
	m := mail.NewMsg()
	if err := m.From(userEmail); err != nil {
		log.Println("failed to set From address: %s", err)
		return false
	}
	if err := m.To(userEmail); err != nil {
		log.Println("failed to set To address: %s", err)
		return false
	}
	m.Subject(book.Title)
	m.SetBodyString(mail.TypeTextPlain, "")
	m.AttachFile(book.Filepath)
	c, err := mail.NewClient("smtp.gmail.com", mail.WithPort(25), mail.WithSMTPAuth(mail.SMTPAuthPlain),
		mail.WithUsername(userEmail), mail.WithPassword(userPassword))
	if err != nil {
		log.Println("failed to create mail client: %s", err)
		return false
	}
	if err := c.DialAndSend(m); err != nil {
		log.Println("failed to send mail: %s", err)
		return false
	}
	return true
}

func SendBookEmail(book models.Book) bool {
	userEmail := GetUserEmail()
	userPassword := GetUserPassword()
	emailSent := composeSendMessage(userEmail, userPassword, book)
	return emailSent
}
