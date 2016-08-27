#https://sites.google.com/site/miningtwitter/questions/sentiment/sentiment

###Step 1: Load the necessary packages
#install.packages(c("devtools", "rjson", "bit64", "httr"))
#install.packages("base64enc") 

# install the twitteR package from GitHub instead of the cran repository using this command:
devtools::install_github("jrowen/twitteR", ref = "oauth_httr_1_0")

library(httr)
library(devtools)
library(twitteR)
library(base64enc)

#not sure if this is useful for win machine
#download.file(url="http://curl.haxx.se/ca/cacert.pem", destfile="cacert.pem") 


#https://apps.twitter.com/app/12742461/keys
api_key <- "z8YK6fo7l8K0sYwWhFEgU5WU0"
api_secret <- "ISTJg08Pvr34cAoO0u8vTEUcy648DQShfh3LP6mZq7Lbcg72UZ"
access_token <- "3319771519-jMeBcD2lQy5aInkD8m3IXdh3Ddgi3MDPVRC5AdR"
access_token_secret <- "HBtAo86h4tUPHheg7sxI1Jtjhob87VF8OqVOu4C2ftj4g"
setup_twitter_oauth(api_key,api_secret,access_token,access_token_secret)

#sentiment is removed from CRAN and moved to https://cran.r-project.org/src/contrib/Archive/sentiment/
#Thus ill use RSentiment

library(RSentiment)
library(plyr)
library(ggplot2)
library(wordcloud)
library(RColorBrewer)

###Step 2: Collect some tweets containing the term "PSEi" 
some_tweets = searchTwitter("investagrams", n=1500, lang="en")

##@investagrams 
##@PhStockExchange 
##@Philbizwatcher - inquirer
##@PHstockMarket 
##@genkumag 
##@sirdeotraders 

# get the text
some_txt = sapply(some_tweets, function(x) x$getText())


###Step 3: Prepare the text for sentiment analysis
# remove retweet entities
some_txt = gsub("(RT|via)((?:\\b\\W*@\\w+)+)", "", some_txt)
# remove at people
some_txt = gsub("@\\w+", "", some_txt)
# remove punctuation
some_txt = gsub("[[:punct:]]", "", some_txt)
# remove numbers
#some_txt = gsub("[[:digit:]]", "", some_txt)

# remove html links
some_txt = gsub("http\\w+", "", some_txt)
# remove unnecessary spaces
some_txt = gsub("[ \t]{2,}", "", some_txt)
some_txt = gsub("^\\s+|\\s+$", "", some_txt)

# define "tolower error handling" function 
try.error = function(x)
{
  # create missing value
  y = NA
  # tryCatch error
  try_error = tryCatch(tolower(x), error=function(e) e)
  # if not an error
  if (!inherits(try_error, "error"))
    y = tolower(x)
  # result
  return(y)
}
# lower case using try.error with sapply 
some_txt = sapply(some_txt, try.error)

# remove NAs in some_txt
some_txt = some_txt[!is.na(some_txt)]
names(some_txt) = NULL

# make into dataframe
some_txt <-data.frame(some_txt = unlist(some_txt))

# remove duplicates
#some_txt = some_txt[duplicated(some_txt), ]
some_txt = unique(some_txt)

###Step 4: Perform Sentiment Analysis
##calculate_score("This is good")
##calculate_score(c("This is good","This is bad"))

# classify emotion
#see https://cran.rstudio.com/web/packages/RSentiment/RSentiment.pdf
emotion = calculate_sentiment(some_txt)
#classifies sentences into 6 categories: Positive, Negative, Very Positive, Very Negative Sarcasm and Neutral.
calculate_total_presence_sentiment(some_txt)
calculate_score(some_txt)

# get emotion best fit
#emotion = class_emo[,7]
# substitute NA's by "unknown"
#emotion[is.na(emotion)] = "unknown"

# classify polarity
#class_pol = classify_polarity(some_txt, algorithm="bayes")
# get polarity best fit
#polarity = class_pol[,4]

###Step 5: Create data frame with the results and obtain some general statistics
# data frame with results
sent_df = data.frame(text=some_txt, emotion=emotion, stringsAsFactors=FALSE)

# sort data frame
sent_df = within(sent_df,
                 emotion <- factor(emotion, levels=names(sort(table(emotion), decreasing=TRUE))))

###Step 6: Let's do some plots of the obtained results
# plot distribution of emotions
ggplot(sent_df, aes(x=emotion)) +
geom_bar(aes(y=..count.., fill=emotion)) +
scale_fill_brewer(palette="Dark2") +
labs(x="emotion categories", y="number of tweets") +
opts(title = "Sentiment Analysis of Tweets about Starbucks\n(classification by emotion)",
plot.title = theme_text(size=12))

# # plot distribution of polarity
# ggplot(sent_df, aes(x=polarity)) +
#   geom_bar(aes(y=..count.., fill=polarity)) +
#   scale_fill_brewer(palette="RdGy") +
#   labs(x="polarity categories", y="number of tweets") +
#   opts(title = "Sentiment Analysis of Tweets about Starbucks\n(classification by polarity)",
#        plot.title = theme_text(size=12))

###Step 7: Separate the text by emotions and visualize the words with a comparison cloud
# separating text by emotion
emos = levels(factor(sent_df$emotion))
nemo = length(emos)
emo.docs = rep("", nemo)
for (i in 1:nemo)
{
  tmp = some_txt[emotion == emos[i]]
  emo.docs[i] = paste(tmp, collapse=" ")
}

# remove stopwords
emo.docs = removeWords(emo.docs, stopwords("english"))
# create corpus
corpus = Corpus(VectorSource(emo.docs))
tdm = TermDocumentMatrix(corpus)
tdm = as.matrix(tdm)
colnames(tdm) = emos

# comparison word cloud
comparison.cloud(tdm, colors = brewer.pal(nemo, "Dark2"),
                 scale = c(3,.5), random.order = FALSE, title.size = 1.5)