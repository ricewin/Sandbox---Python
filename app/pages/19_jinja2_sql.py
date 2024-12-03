import streamlit as st
from jinja2 import Template

# SQLテンプレート
template = """
{% set ns = namespace(last_user_id=None) -%}
{% for user_id in user_ids -%}
    {% set ns.last_user_id = user_id -%}
    SELECT * FROM users WHERE id = {{ user_id }};
{% endfor %}

-- 最後のユーザーIDを使ったクエリ
SELECT * FROM transactions WHERE user_id = {{ ns.last_user_id }};
"""

# Pythonデータ
user_ids = [1, 2, 3, 4, 5]

# Jinja2テンプレートのコンパイル
jinja_template = Template(template)

# テンプレートにデータをレンダリング
sql_query = jinja_template.render(user_ids=user_ids)

st.code(sql_query, language="sql")
