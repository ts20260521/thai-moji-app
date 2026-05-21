import streamlit as st
import random

# ページの設定
st.set_page_config(page_title="タイ子音マスター42", page_icon="🇹🇭", layout="centered")

# タイ文字子音42文字の完全データ
# 形式: {"文字": ["正解の読み(意味)", "ダミー1", "ダミー2", "ダミー3"]}
THAI_CONSONANTS = {
    "ก": ["ko kai (鶏のk)", "kho khai (卵のkh)", "so so (鎖のs)", "ngo ngu (蛇のng)"],
    "ข": ["kho khai (卵のkh)", "ko kai (鶏)", "so so (鎖のs)", "cho chan (皿のc)"],
    "ค": ["kho khwai (水牛のkh)", "do dek (子供のd)", "kho rakhang (鐘のkh)", "ngo ngu (蛇のng)"],
    "ฆ": ["kho rakhang (鐘のkh)", "kho khwai (水牛のkh)", "ngo ngu (蛇のng)", "mo ma (馬のm)"],
    "ง": ["ngo ngu (蛇のng)", "no nu (ネズミのn)", "mo ma (馬のm)", "lo ling (猿のl)"],
    "จ": ["cho chan (皿のc)", "cho ching (シンバルのch)", "cho chang (象のch)", "so so (鎖のs)"],
    "ฉ": ["cho ching (シンバルのch)", "cho chan (皿のc)", "cho chang (象のch)", "pho phung (蜂のph)"],
    "ช": ["cho chang (象のch)", "so so (鎖のs)", "cho kachəə (木のch)", "yo yak (夜叉のy)"],
    "ซ": ["so so (鎖のs)", "cho chang (象のch)", "so sua (虎のs)", "so sala (東屋のs)"],
    "ฌ": ["cho kachəə (木のch)", "cho chang (象のch)", "yo ying (女性のy)", "tho thahan (兵士のth)"],
    "ญ": ["yo ying (女性のy)", "yo yak (夜叉のy)", "no nen (小僧のn)", "tho montho (モントー夫人のth)"],
    "ฎ": ["do chada (冠のd)", "to patak (水牛制御棒のt)", "tho than (台座のth)", "do dek (子供のd)"],
    "ฏ": ["to patak (水牛制御棒のt)", "do chada (冠のd)", "to tao (亀のt)", "tho phuthao (老人のth)"],
    "ฐ": ["tho than (台座のth)", "tho montho (モントー夫人のth)", "tho phuthao (老人のth)", "no nen (小僧のn)"],
    "ฑ": ["tho montho (モントー夫人のth)", "tho than (台座のth)", "tho phuthao (老人のth)", "tho thahan (兵士のth)"],
    "ฒ": ["tho phuthao (老人のth)", "to tao (亀のt)", "tho than (台座のth)", "no nen (小僧のn)"],
    "ณ": ["no nen (小僧のn)", "no nu (ネズミのn)", "mo ma (馬のm)", "lo ling (猿のl)"],
    "ด": ["do dek (子供のd)", "to tao (亀のt)", "do chada (冠のd)", "bo baimai (葉のb)"],
    "ต": ["to tao (亀のt)", "do dek (子供のd)", "to patak (水牛制御棒のt)", "tho thung (袋のth)"],
    "ถ": ["tho thung (袋のth)", "tho thahan (兵士のth)", "tho thong (旗のth)", "pho phung (蜂のph)"],
    "ท": ["tho thahan (兵士のth)", "tho thong (旗のth)", "tho thung (袋のth)", "tho phuthao (老人のth)"],
    "ธ": ["tho thong (旗のth)", "tho thahan (兵士のth)", "no nu (ネズミのn)", "ro rua (船のr)"],
    "น": ["no nu (ネズミのn)", "mo ma (馬のm)", "no nen (小僧のn)", "lo ling (猿のl)"],
    "บ": ["bo baimai (葉のb)", "po pla (魚のp)", "pho phan (トレイのph)", "fo fan (歯のf)"],
    "ป": ["po pla (魚のp)", "bo baimai (葉のb)", "pho phan (トレイのph)", "fo fa (蓋のf)"],
    "ผ": ["pho phung (蜂のph)", "fo fa (蓋のf)", "pho phan (トレイのph)", "pho samphao (ジャンク船のph)"],
    "ฝ": ["fo fa (蓋のf)", "pho phung (蜂のph)", "fo fan (歯のf)", "pho phan (トレイのph)"],
    "พ": ["pho phan (トレイのph)", "fo fan (歯のf)", "pho phung (蜂のph)", "pho samphao (ジャンクのph)"],
    "ฟ": ["fo fan (歯のf)", "pho phan (トレイのph)", "fo fa (蓋のf)", "lo ling (猿のl)"],
    "ภ": ["pho samphao (ジャンクのph)", "pho phan (トレイのph)", "mo ma (馬のm)", "ko kai (鶏のk)"],
    "ม": ["mo ma (馬のm)", "no nu (ネズミのn)", "lo ling (猿のl)", "yo yak (夜叉のy)"],
    "ย": ["yo yak (夜叉のy)", "yo ying (女性のy)", "ro rua (船のr)", "lo ling (猿のl)"],
    "ร": ["ro rua (船のr)", "lo ling (猿のl)", "wo waen (指輪のw)", "mo ma (馬のm)"],
    "ล": ["lo ling (猿のl)", "ro rua (船のr)", "so sua (虎のs)", "lo chula (凧のl)"],
    "ว": ["wo waen (指輪のw)", "ro rua (船のr)", "lo ling (猿のl)", "ɔ ang (洗面器のɔɔ)"],
    "ศ": ["so sala (東屋のs)", "so sua (虎のs)", "so lusi (仙人のs)", "so so (鎖のs)"],
    "ษ": ["so lusi (仙人のs)", "so sala (東屋のs)", "so sua (虎のs)", "bo baimai (葉のb)"],
    "ส": ["so sua (虎のs)", "so sala (東屋のs)", "so lusi (仙人のs)", "cho chan (皿のc)"],
    "ห": ["ho hip (箱のh)", "ɔ ang (洗面器のɔɔ)", "ho nokhuk (ミミズクのh)", "pho samphao (ジャンクのph)"],
    "ฬ": ["lo chula (凧のl)", "lo ling (猿のl)", "ro rua (船のr)", "ɔ ang (洗面器のɔɔ)"],
    "อ": ["ɔ ang (洗面器のɔɔ)", "ho hip (箱のh)", "ho nokhuk (ミミズクのh)", "wo waen (指輪のw)"],
    "ฮ": ["ho nokhuk (ミミズクのh)", "ho hip (箱のh)", "ɔ ang (洗面器のɔɔ)", "ko kai (鶏のk)"]
}

# セッション状態の初期化
if "current_char" not in st.session_state:
    st.session_state.current_char = random.choice(list(THAI_CONSONANTS.keys()))
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.choices = []
    st.session_state.answered = False
    st.session_state.feedback = ""

# 次の問題に進む関数
def next_question():
    st.session_state.current_char = random.choice(list(THAI_CONSONANTS.keys()))
    st.session_state.answered = False
    st.session_state.feedback = ""
    
    options = THAI_CONSONANTS[st.session_state.current_char].copy()
    correct = options[0]
    random.shuffle(options)
    st.session_state.choices = options
    st.session_state.correct_answer = correct

if not st.session_state.choices:
    next_question()

# --- 画面UIレイアウト ---
st.title("🇹🇭 タイ文字子音完全マスター（42文字）")
st.write("ランダムに出題されるタイ文字の読み方を当てよう！")

# スコア表示
st.subheader(f"成績: {st.session_state.score} / {st.session_state.total} 問正解")

st.markdown("---")

# 文字を巨大表示
st.markdown(
    f"<h1 style='text-align: center; font-size: 120px; color: #2563EB;'>{st.session_state.current_char}</h1>", 
    unsafe_allow_html=True
)

st.markdown("---")

# 4択ボタン
for choice in st.session_state.choices:
    if st.button(choice, use_container_width=True, disabled=st.session_state.answered):
        st.session_state.answered = True
        st.session_state.total += 1
        if choice == st.session_state.correct_answer:
            st.session_state.score += 1
            st.session_state.feedback = "⭕ 正解です！その調子！"
        else:
            st.session_state.feedback = f"❌ 残念！正解は 「{st.session_state.correct_answer}」 です。"
        st.rerun()

# 結果フィードバックと次の問題へのボタン
if st.session_state.answered:
    if "⭕" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)
        
    if st.button("次の文字へ進む ➡️", use_container_width=True):
        next_question()
        st.rerun()

# サイドバーにリセットと進捗一覧
with st.sidebar:
    st.header("オプション")
    if st.button("スコアをリセット"):
        st.session_state.score = 0
        st.session_state.total = 0
        next_question()
        st.rerun()
        
    st.markdown("---")
    st.write("💡 **豆知識**")
    st.caption("「ฃ」と「ฅ」の2文字は、現代のタイ語では使われていませんので含まれていません。")