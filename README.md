# The Match Lab

**What makes two people want to see each other again?** The Match Lab is an interactive Streamlit data app exploring that question with records from a Columbia University speed-dating experiment.

It compares stated partner preferences with date ratings and mutual-match outcomes. Visitors can filter the sample by participant gender, age, and study wave, explore interactive charts, and try a descriptive scenario based on historical dates that met selected rating cutoffs.

## What the app includes

- Summary metrics for the filtered sample
- Match rates by overall liking score
- A comparison of mutual and one-sided yes decisions
- Charts comparing stated preferences and partner ratings
- A scenario explorer that reports the observed match rate among records meeting chosen rating thresholds
- Notes on cleaning, data source, and limits of the study

The scenario explorer is descriptive; it is not a personal prediction. The dataset is historical and comes from students at one university, so results should not be generalized to all people or relationships.

## Dataset

The bundled CSV is the Speed Dating dataset distributed through [DataHub's OpenML datasets collection](https://datahub.io/core/openml-datasets/r/SpeedDating.csv). Columbia University describes the original speed-dating study as events conducted from 2002 to 2004 in its [Big Data Analytics dataset list](https://www.ee.columbia.edu/~cylin/course/bigdata/getdatasetinfo.html). The academic research background is Fisman, Iyengar, Kamenica, and Simonson, “Gender Differences in Mate Selection: Evidence from a Speed Dating Experiment,” *Quarterly Journal of Economics* (2006).

One row is a participant's record of one speed date. The app converts key numeric fields, removes records missing the match outcome, participant age, or gender, and uses the recorded `match` field for mutual-match comparisons. Some source column names preserve the original spelling, including `sinsere_o` and `ambitous_o`.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this folder to a public GitHub repository.
2. In [Streamlit Community Cloud](https://share.streamlit.io/), create an app from that repository.
3. Select `main` as the branch and `app.py` as the app file.
4. Submit both the GitHub repository URL (clone link) and the deployed Streamlit app URL.
