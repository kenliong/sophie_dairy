import pandas as pd

def get_old_diary_entries():
    old_diary_entries = pd.read_csv("data/journal_entries_v2.csv")
    return old_diary_entries

mental_tendencies = [
'High Expectations',
'External Validation',
'Reluctance to Share',
'Expectation of Reciprocity',
'Guilt-trapping',
'Balancing Correction and Encouragement',
'Demotivation from Initial Failures',
'Perfectionism',
'Tunnel Vision',
'Self-efficacy',
'Learned Helplessness',
'Overanalysis',
'Fear of Failure',
'Risk Aversion',
'Impostor Syndrome',
'Distractibility',
'Multitasking'
]

emotions = [
"Happiness",
"Sadness",
"Anger",
"Fear",
"Surprise",
"Disgust",
"Love",
"Anticipation",
"Trust",
"Jealousy",
"Envy",
"Guilt",
"Shame",
"Relief",
"Pride",
"Contempt",
"Frustration",
"Boredom",
"Hope",
"Confusion",
"Embarrassment"
]