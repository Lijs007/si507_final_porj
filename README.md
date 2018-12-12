#si507_f18_final#
##1.Data Source: ##
###Scrap three pages from stats.nba.com, one for player data, one for team data and one for all time player data.###
###Use Reddit API to get comment on some keywords.###
###You can use DB browser for sqlite to read the two sqlite files and use any editor to read the json file.###
##2.requirement.txt records the packages needed. pip install requirements.txt before running it.##
##3.Class and functions##
###There's a class called reddit_data which holds a dictionary cached_dict and a list of also stopwords.###
###Function get_wordcloud(self, keyword) will draw a word cloud of the given keyword based on the comment on reddit.###
###plot_scatter(keyword, select) will plot a scatter graph with the given keyword and var select('player' or 'team')###
##4.You can start the project by running the final.py. Then visit the given url on localhost on a web browser.##
