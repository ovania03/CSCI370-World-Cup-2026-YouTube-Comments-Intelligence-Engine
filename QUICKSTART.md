# ⚡ Quick Start Guide

## 🎯 Get Running in 3 Minutes

### For Windows Users (Easiest)

```bash
# 1. Double-click this file:
setup.bat

# 2. Run the dashboard:
streamlit run dashboard.py
```

Done! Your browser will open automatically.

---

## 🐧 For Mac/Linux Users

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download models
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('vader_lexicon')"

# 3. Run dashboard
streamlit run dashboard.py
```

---

## 🎨 What You'll See

### Dashboard URL
```
http://localhost:8501
```

### Main Features
- 📊 **Sentiment Charts**: Pie chart + histogram
- 🔑 **Keywords**: Top 15 most mentioned terms
- 🏷️ **Entities**: Players, teams, locations
- 💬 **Top Comments**: Most-liked comments
- 🔍 **Search**: Type any question about the World Cup

---

## 🔍 Try These Search Queries

```
What do fans think about Messi?
Opinions on USA hosting
Canada team performance
Stadium complaints
Best goals
Ticket prices too high
```

---

## 📊 Filter Examples

### See Only Positive Comments
- Sidebar → Sentiment → Select only "positive"

### High Engagement Only
- Sidebar → Min Likes slider → Move to 10+

### Specific Topics
- Scroll to Topic Distribution chart
- Identify topic numbers
- Reference in data browser

---

## 🚨 Troubleshooting (1-Minute Fixes)

### "Can't find model 'en_core_web_sm'"
```bash
python -m spacy download en_core_web_sm
```

### "Module not found: streamlit"
```bash
pip install streamlit
```

### "Port 8501 already in use"
```bash
streamlit run dashboard.py --server.port 8502
```

### "File not found: worldcup_2026_with_topics.csv"
**Solution**: The CSV file must be in the same folder as dashboard.py

---

## 📂 File Structure Check

Make sure you have:
```
worldcup_analysis/
├── dashboard.py                          ✓ Required
├── worldcup_2026_with_topics.csv         ✓ Required
├── requirements.txt                      ✓ Required
├── README.md                             📖 Documentation
└── setup.bat                             🔧 Setup script
```

---

## 🎓 Next Steps

### Explore the Data
1. Click "Browse Raw Comments" at bottom
2. Sort by clicking column headers
3. Search using the search box

### Export Data
1. Open "Browse Raw Comments"
2. Click the ⋮ menu (top right)
3. Select "Download as CSV"

### Customize Filters
1. Use sentiment filter (sidebar)
2. Adjust minimum likes
3. Watch metrics update in real-time

---

## 📖 Full Documentation

- **Complete Guide**: [README.md](README.md)
- **Detailed Usage**: [USAGE.md](USAGE.md)
- **Notebook**: Open `CSCI370_project_pipeline_final_1 (3).ipynb`

---

## 💡 Pro Tips

### Tip 1: Speed Up Dashboard
Clear filters to show all data → faster initial load

### Tip 2: Find Insights Fast
Use the search feature instead of scrolling through tables

### Tip 3: Screenshot Charts
- Windows: `Win + Shift + S`
- Mac: `Cmd + Shift + 4`
Perfect for presentations!

### Tip 4: Theme Toggle
Streamlit has dark mode! Click ☰ menu → Settings → Theme

---

## 🆘 Still Stuck?

### Check Python Version
```bash
python --version
```
**Required**: Python 3.10 or higher

### Reinstall Everything
```bash
pip uninstall -y -r requirements.txt
pip install -r requirements.txt
```

### Contact Support
- Check [USAGE.md](USAGE.md) for detailed help
- See troubleshooting section in [README.md](README.md)

---

<div align="center">

**🚀 You're All Set!**

[View Full README](README.md) | [Detailed Usage Guide](USAGE.md)

</div>
