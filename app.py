
import streamlit as st
import numpy as np
from scipy.stats import poisson
from api_handler import get_upcoming_matches

st.set_page_config(page_title="📊 توقعات و رهانات ذكية", layout="centered")

st.title("⚽ تحليل ذكي للمباريات")
matches = get_upcoming_matches()
match_options = [f"{m['home']} vs {m['away']}" for m in matches]
match_choice = st.selectbox("اختر مباراة", match_options)

match = matches[match_options.index(match_choice)]

# اختياري: إدخال يدوي لأودز المراهنة
home_odds = st.number_input("💰 أودز الفريق المضيف", 1.1, 20.0, 2.1)
draw_odds = st.number_input("💰 أودز التعادل", 1.1, 20.0, 3.2)
away_odds = st.number_input("💰 أودز الفريق الضيف", 1.1, 20.0, 3.0)

# القيم التجريبية مؤقتاً (لأن API team_id وتحليل المتوسطات غير مفعل هنا)
home_avg = 1.6
away_avg = 1.2

def poisson_matrix(mu1, mu2, max_goals=5):
    return [[poisson.pmf(i, mu1) * poisson.pmf(j, mu2) for j in range(max_goals+1)] for i in range(max_goals+1)]

def get_probs(mat):
    home, draw, away = 0, 0, 0
    for i in range(len(mat)):
        for j in range(len(mat)):
            if i > j: home += mat[i][j]
            elif i == j: draw += mat[i][j]
            else: away += mat[i][j]
    return home, draw, away

def expected_value(prob, odds): return round((prob * odds) - 1, 3)

if st.button("🔍 تحليل المباراة"):
    mat = poisson_matrix(home_avg, away_avg)
    prob_home, prob_draw, prob_away = get_probs(mat)

    st.subheader("🔢 الاحتمالات:")
    st.write(f"🏠 فوز {match['home']}: {prob_home:.2%}")
    st.write(f"🤝 تعادل: {prob_draw:.2%}")
    st.write(f"🛫 فوز {match['away']}: {prob_away:.2%}")

    ev_home = expected_value(prob_home, home_odds)
    ev_draw = expected_value(prob_draw, draw_odds)
    ev_away = expected_value(prob_away, away_odds)

    st.subheader("💡 القيم المتوقعة (EV):")
    st.write(f"🏠 {match['home']}: {ev_home}")
    st.write(f"🤝 تعادل: {ev_draw}")
    st.write(f"🛫 {match['away']}: {ev_away}")

    best = max([(ev_home, "🏠"), (ev_draw, "🤝"), (ev_away, "🛫")], key=lambda x: x[0])
    if best[0] > 0:
        st.success(f"أفضل رهان: {best[1]} بقيمة متوقعة = {best[0]}")
    else:
        st.warning("لا يوجد رهان ذو قيمة متوقعة إيجابية حالياً.")
