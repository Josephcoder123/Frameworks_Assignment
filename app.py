import streamlit as st

st.title('COVID-19 Research Publications Analysis')
st.write('This app provides insights into the COVID-19 research publications.')

# Add interactive widgets
year = st.slider('Select Year', min_value=int(df_cleaned['publish_year'].min()), max_value=int(df_cleaned['publish_year'].max()))
filtered_data = df_cleaned[df_cleaned['publish_year'] == year]

st.write(f'Number of publications in {year}: {len(filtered_data)}')
st.write(filtered_data[['title', 'journal', 'abstract']].head())

# Display visualizations
st.subheader('Number of Publications Over Time')
st.bar_chart(papers_per_year)

st.subheader('Top Journals Publishing COVID-19 Research')
st.bar_chart(top_journals)

st.subheader('Word Cloud of Paper Titles')
st.image(wordcloud.to_array())

#Run the Streamlit app:
streamlit run app.py
