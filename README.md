# REDDITOR

## TLDR

This works one of 3 ways:

1.  **As a single script**: You can run the [`main.py`](./src/redditor/main.py) file directly to execute the script in shell and see the output. All logs will be in the [`logs`](./logs/) directory.
2.  **As a server**: You can run the [`server.py`](./src/redditor/server/server.py) file to start a web server that listens renders a page to make requests to the Reddit API.
    - The server will be available at `http://localhost:8045/` by default.
    <!-- - You can use the `/fetch_posts` endpoint to make requests to the Reddit API. -->
3.  **As a Docker container**: You can build and run the project as a Docker container.

    - The Docker container will run the server and expose it on port 8045 by default.
    - In [`server.py`](./src/redditor/server/server.py), you should change the redditor lib import from the path to the absolute path to use it in Docker. (HOTFIX)

      ```python
      from redditor.main import create_client, fetch_latest_posts  # uncomment to use in standalone mode
      from ..main import create_client, fetch_latest_posts # uncomment to use in Docker
      ```

## Setup

1. **From Reddit:**

   - Create a Reddit app at [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
   - Select "script" as the app type.
   - Copy the `client_id` and `client_secret` values.

2. **Configure Environment Variables:**

   - Copy the `.env.example` file to `.env` and fill in the required values:
     - `REDDIT_CLIENT_ID`: Your Reddit app's client ID.
     - `REDDIT_CLIENT_SECRET`: Your Reddit app's client secret.
     - `REDDIT_USER_AGENT`: A unique user agent string for your app.
     - `REDDIT_USERNAME`: Your Reddit username.
     - `REDDIT_PASSWORD`: Your Reddit password.

3. **Install Required Packages:**

   - Ensure you have Python 3.10 or higher installed.
   - [Optional] Create a virtual environment:

     ```bash
     python -m venv venv
     source venv/bin/activate # On Windows use `venv\Scripts\activate`
     ```

   - [Optional] Use `uv` for package management:`pip install uv`

   - Install the required packages:

     ```bash
     pip install -r requirements.txt # using pip
     uv pip install -r requirements.txt # using uv
     ```

4. **Run the Application:**

   - Using Python:

     ```bash
     python src/redditor/main.py # for simple run
     python src/redditor/server/server.py # for server run
     ```

   - Using Docker:

     ```bash
     docker build --tag <YOUR_IMAGE_NAME> .
     docker run --env-file .env -p 8045:8045 <YOUR_IMAGE_NAME>
     ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
