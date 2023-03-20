import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    #st.text(data)
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'overall')
    selected_user = st.sidebar.selectbox('show analysis with respect to',user_list)

    if st.sidebar.button('Show Analysis'):

        num_messages,words,num_media_msg,links = helper.fetch_stats(selected_user,df)
        cols1,cols2,cols3,cols4 = st.columns(4)

        with cols1:
            st.header('Total Messages')
            st.title(num_messages)

        with cols2:
            st.header('Total Words')
            st.title(words)

        with cols3:
            st.header('Media Shared')
            st.title(num_media_msg)

        with cols4:
            st.header('Links Shared')
            st.title(links)

        # most active user
        if selected_user == 'overall':
            st.title('Most Busy User')
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            cols1, cols2 = st.columns(2)

            with cols1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with cols2:
                st.dataframe(new_df)

        # wordcloud
        df_wc = helper.create_wordcloud(selected_user,df)

        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)