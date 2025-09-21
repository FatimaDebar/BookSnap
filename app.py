import streamlit as st
import json
from PIL import Image
import os

from src.metadata_api import fetch_book_metadata
from src.recommender import SentenceTransformer, cosine_similarity

# Paths
ocr_path = os.path.join("Book", "data", "ocr_results", "ocr_output.json")
recommendation_path = os.path.join("Book", "data", "ocr_results", "recommendations.json")
library_path = os.path.join("Book", "data", "library.json")
image_folder = os.path.join("Book", "data", "raw_images")

# Load OCR and recommendation data
if not os.path.exists(ocr_path) or not os.path.exists(recommendation_path):
    st.error("OCR or recommendation data file not found.")
    st.stop()

with open(ocr_path, 'r') as f:
    ocr_data = json.load(f)

with open(recommendation_path, 'r') as f:
    recommendations = json.load(f)

# Load or initialize library
try:
    with open(library_path, 'r') as f:
        library = json.load(f)
except (json.JSONDecodeError, FileNotFoundError):
    library = []

# Sidebar navigation
page = st.sidebar.radio("📂 Navigate", ["Home", "My Library"])

# Sidebar search
st.sidebar.header("🔍 Search or Filter")
search_query = st.sidebar.text_input("Search by title or author")

# Sidebar library preview
st.sidebar.markdown("## 📚 My Library")
if library:
    for book in library:
        st.sidebar.write(f"**{book['title']}** by {book['author']}")
else:
    st.sidebar.info("Your library is empty.")

# 📍 Page: Home
if page == "Home":
    st.title("📚 BookSnap: Discover Books from Covers")

    uploaded_file = st.file_uploader("Upload a book cover", type=["jpg", "png"])
    if uploaded_file:
        st.image(Image.open(uploaded_file), caption="Uploaded Cover", use_column_width=True)
        filename = uploaded_file.name

        if filename in ocr_data:
            st.subheader("🧠 Extracted Text")
            st.write(" ".join(ocr_data[filename]))

            title = " ".join(ocr_data[filename][:3])
            author = " ".join(ocr_data[filename][3:5])
            st.subheader("📖 Title & Author")
            st.write(f"**Title:** {title}")
            st.write(f"**Author:** {author}")

            metadata = fetch_book_metadata(title, author)
            with st.expander("📘 Full Book Metadata"):
                st.json(metadata)

            # Save to library with rating and tags
            def save_to_library(title, author, filename):
                rating = st.slider("⭐ Rate this book", 1, 5, 3)
                tags_input = st.text_input("🏷️ Add tags (comma-separated)", "")
                tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

                book_entry = {
                    "title": title,
                    "author": author,
                    "filename": filename,
                    "rating": rating,
                    "tags": tags
                }

                if book_entry not in library:
                    library.append(book_entry)
                    with open(library_path, 'w') as f:
                        json.dump(library, f, indent=2)
                    st.success("📥 Book saved to your library!")
                else:
                    st.info("✅ This book is already in your library.")

            if st.button("📥 Save this book to my library"):
                save_to_library(title, author, filename)

            # Show recommendations
            if filename in recommendations:
                st.subheader("🔁 Recommended Books")
                recs = recommendations[filename]
                cols = st.columns(len(recs)) if len(recs) > 1 else [st]

                for i, rec in enumerate(recs):
                    image_path = os.path.join(image_folder, rec)
                    if os.path.exists(image_path):
                        with cols[i]:
                            st.image(Image.open(image_path), caption=rec, use_column_width=True)
                            if st.button(f"View details: {rec}", key=f"btn_{rec}"):
                                st.info(f"Details for {rec} coming soon...")
                    else:
                        st.warning(f"Image not found: {rec}")
        else:
            st.error("No OCR data found for this image.")

# 📍 Page: My Library
elif page == "My Library":
    st.title("📚 My Library")

    if library:
        st.subheader("🔎 Filter Your Library")

        search_term = st.text_input("Search by title or author")
        all_tags = sorted({tag for book in library for tag in book.get("tags", [])})
        selected_tag = st.selectbox("Filter by tag", ["All"] + all_tags)
        min_rating = st.slider("Minimum rating", 1, 5, 1)

        filtered_library = [
            book for book in library
            if (search_term.lower() in book["title"].lower() or search_term.lower() in book["author"].lower())
            and (selected_tag == "All" or selected_tag in book.get("tags", []))
            and book.get("rating", 0) >= min_rating
        ]

        for book in filtered_library:
            col1, col2 = st.columns([1, 3])
            image_path = os.path.join(image_folder, book["filename"])
            with col1:
                if os.path.exists(image_path):
                    st.image(Image.open(image_path), use_column_width=True)
                else:
                    st.warning("Image not found.")
            with col2:
                st.markdown(f"**{book['title']}**")
                st.markdown(f"*by {book['author']}*")
                st.markdown(f"**Rating:** {'⭐' * book.get('rating', 0)}")
                if book.get("tags"):
                    st.markdown(f"**Tags:** {', '.join(book['tags'])}")

                if st.button(f"🗑️ Remove {book['title']}", key=f"del_{book['title']}"):
                    library.remove(book)
                    with open(library_path, 'w') as f:
                        json.dump(library, f, indent=2)
                    st.success(f"{book['title']} removed from your library.")
                    st.experimental_rerun()
    else:
        st.info("Your library is empty.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Fatima | BookSnap 2025")
