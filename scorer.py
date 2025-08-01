import openai
import streamlit as st

# secrets.tomlからAPIキーを読み込む
openai.api_key = st.secrets["OPENAI_API_KEY"]

def score_report(report_text):
    """
    OpenAI APIを使って日報を採点し、点数とコメントを返す関数
    """
    try:
        # AIへの指示（プロンプト）を作成
        prompt = f"""
        以下の日報を、プロのビジネスアナリストの視点で厳しく採点してください。
        採点後、以下のフォーマットで結果を返してください。
        コメントには減点内容も含めてください。

        【フォーマット】
        点数: [0-100]
        コメント: [具体的な改善点や評価ポイント]

        ---
        【日報】
        {report_text}
        """

        # OpenAI APIを呼び出す
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # 最新のモデルがおすすめです
            messages=[
                {"role": "system", "content": "あなたは優秀なビジネスアナリストです。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5, # 出力の多様性を調整
            max_tokens=500,  # 最大トークン数
        )

        # 応答から結果を抽出
        result = response.choices[0].message.content

        # 結果をパースして点数とコメントに分割
        score_line = [line for line in result.split('\n') if '点数:' in line][0]
        comment_line = [line for line in result.split('\n') if 'コメント:' in line][0]
        
        score = int(score_line.replace('点数:', '').strip())
        comment = comment_line.replace('コメント:', '').strip()

        return score, comment

    except Exception as e:
        st.error(f"API呼び出し中にエラーが発生しました: {e}")
        return 0, "採点中にエラーが発生しました。"

