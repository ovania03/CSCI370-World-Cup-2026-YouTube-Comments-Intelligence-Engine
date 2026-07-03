# 📖 Usage Guide - World Cup 2026 Intelligence Engine

## Table of Contents
1. [Quick Start](#quick-start)
2. [Running the Pipeline](#running-the-pipeline)
3. [Using the Dashboard](#using-the-dashboard)
4. [API Setup (YouTube)](#api-setup-youtube)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Configuration](#advanced-configuration)

---

## 🚀 Quick Start

### First Time Setup (5 minutes)

```bash
# Step 1: Navigate to project directory
cd worldcup_analysis

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Download SpaCy model
python -m spacy download en_core_web_sm

# Step 4: Download NLTK data
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('stopwords')"

# Step 5: Run the dashboard
streamlit run dashboard.py
```

Your browser will open at `http://localhost:8501` 🎉

---

## 🔄 Running the Pipeline

### Option 1: Using Jupyter Notebook

1. **Open the notebook**:
   ```bash
   jupyter notebook "CSCI370_project_pipeline_final_1 (3).ipynb"
   ```

2. **Run cells in order**:
   - Cell 1-5: Import libraries and setup
   - Cell 6-10: Data scraping (requires YouTube API key)
   - Cell 11-15: Text preprocessing
   - Cell 16-20: Sentiment analysis
   - Cell 21-25: Named Entity Recognition
   - Cell 26-30: Topic modeling
   - Cell 31+: Save results

3. **Expected Runtime**: 10-15 minutes for full pipeline

### Option 2: Using Google Colab

1. Upload notebook to Google Colab
2. Mount Google Drive:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```
3. Upload data files to Drive
4. Run all cells

### Pipeline Outputs

After running the pipeline, you'll have:
- ✅ `worldcup_2026_comments.csv` - Raw comments
- ✅ `worldcup_2026_final.csv` - With sentiment
- ✅ `worldcup_2026_with_entities.csv` - With NER
- ✅ `worldcup_2026_with_topics.csv` - Final dataset

---

## 📊 Using the Dashboard

### Starting the Dashboard

```bash
streamlit run dashboard.py
```

### Dashboard Controls

#### 1. **Sidebar Filters**

**Sentiment Filter**:
- Select one or multiple: Positive, Negative, Neutral
- Default: All selected
- Use case: Focus on specific sentiment types

**Minimum Likes Slider**:
- Range: 0 to maximum likes in dataset
- Default: 0
- Use case: Filter high-engagement comments

#### 2. **KPI Cards** (Top Row)

Displays real-time metrics:
- **Positive %**: Percentage of positive comments
- **Negative %**: Percentage of negative comments
- **Avg Likes**: Average likes per filtered comment
- **Topics Found**: Number of unique topics

#### 3. **Sentiment Distribution Charts**

**Pie Chart**:
- Shows proportion of each sentiment
- Color coded: Green (positive), Red (negative), Gray (neutral)
- Hover for exact counts

**Histogram**:
- X-axis: VADER compound score (-1 to +1)
- Y-axis: Frequency
- Vertical lines at -0.05 and +0.05 (thresholds)

#### 4. **Keywords & Entities**

**Top Keywords**:
- Horizontal bar chart
- Shows 15 most frequent keywords
- Sorted by count

**Named Entities**:
- Extracted using SpaCy NER
- Examples: Player names, team names, locations
- Orange color scale

#### 5. **Topic Distribution**

- Bar chart of top 10 topics
- Topic IDs with frequencies
- Topics labeled as "Topic 0", "Topic 1", etc.
- Note: Topic -1 represents uncategorized comments

#### 6. **Top Comments Table**

Features:
- Shows 10 most-liked comments
- Columns: Author, Text, Sentiment, Like Count
- Color-coded by sentiment
- Background colors:
  - Light green: Positive
  - Light red: Negative
  - Light gray: Neutral

#### 7. **Semantic Search**

**How to Use**:
1. Type your question in the text box
2. Example queries:
   - "What do fans think about Messi?"
   - "Opinions on USA hosting"
   - "Canada team performance"
   - "Stadium complaints"

**How It Works**:
- Fast keyword-based matching
- Searches across all comment text
- Returns top 8 most relevant comments
- Ranked by keyword match score and likes

**Search Tips**:
- Use specific keywords (e.g., "Ronaldo goals")
- Try player names, team names, cities
- Use multiple words for better results
- No need for exact phrases

#### 8. **Raw Data Browser**

- Expandable section at bottom
- Full dataset with all columns
- Sortable by clicking column headers
- Searchable using Streamlit's built-in search
- Export capability (click ⋮ menu)

---

## 🔑 API Setup (YouTube)

### Getting YouTube API Key

1. **Go to Google Cloud Console**:
   - Visit: https://console.cloud.google.com/

2. **Create a New Project**:
   - Click "Select a project" → "New Project"
   - Name: "WorldCup-NLP"
   - Click "Create"

3. **Enable YouTube Data API v3**:
   - Navigate to "APIs & Services" → "Library"
   - Search "YouTube Data API v3"
   - Click "Enable"

4. **Create Credentials**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy the API key

5. **Secure Your API Key**:
   ```bash
   # Create .env file
   echo YOUTUBE_API_KEY=YOUR_API_KEY_HERE > .env
   ```

6. **Use in Notebook**:
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   api_key = os.getenv("YOUTUBE_API_KEY")
   ```

### API Quota Limits

- **Daily Quota**: 10,000 units
- **Comments.list**: ~1 unit per request
- **Can scrape**: ~8,000-10,000 comments/day
- **Tip**: Spread scraping across multiple days for large datasets

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. **Dashboard Won't Start**

**Error**: `ModuleNotFoundError: No module named 'streamlit'`

**Solution**:
```bash
pip install streamlit
# Or reinstall all dependencies
pip install -r requirements.txt
```

#### 2. **SpaCy Model Not Found**

**Error**: `Can't find model 'en_core_web_sm'`

**Solution**:
```bash
python -m spacy download en_core_web_sm
```

#### 3. **NLTK Data Missing**

**Error**: `Resource vader_lexicon not found`

**Solution**:
```python
import nltk
nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('punkt')
```

#### 4. **Search Takes Too Long**

**Problem**: Semantic search is slow

**Solution**: 
- Already fixed in updated dashboard.py
- Uses fast keyword search instead of vector DB
- Should return results in <1 second

#### 5. **CSV File Not Found**

**Error**: `FileNotFoundError: worldcup_2026_with_topics.csv`

**Solution**:
- Ensure you've run the pipeline notebook first
- Check file is in same directory as dashboard.py
- Verify file name matches exactly

#### 6. **Port Already in Use**

**Error**: `Address already in use: Port 8501`

**Solution**:
```bash
# Use different port
streamlit run dashboard.py --server.port 8502

# Or kill existing process (Windows)
netstat -ano | findstr :8501
taskkill /PID <PID_NUMBER> /F
```

#### 7. **Memory Error**

**Error**: `MemoryError` during topic modeling

**Solution**:
- Reduce dataset size
- Use sampling:
  ```python
  df_sample = df.sample(n=3000, random_state=42)
  ```
- Close other applications
- Increase virtual memory (Windows)

#### 8. **YouTube API Quota Exceeded**

**Error**: `quotaExceeded`

**Solution**:
- Wait 24 hours for quota reset
- Use existing CSV files instead
- Apply for quota increase (Google Cloud Console)

---

## ⚙️ Advanced Configuration

### Customizing Dashboard

#### 1. **Change Port**

```bash
streamlit run dashboard.py --server.port 8080
```

#### 2. **Change Theme**

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

#### 3. **Adjust Caching**

In `dashboard.py`, modify:
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    # ...
```

### Customizing Pipeline

#### 1. **Change Sentiment Thresholds**

```python
# In notebook, modify:
def classify_sentiment(score):
    if score >= 0.1:  # More strict positive threshold
        return 'positive'
    elif score <= -0.1:  # More strict negative threshold
        return 'negative'
    else:
        return 'neutral'
```

#### 2. **Adjust Topic Count**

```python
from bertopic import BERTopic

topic_model = BERTopic(
    nr_topics=15,  # Specify exact number of topics
    min_topic_size=50  # Minimum comments per topic
)
```

#### 3. **Change NER Model**

```python
# Use larger SpaCy model for better accuracy
import spacy
nlp = spacy.load("en_core_web_lg")  # Large model
# or
nlp = spacy.load("en_core_web_trf")  # Transformer-based
```

### Performance Optimization

#### 1. **Enable Caching**

```python
import streamlit as st

@st.cache_data
def expensive_computation():
    # Heavy processing
    return result
```

#### 2. **Parallelize Processing**

```python
from multiprocessing import Pool

def process_batch(batch):
    # Process batch
    return results

with Pool(4) as p:
    results = p.map(process_batch, batches)
```

#### 3. **Use Faster Models**

```python
# Use smaller embedding model
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast & small
```

---

## 📝 Example Workflows

### Workflow 1: Analyze New YouTube Videos

```bash
# 1. Update video IDs in notebook
video_ids = ['VIDEO_ID_1', 'VIDEO_ID_2', 'VIDEO_ID_3']

# 2. Run scraping cells
# 3. Run preprocessing cells
# 4. Run analysis cells (sentiment, NER, topics)
# 5. Save new CSV
# 6. Refresh dashboard
```

### Workflow 2: Export Insights for Presentation

```bash
# 1. Open dashboard
# 2. Apply filters for specific insights
# 3. Take screenshots (Windows: Win + Shift + S)
# 4. Export data table (click ⋮ → Download as CSV)
# 5. Use in PowerPoint/Google Slides
```

### Workflow 3: Compare Different Time Periods

```python
# In dashboard.py, add date filter:
date_range = st.sidebar.date_input("Date Range", [start_date, end_date])
df_filtered = df[
    (df['updated_at'] >= date_range[0]) & 
    (df['updated_at'] <= date_range[1])
]
```

---

## 🎓 Learning Resources

### NLP Concepts
- [VADER Sentiment Analysis](https://github.com/cjhutto/vaderSentiment)
- [SpaCy NER Guide](https://spacy.io/usage/linguistic-features#named-entities)
- [BERTopic Tutorial](https://maartengr.github.io/BERTopic/)

### Streamlit Tips
- [Streamlit Docs](https://docs.streamlit.io/)
- [Plotly Charts](https://plotly.com/python/)
- [Caching Guide](https://docs.streamlit.io/library/advanced-features/caching)

### Python Libraries
- [Pandas Tutorial](https://pandas.pydata.org/docs/user_guide/index.html)
- [NLTK Book](https://www.nltk.org/book/)
- [Scikit-learn](https://scikit-learn.org/stable/tutorial/index.html)

---

## 🆘 Getting Help

### In-Code Help

```python
# Check dashboard function
help(st.plotly_chart)

# Check library version
import streamlit as st
print(st.__version__)
```

### Community Support

- **Streamlit Forum**: https://discuss.streamlit.io/
- **Stack Overflow**: Tag with `streamlit`, `nlp`, `spacy`
- **GitHub Issues**: Create issue with error details

### Contact

For project-specific questions:
- **Email**: [your.email@example.com]
- **Project Issues**: [GitHub Issues Link]

---

<div align="center">

**Happy Analyzing! ⚽📊**

[⬅️ Back to README](README.md)

</div>
