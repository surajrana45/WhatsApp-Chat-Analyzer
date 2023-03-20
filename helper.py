from urlextract import URLExtract
extractor = URLExtract()
from wordcloud import WordCloud


def fetch_stats(selected_user,df):

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    links = []
    for messages in df['message']:
        links.extend(extractor.find_urls(messages))

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]

    return num_messages, len(words),num_media_msg,len(links)


def most_busy_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})

    return x,df

def create_wordcloud(selected_user,df):

    if selected_user != 'overall':
        df = df[df['user']==selected_user]

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))

    return df_wc


