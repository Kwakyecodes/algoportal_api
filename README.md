# Code Fetching API

This Django API is designed to fetch code snippets from the internet based on user queries or error messages. It automates the process of searching for code, providing quicker and less laborious results by scraping multiple websites and returning the most relevant code snippets.

## Features

- **Fetch Code Snippets**: Given a query, the API scrapes websites like GeeksforGeeks, Stack Overflow, and W3Schools to find relevant code snippets.
- **Fetch Debugging Solutions**: Given an error message, the API scrapes Stack Overflow to find related debugging solutions.
- **Logs API Usage**: All API usage is logged into a database, including the endpoint called, the status of the call, the query, and the reason for failure (if any).

## Installation

1. **Clone the Repository**:
    ```sh
    git clone <repository-url>
    cd code-fetching-api
    ```

2. **Set Up the Virtual Environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the Required Packages**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run Migrations**:
    ```sh
    python manage.py migrate
    ```

5. **Start the Server**:
    ```sh
    python manage.py runserver
    ```

## Endpoints

### Fetch Code

**Endpoint**: `/api/fetch_code/`  
**Method**: `POST`  
**Accepts**: `application/json`  
**Request Body**:
```json
{
    "query": "sorting a dictionary using the values of the dictionary in descending order python code implementation"
}
```
**Response**: A JSON array of code snippets related to the query.

### Fetch Debugger

**Endpoint**: `/api/fetch_debugger/`  
**Method**: `POST`  
**Accepts**: `application/json`  
**Request Body**:
```json
{
    "error": "! [rejected] main -> main (fetch first)"
}
```
**Response**: A JSON array of debugging solutions related to the error message.

## Project Structure

- **views.py**: Contains the main logic for handling API requests.
- **models.py**: Contains the `Records` model for logging API usage.
- **scrappers/**: Contains the scraping logic for different websites (GeeksforGeeks, Stack Overflow, W3Schools).
- **urls.py**: Defines the URL patterns for the API endpoints.

## Helper Functions

- **log_usage(call, status='Fail', query='Not given', reason='NA')**: Logs API usage into the database.
- **preference(solution, query)**: Scores solutions to determine which should appear first based on relevance.
- **get_codes(query)**: Fetches code snippets from various sites and returns them sorted by relevance.

## Usage

### Fetch Code Example

To fetch code snippets related to a specific query:
```sh
curl -X POST http://127.0.0.1:8000/api/fetch_code/ -H "Content-Type: application/json" -d '{"query": "sorting a dictionary using the values of the dictionary in descending order python code implementation"}'
```

### Fetch Debugger Example

To fetch debugging solutions related to a specific error message:
```sh
curl -X POST http://127.0.0.1:8000/api/fetch_debugger/ -H "Content-Type: application/json" -d '{"error": "! [rejected] main -> main (fetch first)"}'
```

## Future Enhancements

- Add more scrapers for additional websites.
- Implement caching to reduce the load on external websites and improve response times.
- Add more sophisticated query analysis to improve the relevance of returned code snippets.

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.