from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from styles import RED, GREEN, RESET
import json

#instantiation
analyzer = SentimentIntensityAnalyzer()

#read from
def loadCommentsFromFile(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            comments = json.load(file)
        return comments
    except Exception as e:
        print(f"{RED}Failed to load comments from file: {e}{RESET}")
        return []

if __name__ == "__main__":
    comments = loadCommentsFromFile('dataset.json')
    if comments:
        #for each comment, calculate the weighted sentiment score
        weightedCompoundScores = []
        compoundScores = []
        vaderSentiments = []
        totalUpvotes = 0

        for comment in comments:
            score = analyzer.polarity_scores(comment['body'])
            upvotes = comment['score']
            compoundScores.append(score['compound'])
            weightedCompoundScore = score['compound'] * upvotes
            weightedCompoundScores.append(weightedCompoundScore)
            totalUpvotes += upvotes

            if score['compound'] >= 0.05:
                sentiment = "POSITIVE"
            elif score['compound'] <= -0.05:
                sentiment = "NEGATIVE"
            else:
                sentiment = "NEUTRAL"
            vaderSentiments.append(sentiment)

        #calculate the unweighted average compound score
        averageCompoundScore = sum(compoundScores) / len(compoundScores)

        #calculate the weighted average compound score
        if totalUpvotes != 0:
            averageWeightedCompoundScore = sum(weightedCompoundScores) / totalUpvotes
        else:
            averageWeightedCompoundScore = 0

        #classify general sentiment based on the unweighted average compound score
        if averageCompoundScore >= 0.05:
            unweightedOverallSentiment = "POSITIVE"
            unweightedSentColor = GREEN
        elif averageCompoundScore <= -0.05:
            unweightedOverallSentiment = "NEGATIVE"
            unweightedSentColor = RED
        else:
            unweightedOverallSentiment = "NEUTRAL"
            unweightedSentColor = RESET

        #classify general sentiment based on the weighted average compound score
        if averageWeightedCompoundScore >= 0.05:
            weightedOverallSentiment = "POSITIVE"
            weightedSentColor = GREEN
        elif averageWeightedCompoundScore <= -0.05:
            weightedOverallSentiment = "NEGATIVE"
            weightedSentColor = RED
        else:
            weightedOverallSentiment = "NEUTRAL"
            weightedSentColor = RESET

        #count the number of each sentiment in the dataset
        sentimentCount = {
            "POSITIVE": vaderSentiments.count("POSITIVE"),
            "NEUTRAL": vaderSentiments.count("NEUTRAL"),
            "NEGATIVE": vaderSentiments.count("NEGATIVE")
        }

        #set purchase side inverse of the weighted overall sentiment
        if weightedOverallSentiment == "POSITIVE":
            stockPurchaseSide = "SELL/SHORT"
            purchColor = RED
        elif weightedOverallSentiment == "NEGATIVE":
            stockPurchaseSide = "BUY/CALL"
            purchColor = GREEN
        else:
            stockPurchaseSide = "NO VALUE"
            purchColor = RESET

        #print results
        print(f"{GREEN}POSITIVE{RESET} comments: {sentimentCount['POSITIVE']}")
        print(f"NEUTRAL comments: {sentimentCount['NEUTRAL']}")
        print(f"{RED}NEGATIVE{RESET} comments: {sentimentCount['NEGATIVE']}")
        print(f"Unweighted overall sentiment: {unweightedSentColor}{unweightedOverallSentiment}{RESET}")
        print(f"Weighted overall sentiment: {weightedSentColor}{weightedOverallSentiment}{RESET}")
        print(f"Stock purchase side: {purchColor}{stockPurchaseSide}{RESET}")

    else:
        print("No comments found.")
