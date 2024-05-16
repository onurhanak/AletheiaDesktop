
eel.expose(showNotification);
function showNotification(message) {
  const notificationBox = document.getElementById('notificationBox');
  const messagePara = document.getElementById('notificationMessage');
  messagePara.textContent = message; // Set the text message
  notificationBox.style.display = 'block'; // Show the notification box
}

function closeNotification() {
  const notificationBox = document.getElementById('notificationBox');
  notificationBox.style.display = 'none'; // Hide the notification box
}

function deleteBook(bookTitle) {
    eel.delete_book(bookTitle);
    location.reload();
}

function unfavoriteBook(bookTitle) {
  eel.unfavorite_book(bookTitle);
  location.reload();
}