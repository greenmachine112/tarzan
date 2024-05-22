# Contrabot ![Static Badge](https://img.shields.io/badge/version-v1.0.0-green)
An inverse sentiment trading bot

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/greenmachine112/Contrabot.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Contrabot.git
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
## Usage
**NOTE**: Do not use this model for real trading, as this version suffers from time complexity issues. It averages a comment filter rate of 1.57 +- .4 comments per minute. This program is under active development, and this issue will be fixed in the future.

To connect Contrabot to an Alpaca brokerage account and place trades you must first get a key pair from Alpaca, and Reddit.
1. Alpaca Registry:
    ```bash
    https://app.alpaca.markets/signup
    ```
2. Reddit Registry:
   ```bash
    https://www.reddit.com/wiki/api/
    ```
After obtaining the keys, load them into the ```bash .env ``` file and verify the configurations in ```bash config.py ``` as well as any files that import from it. # Mention which files import
**NOTE**: Unless you want to trade using real funds, make sure the base Alpaca url's host is 'paper-api.alpaca.markets'. This url uses demo funds that do not exist. I highly recommend not giving the bot your funds, unless you'd like to, personally, pay the salary of a Wall Street banker on accident like me.

## Example commands and expected output.

Configuration options.

Optimization and API Call Details

Fetching Comments
To ensure a sufficient number of comments are available for analysis, the fetchComments function fetches submissions from a specified subreddit. It calculates the number of submissions to fetch based on a fraction of the total desired comments (com_limit). For example, if com_limit is set to 1000, the function fetches submissions with a limit of 100 (i.e., com_limit / 10). Each submission can contain multiple comments, leading to a higher total number of comments fetched.

Filtering Comments
The filterComments function processes the fetched comments to filter out those that match specific criteria, such as containing certain keywords, meeting minimum upvote and karma thresholds, and being within a specified time limit. During this process, the process bar will filter signifigantly more than com_limit comments on account that the likelihood of fetching exactly com_limit comments and all of them having at least one keyword is low. To address this, the fetchComments function has been optimized to return exactly the number of comments specified by com_limit. This ensures the progress bar accurately reflects the number of comments being processed. 

Filter Speed
The initial verision(V1.0.0) of the bot has an average filter rate of 1.59 comments per second. This speed is a combination of multiple variables. The first is the speed of the Reddit API, which we can safely geuss is not optimized for high-speed trading. Reddit comments aren't typically valuable to the average trading bot. The second is that the current algorithm uses a linear search. When inputting variations to search, keep in mind the time complexity increases linearly with 'k' variations. This program is under active development, and a parrallel computing or regex style algorithm may be implemented in the future. See filterComments time complexity for more.

API Call Details
When fetching comments, the bot makes API calls to Reddit as follows:

Submission Fetching: The bot makes a single API call to fetch up to 100 submissions. For a com_limit of 1000, this results in 1 API call.

Comments Fetching: Each submission may contain multiple comments. The bot fetches all comments for each submission, which may require additional API calls, especially for submissions with many comments. 
On average, this results in approximately 1 API call/submission.

In total, for a com_limit of 1000, the bot typically makes around 101 API calls (1 for submissions and around 100 for comments).

Handling Rate Limits
Reddit enforces API rate limits for their free tier. Authenticated requests are limited to 60/m. This program is under active development and backoff strategies may be implemented in the future.

Exceeding Rate Limit
The Reddit API's free tier specifies that you may not exceed 60 calls/minute. If the API returns a 429, the program will save what it has filtered to filtered_comments.json, notify the user, and then terminate. You may then analyze the .json file as normal. If you hit the limit, it's safe to wait for a full minute before trying again. This program is under active development, and rate limit monitoring will be implemented in a future release

Time Complexity Summary for Search and Filter

Fetching Comments
Function: fetchComments
Time Complexity: O(N)
Explanation: The function fetches comments from subreddit submissions. The complexity depends on the total number of comments fetched (N).

Filtering Comments
Function: filterComments
Time Complexity: O(i * m * k)
Variables:
i: Number of comments to filter
m: Average length of each comment
k: Number of search term variations
Explination: For each comment, the function converts the text to lowercase (O(m)), and checks if any of the k variations are present (O(k)). Therefore, the time complexity for filtering one comment is O(m * k). Given i comments, the overall complexity is O(i * m * k).

Combined Complexity
The combined time complexity for fetching and filtering is as follows:
Fetching: O(N)
Filtering: O(i * m * k)
Total: O(N + i * m * k)

Explanation of Filter Pass Rate and Keywords
When the number of keywords used in filtering increases, the filter pass rate tends to decrease. This is because each additional keyword introduces another condition that a comment must meet to pass the filter. Therefore, the more keywords you have, the fewer comments will typically match all the criteria.

Impact of Keywords on Filter Pass Rate
More Keywords: As the number of keywords increases, each comment has more conditions to satisfy. This generally leads to a lower filter pass rate because fewer comments will meet all the specified criteria.
Fewer Keywords: With fewer keywords, each comment has fewer conditions to satisfy, which typically leads to a higher filter pass rate because more comments will meet the fewer criteria.
Calculation of Fetch Count with Keywords
The number of comments fetched (F) is calculated to ensure that the desired number of comments (C) is met after filtering. As the number of keywords increases, the estimated filter pass rate (P) will decrease, requiring more comments to be fetched.

Formula
𝐹 = 𝐶/𝑃
Where:
𝐹 = Number of comments to fetch
𝐶 = Number of comments requested by the user
𝑃 = Estimated filter pass rate (inverse relationship with 'k' keywords)

Example
If the user requests 1000 comments and the estimated filter pass rate is 0.2 with a certain number of keywords, the program will fetch:
𝐹 = 1000/0.2 = 500
If the number of keywords increases and the filter pass rate drops to 0.1, the program will fetch:
𝐹 = 1000/0.1 = 1000

.json Formatting
The .json file generated from the fetched and filtered comments can be quite large. Here are some important points to understand about the structure and content of this file:

File Size Insight: The .json file can have thousands of lines due to the detailed structure of each comment.
Comment Breakdown: Each comment occupies multiple lines in the .json file. Typically, a single comment is represented by 6 lines, including metadata like timestamps, karma, upvotes, and comment text.
Estimating Total Comments: To quickly estimate the total number of comments in your .json file, you can use the following approximation:

totalComments = linesInJson / 6

For instance, a .json file with 6,000 lines would approximately contain:

totalComments = 6000 / 6 = 1000

Profanity 
Comments fetched from subreddits, especially from communities like r/wallstreetbets, may contain profane or offensive language. These communities are known for their unfiltered and often crude discussions. They refer to themselves as 'apes', which gives you an idea of their vernacular. Users should be prepared for potentially explicit content when reviewing the fetched comments. Viewer discretion is advised.
