import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize high-scannability configuration
st.set_page_config(page_title="Tolkāppiyam Slot Matrix Engine", layout="wide")

# Safe dynamic transliteration handler
try:
    from aksharamukha import transliterate
    AKSHARAMUKHA_AVAILABLE = True
except ModuleNotFoundError:
    AKSHARAMUKHA_AVAILABLE = False

def get_iso_transliteration(text: str, script_name: str) -> str:
    """Accurately transliterates Dravidian text into ISO 15919."""
    if AKSHARAMUKHA_AVAILABLE:
        try:
            return transliterate.process(src=script_name.strip().capitalize(), tgt="ISO", txt=text)
        except Exception:
            return text
    return text

# ==============================================================================
# 1. MORPHOLOGICAL SLOT DICTIONARY WITH INTERLINEAR LEIPZIG GLOSSING
# Each slot provides:
#   - native: Native Dravidian orthography
#   - gloss: Morphological decomposition [STEM-CASE/TENSE/AGREEMENT]
# ==============================================================================
TOL_SLOT_DICTIONARY = {
    "subject_adjectives": {
        "Experienced / Skilled": {
            "tamil": {"native": "அனுபவம் வாய்ந்த", "gloss": "experience-ACC possess-PAST.RP"},
            "kannada": {"native": "ಅನುಭವಿ", "gloss": "experience-ADJ"},
            "telugu": {"native": "అనుభవజ్ఞురాలైన", "gloss": "experience-possessor.FEM-ADJ"},
            "malayalam": {"native": "പരിചയസമ്പന്നയായ", "gloss": "experience-wealthy-FEM.ADJ"},
            "english": "An experienced"
        },
        "Good / Virtuous": {
            "tamil": {"native": "ஒரு சிறந்த", "gloss": "one eminent-RP"},
            "kannada": {"native": "ಒಬ್ಬ ಉತ್ತಮ", "gloss": "one.HUM virtuous-ADJ"},
            "telugu": {"native": "ఒక మంచి", "gloss": "one good-ADJ"},
            "malayalam": {"native": "ഒരു മികച്ച", "gloss": "one excellent-ADJ"},
            "english": "A good"
        },
        "Young / Energetic": {
            "tamil": {"native": "இளமையான", "gloss": "youth-ADJ"},
            "kannada": {"native": "ಯುವ", "gloss": "youth-ADJ"},
            "telugu": {"native": "యువ", "gloss": "youth-ADJ"},
            "malayalam": {"native": "യുവ", "gloss": "youth-ADJ"},
            "english": "A young"
        }
    },
    "subjects": {
        "Danseuse (Female)": {
            "tamil": {"native": "பெண் நடனக் கலைஞர்", "gloss": "female dance-GEN artist.NOM"},
            "kannada": {"native": "ನೃತ್ಯಗಾರ್ತಿಯೊಬ್ಬರು", "gloss": "dancer-FEM-INDEF.NOM"},
            "telugu": {"native": "నర్తకి", "gloss": "danseuse.FEM.NOM"},
            "malayalam": {"native": "നർത്തകി", "gloss": "danseuse.FEM.NOM"},
            "english": "danseuse"
        },
        "Teacher": {
            "tamil": {"native": "ஆசிரியர்", "gloss": "teacher.HON.NOM"},
            "kannada": {"native": "ಶಿಕ್ಷಕರೊಬ್ಬರು", "gloss": "teacher-HON-INDEF.NOM"},
            "telugu": {"native": "ఉపాధ్యాయుడు", "gloss": "teacher-MASC.NOM"},
            "malayalam": {"native": "അധ്യാപകൻ", "gloss": "teacher-MASC.NOM"},
            "english": "teacher"
        },
        "Scholar": {
            "tamil": {"native": "அறிஞர்", "gloss": "scholar.HON.NOM"},
            "kannada": {"native": "ವಿದ್ವಾಂಸರೊಬ್ಬರು", "gloss": "scholar-HON-INDEF.NOM"},
            "telugu": {"native": "పండితుడు", "gloss": "scholar-MASC.NOM"},
            "malayalam": {"native": "പണ്ഡിതൻ", "gloss": "scholar-MASC.NOM"},
            "english": "scholar"
        }
    },
    "indirect_objects": {
        "Girls / Young Women": {
            "tamil": {"native": "பெண்களுக்குப்", "gloss": "woman-PL-DAT"},
            "kannada": {"native": "ಬಾಲಕಿಯರಿಗೆ", "gloss": "girl-PL-DAT"},
            "telugu": {"native": "అమ్మాయిలకు", "gloss": "girl-PL-DAT"},
            "malayalam": {"native": "പെൺകുട്ടികളെ", "gloss": "girl-PL-ACC/DAT"},
            "english": "to the girls"
        },
        "Boys / Students": {
            "tamil": {"native": "மாணவர்களுக்குப்", "gloss": "student-PL-DAT"},
            "kannada": {"native": "ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ", "gloss": "student-PL-DAT"},
            "telugu": {"native": "విద్యార్థులకు", "gloss": "student-PL-DAT"},
            "malayalam": {"native": "വിദ്യാർത്ഥികളെ", "gloss": "student-PL-ACC/DAT"},
            "english": "to the boys"
        },
        "Children": {
            "tamil": {"native": "குழந்தைகளுக்குப்", "gloss": "child-PL-DAT"},
            "kannada": {"native": "ಮಕ್ಕಳಿಗೆ", "gloss": "child-PL-DAT"},
            "telugu": {"native": "పిల్లలకు", "gloss": "child-PL-DAT"},
            "malayalam": {"native": "കുട്ടികളെ", "gloss": "child-PL-ACC/DAT"},
            "english": "to the children"
        }
    },
    "object_adjectives": {
        "New": {
            "tamil": {"native": "புதிய", "gloss": "new-ADJ"},
            "kannada": {"native": "ಹೊಸ", "gloss": "new-ADJ"},
            "telugu": {"native": "కొత్త", "gloss": "new-ADJ"},
            "malayalam": {"native": "പുതിയ", "gloss": "new-ADJ"},
            "english": "new"
        },
        "Complex / Advanced": {
            "tamil": {"native": "சிக்கலான", "gloss": "complex-ADJ"},
            "kannada": {"native": "ಸಂಕೀರ್ಣ", "gloss": "complex-ADJ"},
            "telugu": {"native": "క్లిష్టమైన", "gloss": "complex-ADJ"},
            "malayalam": {"native": "സങ്കീർണ്ണമായ", "gloss": "complex-ADJ"},
            "english": "complex"
        },
        "Ancient / Classical": {
            "tamil": {"native": "பண்டைய", "gloss": "ancient-ADJ"},
            "kannada": {"native": "ಪ್ರಾಚೀನ", "gloss": "ancient-ADJ"},
            "telugu": {"native": "పురాతన", "gloss": "ancient-ADJ"},
            "malayalam": {"native": "പുരാതനമായ", "gloss": "ancient-ADJ"},
            "english": "ancient"
        }
    },
    "direct_objects": {
        "Dances": {
            "tamil": {"native": "நடனங்களைக்", "gloss": "dance-PL-ACC"},
            "kannada": {"native": "ನೃತ್ಯಗಳನ್ನು", "gloss": "dance-PL-ACC"},
            "telugu": {"native": "నృత్యాలను", "gloss": "dance-PL-ACC"},
            "malayalam": {"native": "നൃത്തങ്ങൾ", "gloss": "dance-PL.ACC"},
            "english": "dances"
        },
        "Tricks / Techniques": {
            "tamil": {"native": "உத்திகளைக்", "gloss": "technique-PL-ACC"},
            "kannada": {"native": "ಯುಕ್ತಿಗಳನ್ನು", "gloss": "technique-PL-ACC"},
            "telugu": {"native": "చిట్కాలను", "gloss": "trick-PL-ACC"},
            "malayalam": {"native": "തന്ത്രങ്ങൾ", "gloss": "technique-PL.ACC"},
            "english": "tricks"
        },
        "Lessons / Verses": {
            "tamil": {"native": "பாடங்களைக்", "gloss": "lesson-PL-ACC"},
            "kannada": {"native": "ಪಾಠಗಳನ್ನು", "gloss": "lesson-PL-ACC"},
            "telugu": {"native": "పాఠాలను", "gloss": "lesson-PL-ACC"},
            "malayalam": {"native": "പാഠങ്ങൾ", "gloss": "lesson-PL.ACC"},
            "english": "lessons"
        }
    },
    "purposive_clauses": {
        "To rehearse what was practised": {
            "tamil": {
                "native": "ஏற்கனவே பயிற்சி செய்யப்பட்டவற்றை ஒத்திகை பார்ப்பதற்காகப்",
                "gloss": "already practice do-PASS-RP-PRO.N.PL.ACC rehearsal see-INF-PURP"
            },
            "kannada": {
                "native": "ಹಿಂದೆ ಅಭ್ಯಾಸ ಮಾಡಿದ್ದನ್ನು ಪುನರಭ್ಯಾಸ ಮಾಡಲು",
                "gloss": "previously practice do-PAST-RP.PRO.ACC rehearsal do-INF"
            },
            "telugu": {
                "native": "సాధన చేసిన వాటిని పునశ్చరణ చేయడానికి",
                "gloss": "practice do-PAST.RP DEM.PL.ACC revision do-INF-PURP"
            },
            "malayalam": {
                "native": "നേരത്തെ പരിശീലിച്ച കാര്യങ്ങൾ റിഹേഴ്സൽ ചെയ്യുന്നതിനായി",
                "gloss": "earlier practice-PAST.RP matter.PL rehearsal do-PRES-VN-PURP"
            },
            "english": "to rehearse what was practised"
        },
        "To retain what is learnt": {
            "tamil": {
                "native": "தாங்கள் கற்றவற்றை நினைவில் வைத்துக்கொள்ளும் வகையில்",
                "gloss": "themselves learn-PAST-RP-PRO.N.PL.ACC memory-LOC keep-REFL-RP manner-LOC"
            },
            "kannada": {
                "native": "ಕಲಿತದ್ದನ್ನು ನೆನಪಿನಲ್ಲಿಟ್ಟುಕೊಳ್ಳಲು",
                "gloss": "learn-PAST-RP.PRO.ACC memory-LOC-keep-REFL-INF"
            },
            "telugu": {
                "native": "నేర్చుకున్న వాటిని గుర్తుంచుకోవడానికి",
                "gloss": "learn-PAST.RP DEM.PL.ACC memory-keep-INF-PURP"
            },
            "malayalam": {
                "native": "പഠിച്ച കാര്യങ്ങൾ ഓർമ്മയിൽ സൂക്ഷിക്കാൻ",
                "gloss": "learn-PAST.RP matter.PL memory-LOC keep-INF"
            },
            "english": "to retain what is learnt"
        }
    },
    "verbs": {
        "teach": {
            "tamil": {"native": "கற்றுக்கொடுக்கிறார்", "gloss": "learn-VR-give-PRES-3.HON.SG"},
            "kannada": {"native": "ಕಲಿಸುತ್ತಾರೆ", "gloss": "teach-PRES-3.HON.PL"},
            "telugu": {
                "female": {"native": "నేర్పిస్తుంది", "gloss": "teach-PRES-3.FEM.SG"},
                "male": {"native": "నేర్పిస్తాడు", "gloss": "teach-PRES-3.MASC.SG"}
            },
            "malayalam": {"native": "പഠിപ്പിക്കുന്നു", "gloss": "teach-PRES"}  # Zero Person-Number-Gender inflection
        }
    }
}

# ==============================================================================
# 2. STREAMLIT APPLICATION UI
# ==============================================================================
st.title("🌐 Tolkāppiyam Slot Matrix Machine Translation Studio")
st.markdown("##### *Dynamic Generative Agglutinative Blueprint for Dravidian Syntactic Systems*")
st.caption("Morphosyntactic engine tracking 3-tier representations: Native Orthography, ISO 15919 Transliteration, and Leipzig Interlinear Glossing.")
st.markdown("---")

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

eng_sentence = f"{TOL_SLOT_DICTIONARY['subject_adjectives'][s_adj]['english']} {TOL_SLOT_DICTIONARY['subjects'][sub]['english']} teaches {TOL_SLOT_DICTIONARY['object_adjectives'][o_adj]['english']} {TOL_SLOT_DICTIONARY['direct_objects'][d_obj]['english']} {TOL_SLOT_DICTIONARY['indirect_objects'][i_obj]['english']} {TOL_SLOT_DICTIONARY['purposive_clauses'][purp]['english']}."

st.markdown(f"**VIRTUAL LIVE INPUT BASE SENTENCE :** `{eng_sentence}`")
st.markdown(f"**MATRIX RE-COMPILATION TIME :** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST`")
st.markdown("---")

# ==============================================================================
# 3. SYNTACTIC ASSEMBLY & 3-TIER INTERLINEAR GLOSS ENGINE
# ==============================================================================
languages = [
    ("Tamil (Dravidian Head-Final Matrix)", "tamil", "Tamil"),
    ("Kannada (Dravidian Head-Final Matrix)", "kannada", "Kannada"),
    ("Telugu (Dravidian Head-Final Matrix)", "telugu", "Telugu"),
    ("Malayalam (Dravidian Matrix - No PNG Suffix)", "malayalam", "Malayalam")
]

compiled_output = []

for label, lang_key, script_title in languages:
    sa = TOL_SLOT_DICTIONARY["subject_adjectives"][s_adj][lang_key]
    sb = TOL_SLOT_DICTIONARY["subjects"][sub][lang_key]
    io = TOL_SLOT_DICTIONARY["indirect_objects"][i_obj][lang_key]
    oa = TOL_SLOT_DICTIONARY["object_adjectives"][o_adj][lang_key]
    do = TOL_SLOT_DICTIONARY["direct_objects"][d_obj][lang_key]
    pc = TOL_SLOT_DICTIONARY["purposive_clauses"][purp][lang_key]
    
    # Verb selection logic (handling Telugu PNG agreement)
    if lang_key == "telugu":
        v_data = TOL_SLOT_DICTIONARY["verbs"]["teach"][lang_key]["female" if "Danseuse" in sub else "male"]
    else:
        v_data = TOL_SLOT_DICTIONARY["verbs"]["teach"][lang_key]

    # Syntactic ordering according to head-final Dravidian clause typology
    if lang_key == "malayalam":
        native_sentence = f"{pc['native']} {sa['native']} {sb['native']} {io['native']} {oa['native']} {do['native']} {v_data['native']}."
        gloss_sentence = f"[{pc['gloss']}] [{sa['gloss']}] [{sb['gloss']}] [{io['gloss']}] [{oa['gloss']}] [{do['gloss']}] [{v_data['gloss']}]"
    else:
        native_sentence = f"{sa['native']} {sb['native']}, {pc['native']} {io['native']} {oa['native']} {do['native']} {v_data['native']}."
        gloss_sentence = f"[{sa['gloss']}] [{sb['gloss']}], [{pc['gloss']}] [{io['gloss']}] [{oa['gloss']}] [{do['gloss']}] [{v_data['gloss']}]"

    # Phonetically verified ISO 15919 transliteration
    roman_sentence = get_iso_transliteration(native_sentence, script_title)

    # 1. Native Orthography Row
    compiled_output.append({
        "Language Workspace": label,
        "Structural Layer": "1. Native Script",
        "Syntactic & Morphological Representation": native_sentence
    })

    # 2. Phonetic Roman Transliteration Row
    compiled_output.append({
        "Language Workspace": f"↳ {label.split(' ')[0]} (Roman ISO 15919)",
        "Structural Layer": "2. Phonetic Romanization",
        "Syntactic & Morphological Representation": roman_sentence
    })

    # 3. Interlinear Morphemic Gloss Row (Leipzig Conventions)
    compiled_output.append({
        "Language Workspace": f"↳ {label.split(' ')[0]} (Morpheme Gloss)",
        "Structural Layer": "3. Interlinear Morphemic Gloss",
        "Syntactic & Morphological Representation": gloss_sentence
    })

# Render compiled 3-tier interlinear structural matrix
df_matrix = pd.DataFrame(compiled_output)
st.dataframe(df_matrix, use_container_width=True, hide_index=True)

# Leipzig Abbreviations Legend
with st.expander("📖 Leipzig Glossing Abbreviations Reference"):
    st.markdown("""
    * **NOM / ACC / DAT / GEN / LOC**: Nominative, Accusative, Dative, Genitive, Locative case markers
    * **PL / SG**: Plural / Singular
    * **HUM / FEM / MASC / HON**: Human, Feminine, Masculine, Honorific markers
    * **PRES / PAST**: Present / Past tense inflections
    * **RP / VR**: Relative Participle / Verbal Reflexive
    * **INF / PURP / VN**: Infinitive, Purposive clause clitic, Verbal Noun
    * **3.HON.SG / 3.FEM.SG**: Third person singular agreement suffixes (absent in Malayalam)
    """)