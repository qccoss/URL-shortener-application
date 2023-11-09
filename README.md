# URL Shortener Application

This is a simple URL shortener service similar to TinyURL or Bit.ly, which allows you to shorten long URLs and provides usage statistics for each shortened URL.

## Features

- Shorten URLs with optional custom shortcodes
- Retrieve original URLs using shortcodes
- View statistics for each shortened URL, such as creation date, last accessed date, and access count

## Installation

To set up the URL Shortener Application on your local machine, follow these steps:

1. Clone the repository: https://github.com/qccoss/URL-shortener-application.git
3. Navigate to the project directory.
4. Install the required dependencies:
```pip install -r requirements.txt```


## Usage

To start the application, run the following command in the terminal:
```flask run```

### Shortening a URL

Send a POST request to `/shorten` with a JSON payload containing the URL:

```json
{
  "url": "https://www.example.com/"
}
```
### Redirecting to the Original URL
Access the original URL by visiting `/<shortcode>` in your browser or sending a GET request.

### Getting URL Statistics
Send a GET request to `/<shortcode>/stats` to retrieve statistics about the URL associated with the shortcode.

