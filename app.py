import streamlit as st
import random

# ページの設定
st.set_page_config(page_title="タイ文字完全マスター", page_icon="🇹🇭", layout="centered")

# --- 👑 Google Fontsを強制的に読み込む魔法のCSS 👑 ---
# 1. Leelawadee（標準・教科書体）
# 2. Itim（丸っこい手書き風）
# 3. Kanit（タイの若者が使う、◯がない超モダン体）
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Itim&family=Kanit:wght@500&display=swap');

/* それぞれのフォントクラスを定義 */
.font-standard {
    font-family: 'Leelawadee', 'Arial', sans-serif;
}
.font-hand {
    font-family: 'Itim', cursive;
}
.font-modern {
    font-family: 'Kanit', sans-serif;
}

/* 表示をキレイに整える枠 */
.font-box {
    text-align: center; 
    padding: 10px; 
    border-radius: 10px; 
    background-color: #f0f2f6;
    margin: 5px;
}
</style>
""", unsafe_allow_html=True)

# --- データ定義（子音・母音） ---
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

# 母音32パターン（子音「ก」と組み合わせた表記）
THAI_VOWELS = {
    "กะ": ["ka (短母音 a)", "kaach (長母音 aa)", "ki (短母音 i)", "ko (短母音 o)"],
    "กา": ["kaa (長母音 aa)", "ka (短母音 a)", "ki (短母音 i)", "kee (長母音 ee)"],
    "กิ": ["ki (短母音 i)", "kii (長母音 ii)", "ku (短母音 u)", "ka (短母音 a)"],
    "กี": ["kii (長母音 ii)", "ki (短母音 i)", "kue (短母音 ue)", "kee (長母音 ee)"],
    "กึ": ["kue (短母音 ue)", "kuee (長母音 uee)", "ki (短母音 i)", "ku (短母音 u)"],
    "กือ": ["kuee (長母音 uee)", "kue (短母音 ue)", "koo (長母音 oo)", "kii (長母音 ii)"],
    "กุ": ["ku (短母音 u)", "kuu (長母音 uu)", "ki (短母音 i)", "ko (短母音 o)"],
    "กู": ["kuu (長母音 uu)", "ku (短母音 u)", "koo (長母音 oo)", "kaa (長母音 aa)"],
    "เกะ": ["ke (短母音 e)", "kee (長母音 ee)", "kae (短母音 ae)", "ko (短母音 o)"],
    "เก": ["kee (長母音 ee)", "ke (短母音 e)", "kaee (長母音 aee)", "koo (長母音 oo)"],
    "แกะ": ["kae (短母音 ae)", "kaee (長母音 aee)", "ke (短母音 e)", "ko (短母音 o)"],
    "แก": ["kaee (長母音 aee)", "kae (短母音 ae)", "kee (長母音 ee)", "koo (長母音 oo)"],
    "โกะ": ["ko (短母音 o)", "koo (長母音 oo)", "ke (短母音 e)", "kaw (短母音 aw)"],
    "โก": ["koo (長母音 oo)", "ko (短母音 o)", "kee (長母音 ee)", "kaaw (長母音 aaw)"],
    "เกาะ": ["kaw (短母音 aw)", "kaaw (長母音 aaw)", "ko (短母音 o)", "kae (短母音 ae)"],
    "กอ": ["kaaw (長母音 aaw)", "kaw (短母音 aw)", "koo (長母音 oo)", "kaee (長母音 aee)"],
    "เกอะ": ["koer (短母音 oer)", "koerr (長母音 oerr)", "ke (短母音 e)", "kue (短母音 ue)"],
    "เกอ": ["koerr (長母音 oerr)", "koer (短母音 oer)", "kee (長母音 ee)", "kuee (長母音 uee)"],
    "เกียะ": ["kia (短母音 ia)", "kiaa (長母音 iaa)", "kua (短母音 ua)", "kuea (短母音 uea)"],
    "เกีย": ["kiaa (長母音 iaa)", "kia (短母音 ia)", "kuaa (長母音 uaa)", "kueaa (長母音 ueaa)"],
    "เกือะ": ["kuea (短母音 uea)", "kueaa (長母音 ueaa)", "kia (短母音 ia)", "kua (短母音 ua)"],
    "เกือ": ["kueaa (長母音 ueaa)", "kuea (短母音 uea)", "kiaa (長母音 iaa)", "kuaa (長母音 uaa)"],
    "กัวะ": ["kua (短母音 ua)", "kuaa (長母音 uaa)", "kia (短母音 ia)", "kuea (短母音 uea)"],
    "กัว": ["kuaa (長母音 uaa)", "kua (短母音 ua)", "kiaa (長母音 iaa)", "kueaa (長母音 ueaa)"],
    "กิว": ["kiw (特殊母音 iu)", "kaw (短母音 aw)", "kay (特殊母音 ai)", "kui (特殊母音 ui)"],
    "กัย": ["kay (特殊母音 ai)", "kaw (短母音 aw)", "kaaw (長母音 aaw)", "kiw (特殊母音 iu)"],
    "ใก": ["kai (特殊母音 ai / 巻きのマイムアン)", "kai (特殊母音 ai / 結びのマイマライ)", "kam (特殊母音 am)", "kaaw (長母音 aaw)"],
    "ไก": ["kai (特殊母音 ai / 結びのマイマライ)", "kai (特殊母音 ai / 巻きのマイムアン)", "kam (特殊母音 am)", "ka (短母音 a)"],
    "กํา": ["kam (特殊母音 am)", "kai (特殊母音 ai)", "kaw (短母音 aw)", "ka (短母音 a)"],
    "กาว": ["kaaw (特殊母音 aaw)", "kaw (短母音 aw)", "kiw (特殊母音 iu)", "koo (長母音 oo)"],
    "กุย": ["kui (特殊母音 ui)", "kuay (特殊母音 uay)", "koey (特殊母音 oey)", "kiw (特殊母音 iu)"],
    "เกย": ["koey (特殊母音 oey)", "kui (特殊母音 ui)", "keay (特殊母音 eay)", "kiaa (長母音 iaa)"]
}

# --- セッション状態の初期化 ---
if "mode" not in st.session_state:
    st.session_state.mode = "すべて"
if "quiz_font" not in st.session_state:
    st.session_state.quiz_font = "標準 (教科書体)"
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.choices = []
    st.session_state.answered = False
    st.session_state.feedback = ""

def get_current_pool():
    if st.session_state.mode == "子音のみ":
        return THAI_CONSONANTS
    elif st.session_state.mode == "母音のみ":
        return THAI_VOWELS
    else:
        return {**THAI_CONSONANTS, **THAI_VOWELS}

def next_question():
    pool = get_current_pool()
    st.session_state.current_char = random.choice(list(pool.keys()))
    st.session_state.answered = False
    st.session_state.feedback = ""
    
    options = pool[st.session_state.current_char].copy()
    correct = options[0]
    random.shuffle(options)
    st.session_state.choices = options
    st.session_state.correct_answer = correct

if "current_char" not in st.session_state or not st.session_state.choices:
    next_question()

# --- UIレイアウト ---
st.title("🇹🇭 タイ文字究極マスター Pro")

# サイドバー設定
with st.sidebar:
    st.header("⚙️ アプリ設定")
    old_mode = st.session_state.mode
    st.session_state.mode = st.radio("出題範囲", ["すべて", "子音のみ", "母音のみ"])
    
    st.markdown("---")
    st.header("🎨 クイズのフォント")
    st.session_state.quiz_font = st.radio(
        "出題時の見た目を変える：", 
        ["標準 (教科書体)", "手書き風 (Itim)", "丸なしモダン (Kanit)"]
    )
    st.caption("※丸なしモダンにすると、タイの街中の看板レベルの難易度になります！")
    
    if old_mode != st.session_state.mode:
        next_question()
        st.rerun()
        
    if st.button("スコアをリセット"):
        st.session_state.score = 0
        st.session_state.total = 0
        next_question()
        st.rerun()

# スコア表示
st.write(f"成績: **{st.session_state.score} / {st.session_state.total}** 問正解")

st.markdown("---")

# 出題フォントのクラス決定
font_class = "font-standard"
if st.session_state.quiz_font == "手書き風 (Itim)":
    font_class = "font-hand"
elif st.session_state.quiz_font == "丸なしモダン (Kanit)":
    font_class = "font-modern"

# クイズ文字の表示（選択されたフォントが強制適用されます）
st.markdown(
    f"<h1 class='{font_class}' style='text-align: center; font-size: 130px; color: #DC2626; margin: 20px 0;'>{st.session_state.current_char}</h1>", 
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
            st.session_state.feedback = "⭕ 正解です！"
        else:
            st.session_state.feedback = f"❌ 残念！正解は 「{st.session_state.correct_answer}」 です。"
        st.rerun()

# 結果表示 ＆ 【答え合わせ時に3つのフォントを同時比較！】
if st.session_state.answered:
    if "⭕" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)
    
    # 🌟 ここが目玉機能：正解・不正解のあとに、3つのフォントを並べて比較表示！
    st.write("🔍 **フォントによる形の違いを比較してみよう：**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='font-box'><p style='font-size:12://px; color:gray;'>標準</p><h2 class='font-standard'>{st.session_state.current_char}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='font-box'><p style='font-size:12px; color:gray;'>手書き風</p><h2 class='font-hand'>{st.session_state.current_char}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='font-box'><p style='font-size:12px; color:gray;'>丸なし(看板)</p><h2 class='font-modern'>{st.session_state.current_char}</h2></div>", unsafe_allow_html=True)
        
    if st.button("次の問題へ進む ➡️", use_container_width=True):
        next_question()
        st.rerun()