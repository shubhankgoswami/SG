import feedparser
import google.generativeai as genai
import json
import os
import datetime
import ssl

# Fix for SSL certificate verify failed on Mac
if not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
    ssl._create_default_https_context = ssl._create_unverified_context

# Configuration
RSS_FEEDS = {
    "TechCrunch": "https://techcrunch.com/feed/",
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "Wired": "https://www.wired.com/feed/rss",
    "VentureBeat": "https://venturebeat.com/feed/",
    "NYT Tech": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "WSJ Tech": "https://feeds.a.dj.com/rss/RSSWSJD.xml",
    "MIT Tech Review": "https://www.technologyreview.com/feed/",
}

def fetch_news():
    all_entries = []
    print("Fetching news from RSS feeds...")
    for source, url in RSS_FEEDS.items():
        try:
            print(f"Parsing {source}: {url}...")
            feed = feedparser.parse(url)
            if not feed.entries:
                print(f"Warning: No entries found for {source}. Bozo: {feed.get('bozo', 0)}")
                if 'bozo_exception' in feed:
                    print(f"Bozo exception: {feed.bozo_exception}")
            for entry in feed.entries[:10]: # Get top 10 from each source
                all_entries.append({
                    "source": source,
                    "title": entry.title,
                    "link": entry.link,
                    "summary": entry.get("summary", entry.get("description", "")),
                    "published": entry.get("published", "")
                })
            print(f"Successfully fetched {len(feed.entries)} entries from {source}")
        except Exception as e:
            print(f"Error fetching from {source}: {e}")
    return all_entries

def curate_news(entries):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        return []

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    # Prepare input for Gemini
    news_input = "\n".join([f"Source: {e['source']}\nTitle: {e['title']}\nSummary: {e['summary'][:200]}\nLink: {e['link']}\n---" for e in entries])

    prompt = f"""
    You are a high-end news curator for a tech-savvy executive. 
    Analyze the following news items and select the top 20-25 most critical and interesting updates for today ({datetime.date.today()}).
    Prioritize AI, breakthroughs in Tech, and major global shifts.
    
    For each selected item, provide:
    1. A catchy broad category (e.g., "AI BREAKTHROUGH", "BIG TECH", "GLOBAL ECONOMY").
    2. A short, punchy title.
    3. A cohesive summary of 60-100 words that provides deep context and insight.
    4. The original source link.

    Return the output ONLY as a JSON array of objects with the following keys:
    "category", "title", "summary", "link"

    News Items:
    {news_input}
    """

    print("Curating top stories with Gemini...")
    try:
        response = model.generate_content(prompt)
        # Extract JSON from response (handling potential markdown formatting)
        content = response.text.strip()
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
        
        curated_news = json.loads(content)
        return curated_news
    except Exception as e:
        print(f"Error curating news: {e}")
        return []

def main():
    entries = fetch_news()
    if not entries:
        print("No news entries fetched.")
        return

    curated = curate_news(entries)
    if curated:
        # Save as .js file to bypass CORS issues on local/mobile previews
        with open("news_data.js", "w") as f:
            f.write(f"window.NEWS_DATA = {json.dumps(curated, indent=4)};")
        print(f"Successfully generated news_data.js with {len(curated)} items.")
    else:
        print("Failed to curate news.")

if __name__ == "__main__":
    main()
