import streamlit as st
from scorer import score_report # scorer.pyから関数をインポート

st.title('日報採点くん')

report = st.text_area('日報を入力してください', height=300)

if st.button('採点する'):
    if report:
        with st.spinner('採点中です...'):
            score, comment = score_report(report)
        
        st.subheader('採点結果')
        st.metric('得点', f'{score}点')
        st.text_area('コメント', comment, height=150)
    else:
        st.warning('日報が入力されていません。')
