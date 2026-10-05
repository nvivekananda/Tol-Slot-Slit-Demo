import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize high-scannability configuration
st.set_page_config(page_title="Tolkāppiyam Slot Matrix Engine", layout="wide")

# ==============================================================================
# PROJECT: Dravidian Cross-Family Morphological Slot Matrix Studio
# COMPONENT: Tolkāppiyam-Inspired Agglutinative Structural Generator
# VERSION: 15.0.0
# TIMESTAMP: 2026-10-02 19:15:00 IST
# AUTHOR: Collaborative AI Framework
# ==============================================================================

# Expanded Morphological Rules Dictionary
TOL_SLOT_DICTIONARY = {
    "subject_adjectives": {
        "Experienced / Skilled": {
            "tamil": "அனுபவம் வாய்ந்த",
            "kannada": "ಅನುಭವಿ",
            "telugu": "అనుభవజ్ఞురాలైన",
            "malayalam": "പരിചയസമ്പന്നയായ",
            "english": "An experienced"
        },
        "Good / Virtuous": {
            "tamil": "ஒரு சிறந்த",
            "kannada": "ಒಬ್ಬ ಉತ್ತಮ",
            "telugu": "ఒక మంచి",
            "malayalam": "ഒരു മികച്ച",
            "english": "A good"
        },
        "Young / Energetic": {
            "tamil": "இளமையான",
            "kannada": "ಯುವ",
            "telugu": "యువ",
            "malayalam": "യുവ",
            "english": "A young"
        }
    },
    "subjects": {
        "Danseuse (Female)": {
            "tamil": "பெண் நடனக் கலைஞர்",
            "kannada": "ನೃತ್ಯಗಾರ್ತಿಯೊಬ್ಬರು",
            "telugu": "నర్తకి",
            "malayalam": "നർത്തകി",
            "english": "danseuse"
        },
        "Teacher": {
            "tamil": "ஆசிரியர்",
            "kannada": "ಶಿಕ್ಷಕರೊಬ್ಬರು",
            "telugu": "ఉపాధ్యಾಯుడు",
            "malayalam": "അധ്യാപകൻ",
            "english": "teacher"
        },
        "Scholar": {
            "tamil": "அறிஞர்",
            "kannada": "ವಿದ್ವಾಂಸರೊಬ್ಬರು",
            "telugu": "పండితుడు",
            "malayalam": "പണ്ഡിതൻ",
            "english": "scholar"
        }
    },
    "indirect_objects": {
        "Girls / Young Women": {
            "tamil": "பெண்களுக்குப்",
            "kannada": "ಬಾಲಕಿಯರಿಗೆ",
            "telugu": "అమ్మాయిలకు",
            "malayalam": "പെൺകുട്ടികളെ",
            "english": "to the girls"
        },
        "Boys / Students": {
            "tamil": "மாணவர்களுக்குப்",
            "kannada": "ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ",
            "telugu": "విద్యార్థులకు",
            "malayalam": "വിദ്യാർത്ഥികളെ",
            "english": "to the boys"
        },
        "Children": {
            "tamil": "குழந்தைகளுக்குப்",
            "kannada": "ಮಕ್ಕಳಿಗೆ",
            "telugu": "పిల్లలకు",
            "malayalam": "കുട്ടികളെ",
            "english": "to the children"
        }
    },
    "object_adjectives": {
        "New": {
            "tamil": "புதிய",
            "kannada": "ಹೊಸ",
            "telugu": "కొత్త",
            "malayalam": "പുതിയ",
            "english": "new"
        },
        "Complex / Advanced": {
            "tamil": "சிக்கலான",
            "kannada": "ಸಂಕೀರ್ಣ",
            "telugu": "క్లిష్టమైన",
            "malayalam": "സങ്കീർണ്ണമായ",
            "english": "complex"
        },
        "Ancient / Classical": {
            "tamil": "பண்டைய",
            "kannada": "ಪ್ರಾಚೀನ",
            "telugu": "పురాతన",
            "malayalam": "പുരാതനമായ",
            "english": "ancient"
        }
    },
    "direct_objects": {
        "Dances": {
            "tamil": "நடனங்களைக்",
            "kannada": "ನೃತ್ಯಗಳನ್ನು",
            "telugu": "నృత్యాలను",
            "malayalam": "നൃത്തങ്ങൾ",
            "english": "dances"
        },
        "Tricks / Techniques": {
            "tamil": "உத்திகளைக்",
            "kannada": "ಯುಕ್ತಿಗಳನ್ನು",
            "telugu": "చిట్కాలను",
            "malayalam": "തന്ത്രങ്ങൾ",
            "english": "tricks"
        },
        "Lessons / Verses": {
            "tamil": "பாடங்களைக்",
            "kannada": "ಪಾಠಗಳನ್ನು",
            "telugu": "పాఠాలను",
            "malayalam": "പാഠങ്ങൾ",
            "english": "lessons"
        }
    },
    "purposive_clauses": {
        "To rehearse what was practised": {
            "tamil": "ஏற்கனவே பயிற்சி செய்யப்பட்டவற்றை ஒத்திகை பார்ப்பதற்காகப்",
            "kannada": "ಹಿಂದೆ ಅಭ್ಯಾಸ ಮಾಡಿದ್ದನ್ನು ಪುನರಭ್ಯಾಸ ಮಾಡಲು",
            "telugu": "సాధన చేసిన వాటిని పునశ్చరణ చేయడానికి",
            "malayalam": "നേരത്തെ പരിശീലിച്ച കാര്യങ്ങൾ റിഹേഴ്സൽ ചെയ്യുന്നതിനായി",
            "english": "to rehearse what was practised"
        },
        "To retain what is learnt": {
            "tamil": "தாங்கள் கற்றவற்றை நினைவில் வைத்துக்கொள்ளும் வகையில்",
            "kannada": "ಕಲಿತದ್ದನ್ನು ನೆನಪಿನಲ್ಲಿಟ್ಟುಕೊಳ್ಳಲು",
            "telugu": "నేర్చుకున్న వాటిని గుర్తుంచుకోవడానికి",
            "malayalam": "പഠിച്ച കാര്യങ്ങൾ ഓർമ്മയിൽ സൂക്ഷിക്കാൻ",
            "english": "to retain what is learnt"
        }
    },
    "verbs": {
        "teach": {
            "tamil": "கற்றுக்கொடுக்கிறார்",
            "kannada": "ಕಲಿಸುತ್ತಾರೆ",
            "telugu": "నేర్పిస్తుంది / నేర్పిస్తాడు",
            "malayalam": "പഠിപ്പിക്കുന്നു"
        }
    }
}

# --- APPLICATION UI LAYOUT ---
st.title("🌐 Tolkāppiyam Slot Matrix Machine Translation Studio")
st.markdown("##### *Dynamic Generative Agglutinative Blueprint for Dravidian Syntactic Systems*")
st.text("==========================================================================")

# 1. Structural Slot Selectors arranged in responsive columns
st.markdown("### 🛠️ Configure Syntactic Morphological Matrix Slots:")
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    s_adj = st.selectbox("1. Subject Adjective", list(TOL_SLOT_DICTIONARY["subject_adjectives"].keys()), index=0)
with col2:
    sub = st.selectbox("2. Actor Subject (Noun)", list(TOL_SLOT_DICTIONARY["subjects"].keys()), index=0)
with col3:
    i_obj = st.selectbox("3. Recipient Indirect Object", list(TOL_SLOT_DICTIONARY["indirect_objects"].keys()), index=0)
with col4:
    o_adj = st.selectbox("4. Object Attribute (Adjective)", list(TOL_SLOT_DICTIONARY["object_adjectives"].keys()), index=0)
with col5:
    d_obj = st.selectbox("5. Goal Direct Object", list(TOL_SLOT_DICTIONARY["direct_objects"].keys()), index=0)
with col6:
    purp = st.selectbox("6. Purposive Action Particle/Clause", list(TOL_SLOT_DICTIONARY["purposive_clauses"].keys()), index=0)

st.text("===============================================================================================")

# 2. Reconstruct the dynamically synced English Context Sentence
eng_sentence = f"{TOL_SLOT_DICTIONARY['subject_adjectives'][s_adj]['english']} {TOL_SLOT_DICTIONARY['subjects'][sub]['english']} teaches {TOL_SLOT_DICTIONARY['object_adjectives'][o_adj]['english']} {TOL_SLOT_DICTIONARY['direct_objects'][d_obj]['english']} {TOL_SLOT_DICTIONARY['indirect_objects'][i_obj]['english']} {TOL_SLOT_DICTIONARY['purposive_clauses'][purp]['english']}."

st.markdown(f"**VIRTUAL LIVE INPUT BASE SENTENCE :** `{eng_sentence}`")
st.markdown(f"**MATRIX RE-COMPILATION TIME :** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST`")
st.text("===============================================================================================")

# 3. Structural Assembly Engine 
# Dravidian Syntactic Parameter Setup: Left-Branching Head-Final Structure
# Typical Structural Sequence: [Subject Adjective] [Subject] + [Purposive Modifier Clause] + [Indirect Object] + [Object Adjective] + [Direct Object] + [Verb Engine]

languages = [
    ("Tamil (Dravidian Head-Final Matrix)", "tamil"),
    ("Kannada (Dravidian Head-Final Matrix)", "kannada"),
    ("Telugu (Dravidian Head-Final Matrix)", "telugu"),
    ("Malayalam (Dravidian Matrix - No PNG Suffix)", "malayalam")
]

compiled_output = []

for label, lang_key in languages:
    sa = TOL_SLOT_DICTIONARY["subject_adjectives"][s_adj][lang_key]
    sb = TOL_SLOT_DICTIONARY["subjects"][sub][lang_key]
    io = TOL_SLOT_DICTIONARY["indirect_objects"][i_obj][lang_key]
    oa = TOL_SLOT_DICTIONARY["object_adjectives"][o_adj][lang_key]
    do = TOL_SLOT_DICTIONARY["direct_objects"][d_obj][lang_key]
    pc = TOL_SLOT_DICTIONARY["purposive_clauses"][purp][lang_key]
    
    # Custom contextual choice handling for Telugu verbs based on noun gender proxy
    v_engine = TOL_SLOT_DICTIONARY["verbs"]["teach"][lang_key]
    if lang_key == "telugu":
        v_engine = "నేర్పిస్తుంది" if "Danseuse" in sub else "నేర్పిస్తాడు"

    # Assemble using highly refined modern natural phrasing order
    if lang_key == "tamil":
        # Structure: [Sub Adj] [Sub], [Purposive] [Indirect Obj] [Obj Adj] [Direct Obj] [Verb]
        sentence = f"{sa} {sb}, {pc} {io} {oa} {do} {v_engine}."
    elif lang_key == "kannada":
        sentence = f"{sa} {sb}, {pc} {io} {oa} {do} {v_engine}."
    elif lang_key == "telugu":
        sentence = f"{sa} {sb}, {pc} {io} {oa} {do} {v_engine}."
    elif lang_key == "malayalam":
        sentence = f"{pc} {sa} {sb} {io} {oa} {do} {v_engine}."

    compiled_output.append({
        "Dravidian Language Subsystem Workspace": label,
        "Generated Syntactic Sentence Representation": sentence
    })

# Render compiled structural matrix as an interactive responsive DataFrame
df_matrix = pd.DataFrame(compiled_output)
st.dataframe(df_matrix, use_container_width=True, hide_index=True)
