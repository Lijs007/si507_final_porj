import praw
import pandas as pd
import datetime as dt
import json
import request
from secret import personal_use_script, secret, name, user, pwd 
import nltk 
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt
from flask import Flask, render_template, redirect
import sqlite3
import plotly
import plotly.graph_objs as go

diction = {'player':{'table' : 'Players', 'col' : 'PLAYER'},'team':{'table' : 'Teams', 'col' : 'TEAM'}}

class reddit_data():
	stop = set(stopwords.words("english"))
	#The extra_stopwords are copied online, I know it's too long...
	extra_stopwords = ['a', 'about', 'above', 'across', 'after', 'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'among', 'an', 'and', 'another', 'any', 'anybody', 'anyone', 'anything', 'anywhere', 'are', 'area', 'areas', 'around', 'as', 'ask', 'asked', 'asking', 'asks', 'at', 'away', 'b', 'back', 'backed', 'backing', 'backs', 'be', 'became', 'because', 'become', 'becomes', 'been', 'before', 'began', 'behind', 'being', 'beings', 'best', 'better', 'between', 'big', 'both', 'but', 'by', 'c', 'came', 'can', 'cannot', 'case', 'cases', 'certain', 'certainly', 'clear', 'clearly', 'come', 'could', 'd', 'did', 'differ', 'different', 'differently', 'do', 'does', 'done', 'down', 'down', 'downed', 'downing', 'downs', 'during', 'e', 'each', 'early', 'either', 'end', 'ended', 'ending', 'ends', 'enough', 'even', 'evenly', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'f', 'face', 'faces', 'fact', 'facts', 'far', 'felt', 'few', 'find', 'finds', 'first', 'for', 'four', 'from', 'full', 'fully', 'further', 'furthered', 'furthering', 'furthers', 'g', 'gave', 'general', 'generally', 'get', 'gets', 'give', 'given', 'gives', 'go', 'going', 'good', 'goods', 'got', 'great', 'greater', 'greatest', 'group', 'grouped', 'grouping', 'groups', 'h', 'had', 'has', 'have', 'having', 'he', 'her', 'here', 'herself', 'high', 'high', 'high', 'higher', 'highest', 'him', 'himself', 'his', 'how', 'however', 'i', 'if', 'important', 'in', 'interest', 'interested', 'interesting', 'interests', 'into', 'is', 'it', 'its', 'itself', 'j', 'just', 'k', 'keep', 'keeps', 'kind', 'knew', 'know', 'known', 'knows', 'l', 'large', 'largely', 'last', 'later', 'latest', 'least', 'less', 'let', 'lets', 'like', 'likely', 'long', 'longer', 'longest', 'm', 'made', 'make', 'making', 'man', 'many', 'may', 'me', 'member', 'members', 'men', 'might', 'more', 'most', 'mostly', 'mr', 'mrs', 'much', 'must', 'my', 'myself', 'n', 'necessary', 'need', 'needed', 'needing', 'needs', 'never', 'new', 'new', 'newer', 'newest', 'next', 'no', 'nobody', 'non', 'noone', 'not', 'nothing', 'now', 'nowhere', 'number', 'numbers', 'o', 'of', 'off', 'often', 'old', 'older', 'oldest', 'on', 'once', 'one', 'only', 'open', 'opened', 'opening', 'opens', 'or', 'order', 'ordered', 'ordering', 'orders', 'other', 'others', 'our', 'out', 'over', 'p', 'part', 'parted', 'parting', 'parts', 'per', 'perhaps', 'place', 'places', 'point', 'pointed', 'pointing', 'points', 'possible', 'present', 'presented', 'presenting', 'presents', 'problem', 'problems', 'put', 'puts', 'q', 'quite', 'r', 'rather', 'really', 'right', 'right', 'room', 'rooms', 's', 'said', 'same', 'saw', 'say', 'says', 'second', 'seconds', 'see', 'seem', 'seemed', 'seeming', 'seems', 'sees', 'several', 'shall', 'she', 'should', 'show', 'showed', 'showing', 'shows', 'side', 'sides', 'since', 'small', 'smaller', 'smallest', 'so', 'some', 'somebody', 'someone', 'something', 'somewhere', 'state', 'states', 'still', 'still', 'such', 'sure', 't', 'take', 'taken', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'therefore', 'these', 'they', 'thing', 'things', 'think', 'thinks', 'this', 'those', 'though', 'thought', 'thoughts', 'three', 'through', 'thus', 'to', 'today', 'together', 'too', 'took', 'toward', 'turn', 'turned', 'turning', 'turns', 'two', 'u', 'under', 'until', 'up', 'upon', 'us', 'use', 'used', 'uses', 'v', 'very', 'w', 'want', 'wanted', 'wanting', 'wants', 'was', 'way', 'ways', 'we', 'well', 'wells', 'went', 'were', 'what', 'when', 'where', 'whether', 'which', 'while', 'who', 'whole', 'whose', 'why', 'will', 'with', 'within', 'without', 'work', 'worked', 'working', 'works', 'would', 'x', 'y', 'year', 'years', 'yet', 'you', 'young', 'younger', 'youngest', 'your', 'yours', 'z']
	stop = stop.union(extra_stopwords)
	stop = stop.union(["https", "http", "RT", "people", "n't", "shit", "yeah", "game", "games", "team", "teams", "player", "players", "basketball", "nba", "play", "lol", "lmao", "guy", "dude", "actually" ])
	cache_fname = 'cache_comment.json'
	cached_dict = {}

	
	def __init__(self):

		try:
			fr = open(self.cache_fname,'r')
			self.cached_dict = json.loads(fr.read())
			fr.close()

		except:
			pass

	def print_most_frequent_word(self, search_str):
		text = ""
		freq_dict = {}
		for comment in self.cached_dict[search_str]:
			words = nltk.word_tokenize(comment)
			for word in words:
				word = word.lower()
				if word[0].isalpha() and (word not in self.stop):
					try:
						freq_dict[word] += 1
					except:
						freq_dict[word] = 1



		#item_sorted = sorted(freq_dict.items(), reverse = True, key = lambda item:item[1])

		return freq_dict


	def get_wordcloud(self, keyword):
		if keyword in self.cached_dict:
			return
		else:
			reddit = praw.Reddit(client_id=personal_use_script, \
			                 client_secret=secret, \
			                 user_agent=name, \
			                 username=user, \
			                 password=pwd)

			subreddit = reddit.subreddit('nba')

			self.cached_dict[keyword] = []

			subs = subreddit.search(keyword, sort = 'relevence', limit = 10)

			for sub_id in subs:
				submission = reddit.submission(id=sub_id)
				submission.comments.replace_more(limit=0)


				for comment in submission.comments.list():
					cached_dict[keyword].append(comment.body)

			freq = self.print_most_frequent_word(keyword)

			wordcloud = WordCloud(width = 800, height = 800, 
			                background_color ='white', 
			                stopwords = STOPWORDS, 
			                min_font_size = 10).generate_from_frequencies(freq) 
			  
			# plot the WordCloud image                        
			plt.figure(figsize = (8, 8), facecolor = None) 
			plt.imshow(wordcloud, interpolation="bilinear") 
			plt.axis("off") 
			plt.tight_layout(pad = 0) 
			#plt.show()
			plt.savefig("./static/img/wordcloud/" + keyword + ".png")

			fw = open(self.cache_fname,'w')
			fw.write(json.dumps(self.cached_dict, indent = 4))
			fw.close()

def plot_polar(keyword, select):
	try:
		conn = sqlite3.connect("final.sqlite")
		cur = conn.cursor()
		statement = '''
			SELECT * FROM
			{} t
			WHERE t.{} LIKE "%{}%"
		'''
		statement = statement.format(diction[select]['table'], diction[select]['col'], keyword)

		cur.execute(statement)
		data = list(cur.fetchone())

		cur.execute('PRAGMA table_info({})'.format(diction[select]['table']))
		tups = cur.fetchall()

		if select == 'player': 
			cur.execute('SELECT MAX(PTS), MAX(REB), MAX(AST), MAX(STL), MAX(BLK), MAX(TOV) FROM ' + diction[select]['table'] + ';')
			maxs = cur.fetchone()
			#print(maxs)
			#print(data)

			cols = []
			for tup in tups:
				cols.append(tup[1])
			conn.close()
			#data = [go.Bar(x = data[3:], y = cols[3:], orientation = 'h')]
			data = [go.Scatterpolar(r = [data[8]/maxs[0], data[20]/maxs[1], data[21]/maxs[2], data[23]/maxs[3], data[24]/maxs[4], data[22]/maxs[5], data[8]/maxs[0]],\
			 theta = [cols[8], cols[20], cols[21], cols[23], cols[24], cols[22], cols[8]], fill = 'toself')]
			#layout = go.Layout(polar = dict(radialaxis = dict( visible = True, range = [0, 1])), showlegend = False)

			#plotly.offline.plot(data, filename='./static/img/player/' + keyword + '.png', image='png')
			# plotly.offline.plot({"data": data,
		#                     "layout": go.Layout(title="Data of " + keyword)},
		#                     image='png', image_filename='test')
			#fig = {'data' : data, 'layout' : layout}
		else:
			cur.execute('SELECT MAX("WIN%"), MAX(PTS), MAX("3PA"), MAX("3P%"), MAX(REB), MAX(AST), MAX(TOV), MAX("+/-") FROM ' + diction[select]['table'] + ';')
			maxs = cur.fetchone()
			#print(maxs)
			#print(data)

			cols = []
			for tup in tups:
				cols.append(tup[1])
			conn.close()
			#data = [go.Bar(x = data[3:], y = cols[3:], orientation = 'h')]
			data = [go.Scatterpolar(r = [data[5]/maxs[0], data[7]/maxs[1], data[12]/maxs[2], data[13]/maxs[3], data[19]/maxs[4], data[20]/maxs[5], data[21]/maxs[6], data[27]/maxs[7], data[5]/maxs[0]],\
			 theta = [cols[5], cols[7], cols[12], cols[13], cols[19], cols[20], cols[21], cols[27], cols[5]], fill = 'toself')]
			#layout = go.Layout(polar = dict(radialaxis = dict( visible = True, range = [0, 1])), showlegend = False)

			#plotly.offline.plot(data, filename='./static/img/player/' + keyword + '.png', image='png')
			# plotly.offline.plot({"data": data,
		#                     "layout": go.Layout(title="Data of " + keyword)},
		#                     image='png', image_filename='test')
			#fig = {'data' : data, 'layout' : layout}

	except:
		data = [go.Scatterpolar( r = [0,0,0,0,0,0], theta = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PTS'])]

	graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)	
	return graphJSON	

def plot_scatter(keyword, select):
	namelist = []
	vars1 = []
	vars2 = []
	strs = keyword.split('&')
	conn = sqlite3.connect("final.sqlite")
	cur = conn.cursor()
	statement = '''
		SELECT {}, "{}", "{}" FROM {}
		ORDER BY "{}" DESC LIMIT 50 
	'''
	statement = statement.format(diction[select]['col'], strs[0], strs[1], diction[select]['table'], strs[0])
	cur.execute(statement)
	players = cur.fetchall()

	conn.close()

	for player in players:
		tups = list(player)
		namelist.append(tups[0])
		vars1.append(tups[1])
		vars2.append(tups[2])

	trace = go.Scatter(x = vars1, y = vars2, mode = 'markers', name = 'markers', text = namelist)
	data = [trace]
	layout= go.Layout(title= strs[0] + ' vs. ' + strs[1], hovermode= 'closest', xaxis= dict( title= strs[0], ticklen= 5, zeroline= False, gridwidth= 2,),\
		yaxis=dict(title= strs[1], ticklen= 5, gridwidth= 2,),showlegend= False)
	fig= go.Figure(data = data, layout=layout)

	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON

def create_table(tb_name):
	return_list = []
	search_list = ['PTS', 'REB', 'AST', 'BLK', 'STL', 'TOV']
	conn = sqlite3.connect(tb_name)
	cur = conn.cursor()
	statement = '''
		SELECT PLAYER, {} FROM Players
		WHERE {} != '-'
		ORDER BY {} DESC LIMIT 10 
	'''
	for i in range(len(search_list)):
		state = statement.format(search_list[i], search_list[i], search_list[i])
		cur.execute(state)
		return_list.append(cur.fetchall())

	return return_list

def get_total_name_list(db_name, select):
	namelist = []
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	statement = '''
		SELECT {} FROM {}
	'''	
	if db_name == "final.sqlite":
		statement = statement.format(diction[select]['col'], diction[select]['table'])
	else:
		statement = statement.format('Player', 'Players')
	cur.execute(statement)
	for  item in cur.fetchall():
		namelist.append([item[0],select])
	return namelist


r_data = reddit_data()


app = Flask(__name__)

@app.route('/player/<nm>')
def display_player(nm):
	nm = nm.replace("%20", " ")
	r_data.get_wordcloud(nm)
	graphJSON = plot_polar(keyword = nm, select = 'player')
	total_list = get_total_name_list("final.sqlite",'player') + get_total_name_list("final.sqlite", "team") + get_total_name_list("all_time.sqlite", "player")
	return render_template('index.html', name=nm, graphJSON=graphJSON, total_list = total_list)

@app.route('/team/<nm>')
def display_team(nm):
	nm = nm.replace("%20", " ")
	r_data.get_wordcloud(nm)
	graphJSON = plot_polar(keyword = nm, select = 'team')
	total_list = get_total_name_list("final.sqlite",'player') + get_total_name_list("final.sqlite", "team") + get_total_name_list("all_time.sqlite", "player")
	return render_template('index.html', name=nm, graphJSON=graphJSON, total_list = total_list)


@app.route('/<vars>')
def scatter(vars):
	graphJSON = plot_scatter(keyword = vars, select = 'player')
	data = create_table("final.sqlite")
	data_all = create_table("all_time.sqlite")
	header = vars.replace("&", " vs. ")
	total_list = get_total_name_list("final.sqlite",'player') + get_total_name_list("final.sqlite", "team") + get_total_name_list("all_time.sqlite", "player")
	return render_template('default.html', header = header, graphJSON = graphJSON, data = data, data_all = data_all, total_list = total_list)

@app.route('/')
def home():
	return redirect('/3PA&3P%')
	#return render_template('default.html')

if __name__ == '__main__':
	app.run(debug=True)
	#plot_bar('Kevin Durant')
	#print(create_table())
	#print(get_total_name_list())

