---

# 🕵️ Review Scraper + Sentiment Analysis with Claude + Streamlit Dashboard

This project scrapes product/service reviews from the web, uses **prompt engineering** with **Claude (Anthropic)** to analyze the sentiment and extract key topics, and then visualizes everything nicely in a **Streamlit** dashboard.

## 🔍 What It Does

* **Scrapes reviews** from a source (Amazon, Yelp, or a static dataset)
* Sends each review to **Claude** with a custom prompt for:

  * **Sentiment analysis** (positive, neutral, or negative)
  * **Keyword extraction** (main themes or issues)
* Stores the processed data
* Displays interactive charts and summaries using **Streamlit**

---

## 🧠 Why Prompt Engineering?

Using Claude (or any LLM) out of the box is okay, but you often get generic results. With good **prompt engineering**, you can guide the model to:

* Be more consistent with sentiment labeling
* Pull out relevant keywords without generic fluff
* Save money and time by reducing unnecessary token usage

## 📊 Streamlit Dashboard

The dashboard shows:

* Pie chart of sentiments
* Filterable review table
* Trend over time if date info is available

It’s super simple to run and doesn’t need much setup.

---

## 🚀 How to Run

1. Clone the repo
2. Run the app

   ```
   streamlit run app.py
   ```

---

## 🆚 Why Use Claude?

**Pros:**

* Great at language understanding
* Handles nuanced sentiment better than rule-based tools

**Cons:**

* Needs API access
* Slightly slower than local models

But if you care about quality over speed or cost, Claude + prompt engineering is a solid combo.

---

## 🧾 File Structure

```
.
├── scraper.ipynb           # Scrapes reviews
├── data.tsv                # Stores the scraped reviews
├── review_analysis.json    # Stored Sentiment Analysis of reviews  
├── app.py                  # Streamlit dashboard for analytics
├── project.ipynb           # Main file
└── README.md
```

---

## ⚠️ Notes

* Make sure you're complying with terms of service when scraping.
* API costs can add up — test with a small batch first.
* You can swap Claude for another LLM if you want — just tweak the prompt format.
