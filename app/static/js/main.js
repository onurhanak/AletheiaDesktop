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


async function populateResults() {
  document.getElementById('loader').style.display = 'block'; // Show loader
  const searchType = document.getElementById('searchType').value;
  const searchQuery = document.getElementById('searchQuery').value;

  const results = await eel.search_books(searchQuery, searchType)();
  document.getElementById('loader').style.display = 'none'; // Hide loader

  const resultsContainer = document.getElementById('results-grid');
  resultsContainer.innerHTML = ''; // Clear previous results

  if (Array.isArray(results)) {
    results.forEach(item => {
      resultsContainer.innerHTML += `
                    <div class="col">
                        <div class="card h-100">
                            <div class="card-background" style="background-image: url('${item.Cover}');"></div>
                            <div class="card-body">
                                <h5 class="card-title">${item.Title}</h5>
                                <p class="card-text">Author: ${item.Author}<br>Publisher: ${item.Publisher}<br>Year: ${item.Year}<br>Filetype: ${item.Extension}</p>
                                <a href="#" onclick='downloadBook(${JSON.stringify(item)})' class="fa fa-download"></a>
                                <a href="#" onclick='favoriteBook(${JSON.stringify(item)})' class="fa fa-heart"></a>

                            </div>
                        </div>
                    </div>
                `;
    });
  } else {
    console.error('Received data is not an array:', results);
  }
}

async function downloadBook(book) {
  eel.download_book_thread(book)(response => {
    showNotification("Download started: " + book.Title + " by " + book.Author); // Use custom notification
  });
}


async function favoriteBook(book) {
  eel.favorite_book(book)(response => {
    showNotification(book.Title + " by " + book.Author + " is added to your favorites."); // Use custom notification
  });
}

eel.expose(showNotification);
function showNotification(message) {
  console
  const notificationBox = document.getElementById('notificationBox');
  const messagePara = document.getElementById('notificationMessage');
  messagePara.textContent = message; // Set the text message
  notificationBox.style.display = 'block'; // Show the notification box
}

function closeNotification() {
  const notificationBox = document.getElementById('notificationBox');
  notificationBox.style.display = 'none'; // Hide the notification box
}


async function populateLibrary() {

  const results = await eel.return_library_elements(1)();

  const resultsContainer = document.getElementById('results-grid');
  resultsContainer.innerHTML = ''; //clear

  if (Array.isArray(results)) {
    results.forEach(item => {
      resultsContainer.innerHTML += `
                    <div class="col">
                        <div class="card h-100" >
                            <div class="card-background" style="background-image: url('${item.Cover}');"></div>
                            <div class="card-body" onclick='openBook("${item.Title.replace(/"/g, "&quot;")}")'>
                                <h5 class="card-title">${item.Title}</h5>
                                <p class="card-text">Author: ${item.Author}<br>Publisher: ${item.Publisher}<br>Year: ${item.Year}<br>Filetype: ${item.Extension}</p>
                                <a href="#" onclick='openBook("${item.Title.replace(/"/g, "&quot;")}")' class="fa fa-external-link"></a>

                              </div>
                        </div>
                    </div>
                `;
    });
  } else {
    console.error('Received data is not an array:', results);
  }
}
populateLibrary();

function openBook(book) {
  eel.open_file_with_default_program(book)
}

eel.expose(saveSettings);
function saveSettings() {
    var downloadPath = document.getElementById('downloadLocation').value;
    eel.save_settings(downloadPath);
    location.reload();
}
function askForDirectory() {
    eel.select_directory();
}

async function getLibraryLocation() {
    const libraryLocation = await eel.get_library_location()();
    document.querySelector('label[for="downloadLocation"]').textContent = `Download Location: ${libraryLocation}`;
}

eel.expose(showNotification);
function showNotification(message) {
  console
  const notificationBox = document.getElementById('notificationBox');
  const messagePara = document.getElementById('notificationMessage');
  messagePara.textContent = message; // Set the text message
  notificationBox.style.display = 'block'; // Show the notification box
}

function closeNotification() {
  const notificationBox = document.getElementById('notificationBox');
  notificationBox.style.display = 'none'; // Hide the notification box
}


async function populateFavorites() {

  const results = await eel.return_library_elements(0)();

  const resultsContainer = document.getElementById('results-grid');
  resultsContainer.innerHTML = ''; //clear

  if (Array.isArray(results)) {
    results.forEach(item => {
      resultsContainer.innerHTML += `
                    <div class="col">
                        <div class="card h-100">
                            <div class="card-background" style="background-image: url('${item.Cover}');"></div>
                            <div class="card-body">
                                <h5 class="card-title">${item.Title}</h5>
                                <p class="card-text">Author: ${item.Author}<br>Publisher: ${item.Publisher}<br>Year: ${item.Year}<br>Filetype: ${item.Extension}</p>
                                <a href="#" onclick='downloadBook(${JSON.stringify(item)})' class="fa fa-download"></a>

                            </div>
                        </div>
                    </div>
                `;
    });
  } else {
    console.error('Received data is not an array:', results);
  }
}
populateFavorites();

async function downloadBook(book) {
  eel.download_book_thread(book)(response => {
    showNotification("Download started: " + book.Title + " by " + book.Author); // Use custom notification
  });
}