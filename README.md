# CV tracking system

**Run the following in the Command Prompt**

```bash
conda create --name cv_genius python=3.10 -y
```

```bash
conda activate cv_genius
```

```bash
pip install -r requirements.txt
```

```bash
pip install -U textblob
```

```bash
pip install python-dotenv streamlit Pillow pdf2image google-generativeai textblob
```

```bash
streamlit run app.py
```


1. The projects tells about the summary of the resume to which jobs it is a great fit or to which jobs it can be applied.
2. Based on the Job Description provided it tells about in which particular areas the resume can be modified or upgraded.
3. It basically traces the CV of an individual and predicts the match with the provided job description.
4. Also predicts the polarity and the sentiment analysis for the given CV.