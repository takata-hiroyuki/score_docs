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
        あなたはプロの日本語推敲が得意な編集者です。
        以下の日報を、観点にそって100点満点で厳しく採点してください。
        採点後、以下のフォーマットで結果を返してください。
        コメントには減点内容も含めてください。

        【観点】
        1. 分かりやすさ。素人や子供など誰が読んでも分かる文章になっているか。こちらが今回の採点のメインとなります。
        2. 誤字脱字。 ビジネスマンとして当たり前な誤字脱字は減点対象です。

        【フォーマット】
        点数: [0-100]
        コメント: [具体的な改善点や評価ポイント]

        ---
        【日報】
        {report_text}
        """

        # OpenAI APIを呼び出す
        response = openai.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": "あなたは優秀な編集者です。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5, # 出力の多様性を調整
            max_tokens=500,  # 最大トークン数
        )

        # 応答から結果を抽出
        result = response.choices[0].message.content

        # 結果をパースして点数とコメントに分割
        print(result)#デバッグ用
        lines = result.strip().split('\n')
        score = 0
        comment = ""

        for i, line in enumerate(lines):
            if '点数:' in line:
                try:
                    score = int(line.replace('点数:', '').strip())
                except ValueError:
                    pass # 点数が不正な形式の場合はスキップ
            elif 'コメント:' in line:
                # 「コメント:」の後のテキストと、それ以降のすべての行を連結する
                comment_parts = [line.replace('コメント:', '').strip()]
                comment_parts.extend(lines[i+1:])
                comment = '\n'.join(comment_parts).strip()
                break # コメントが見つかったらループを終了

        # scoreとcommentが両方取得できなかった場合のフォールバック
        if score == 0 and not comment:
            # 最も基本的なパースを試みる
            try:
                score_line = [line for line in lines if '点数:' in line][0]
                score = int(score_line.replace('点数:', '').strip())
                comment_line = [line for line in lines if 'コメント:' in line][0]
                comment = comment_line.replace('コメント:', '').strip()
            except (IndexError, ValueError):
                 raise ValueError("レスポンスから点数とコメントを抽出できませんでした。")

        return score, comment

    except Exception as e:
        st.error(f"API呼び出し中にエラーが発生しました: {e}")
        return 0, "採点中にエラーが発生しました。"

