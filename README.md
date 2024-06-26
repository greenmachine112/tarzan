# Tarzan 
An automated trading bot that gathers text data from a specified subreddit, analyzes sentiment with the Vader library, and places trades to an Alpaca brokerage account via the Alpaca Trading API based on inverse popular sentiment. It aims to capitalize on market overcorrections and uneducated investing.
## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/greenmachine112/tarzan.git
    ```
2. Navigate to the project directory:
    ```bash
    cd tarzan.git
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
## Usage
**NOTE**: Do not use this model for real trading, as this version suffers from time complexity issues. It averages a comment filter rate of 1.57 +- .4 comments per minute. This program is under active development, and this issue will be fixed in the future.

To connect Tarzan to an Alpaca brokerage account and place trades you must first get a key pair from Alpaca, and Reddit.

1. Alpaca Registry:
    ```bash
    https://app.alpaca.markets/signup
    ```
2. Reddit Registry:
    ```bash
    https://www.reddit.com/wiki/api/
    ```
   
After obtaining the keys, load them into the ```.env ``` file and verify the configurations in ```config.py ``` as well as any files that import from it.

3. Navigate to source:
   ```bash
   cd C:\your-path\InverseWSB-Trading-Bot\src 
   ```
4. Run:
   ```bash
   python main.py
   ```

**NOTE**: Unless you want to trade using real funds, make sure the base Alpaca url's host is ```paper-api.alpaca.markets```. I highly recommend **not** giving the bot your funds, unless you'd like to, personally, pay the salary of a Wall Street banker on accident.

## Commands

Configuration options.

## Optimization and API Call Details

### Fetching Comments
To ensure a sufficient number of comments are available for analysis, the ```fetchComments``` function fetches submissions from a specified subreddit. It calculates the number of submissions to fetch based on a fraction of the total desired comments ```comLimit```. For example, if ```comLimit``` is set to 1000, the function fetches submissions with a limit of 100 (i.e., com_limit / 10). Each submission can contain multiple comments, leading to a higher total number of comments fetched. 

If you have 8 keywords, the total number of search terms would be 8 (keywords) + 1 (primary ticker) = 9.For a ```comLimit``` of 1000 and 9 search terms, the program would set ```rawComments``` to be fetched = ```comLimit * 9```

### Filtering Comments
The ```filterComments``` function processes the fetched comments to filter out those that match specific criteria, such as containing certain keywords, meeting minimum upvote and karma thresholds, and being within a specified time limit. During this process, the process bar will filter signifigantly more than ```comLimit``` comments on account that the likelihood of fetching exactly ```comLimit``` comments and all of them having at least one keyword is low. To address this, the ```fetchComments``` function has been optimized to return exactly the number of comments specified by ```comLimit```. This ensures the progress bar accurately reflects the number of comments being processed. 

### Filter Speed
The initial comment filter function of the bot has an average filter rate of ```1.59 comments per second```. This speed is a combination of multiple variables. The first is the speed of the Reddit API, which we can safely geuss is not optimized for high-speed trading, as Reddit comments aren't valuable to the average trading bot. The second is that the current algorithm uses a non-linear search. When inputting variations to search, keep in mind the time complexity increases with 'k' variations. This program is under active development, and a parallel computing or regex style algorithms may be implemented in the future. See [filterComments time complexity](#filter-comments).

## API Call Details
 When fetching comments, the bot makes API calls to Reddit as follows:

### Submission Fetching
The bot makes a single API call to fetch up to 100 submissions. For a ```comLimit``` of 1000, this results in 1 API call.

### Comments Fetching
Each submission may contain multiple comments. The bot fetches all comments for each submission, which may require additional API calls, especially for submissions with many comments. 
On average, this results in approximately 1 API call/submission.

**In total, for a ```comLimit``` of 1000, the bot typically makes around ```101 API calls``` (1 for submissions and around 100 for comments).**

## Handling Rate Limits
Reddit enforces API rate limits for their free tier. Authenticated requests are limited to ```60/m```. This program is under active development and backoff strategies may be implemented in the future.

### Exceeding Rate Limit
The Reddit API's free tier specifies that you may not exceed 60 calls/minute. If the API returns a ```HTTP 429 ERROR```, the program will save what it has filtered to the ```.json```, notify the user, and then terminate. You may then analyze the ```.json``` file using ```sentiment_analyzer``` as normal. If you hit the limit, it's safe to wait for a full minute before trying again. This program is under active development, and rate limit monitoring will be implemented in a future release

## Time Complexity Summary for Search and Filter

### Fetch Comments
1. Function: ```fetchComments```
2. Time Complexity: ```O(N)```
3. Explanation: The function fetches comments from subreddit submissions. Linear complexity```N```.

### Filter Comments
1. Function: ```filterComments```
2. Time Complexity: ```O(i * m * k)```
3. Variables:
    -  ```i```: Number of comments to filter
    - ```m```: Average length of each comment
    - ```k```: Number of search term variations
4. Explanation: For each comment, the function converts the text to lowercase ```(O(m))```, and checks if any of the ```k``` variations are present (O(k)). Therefore, the time complexity for filtering one comment is ```O(m * k)```. Given ```i``` comments, the overall complexity is ```O(i * m * k)```

### Combined Complexity
The combined time complexity for fetching and filtering is as follows:
1. Fetching: ```O(N)```
2. Filtering: ```O(i * m * k)```
3. Total: ```O(N + i * m * k)```

## Understanding Filter Pass Rate and Keywords
When the number of keywords used in filtering increases, the filter pass rate tends to decrease. This is because each additional keyword introduces another condition that a comment must meet to pass the filter. Therefore, the more keywords you have, the fewer comments will typically match all the criteria.

### Impact of Keywords on Filter Pass Rate
1. **More Keywords**: As the number of keywords increases, each comment has more conditions to satisfy. This generally leads to a lower filter pass rate because fewer comments will meet all the specified criteria.
1. **Fewer Keywords**: With fewer keywords, each comment has fewer conditions to satisfy, which typically leads to a higher filter pass rate because more comments will meet the fewer criteria.
3. **Calculation of Fetch Count with Keywords**
The number of comments fetched ```F``` is calculated to ensure that the desired number of comments ```C``` is met after filtering. As the number of keywords increases, the estimated filter pass rate ```P``` will decrease, requiring more comments to be fetched.
    - Formula:
      - ```𝐹 = 𝐶/𝑃```
    - Where:
      - ```𝐹``` = Number of comments to fetch
      - ```𝐶``` = Number of comments requested by the user
      - ```𝑃``` = Estimated filter pass rate (inverse relationship with ```k``` keywords)

**Example**: If the user requests 1000 comments and the estimated filter pass rate is 0.2 with a certain number of keywords, the program will fetch: ```𝐹 = 1000/0.2 = 500```
If the number of keywords increases and the filter pass rate drops to 0.1, the program will fetch: ```𝐹 = 1000/0.1 = 1000```

## .json Formatting
The ```.json``` files containing the filtered data can be quite large. 
### Example 
![image](https://i.postimg.cc/G2s9V3Wf/example-output.png)

Here are some important points to understand about the structure and content of these files:
1. **File Size**: The ```.json``` filse can have thousands of lines due to the detailed structure of each comment.
2. **Comment Breakdown**: Each comment occupies multiple lines in the ```.json``` files. Typically, a single comment is represented by 6 lines, including metadata like ```timestamp```, ```karma```, ```score```, and ```body```.
3. **Estimating Total Comments**: To quickly estimate the total number of comments in your ```.json``` files, you can use the following approximation:
```totalComments = linesInJson / 6```

## Sentiment
To analyze the sentiment of comment bodies, they are run through the ```vaderSentiment``` transformer

### Sentiment Analysis Algorithm
The sentiment analysis has been updated to, in addition to single variable analysis, weigh comments based on the number of upvotes. This means that comments with more upvotes have a greater influence on the overall sentiment score. ```weightedOverallSentiment``` is calculated by multiplying the vader output by the ```score``` value of a given comment. This ensures that comments with higher upvotes, which likely represent more widely held opinions, have a greater impact on the overall sentiment analysis.

### Example Output
![image](https://i.postimg.cc/pLq9n6Qs/sentiment-output.png)

NOTE: The inverse trading strategy may be reversed, or otherwise modified, by modifying ```stockPurchaseSide``` in ```sentiment_analyzer.py```

## Profanity 
Comments fetched from subreddits, especially from communities like ```r/wallstreetbets```, may contain profane or offensive language. These communities are known for their unfiltered and often crude discussions. They refer to themselves as 'apes', which gives you an idea of their vernacular. Users should be prepared for potentially explicit content when reviewing the fetched comments. **Viewer discretion is advised**
