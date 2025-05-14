# 📄 PDF Text Extractor API using FastAPI and PyMuPDF

This project is a FastAPI-based backend service that allows users to upload PDF files and extract all the visible text from them using **PyMuPDF (fitz)**. The API reads PDF content in memory and returns clean, extracted text as JSON.

---

## 🚀 Features

- Upload PDF via API
- Extract text from all pages
- Works with in-memory file streams (no file saving)
- Uses `PyMuPDF` for fast and reliable text extraction
- Returns filename and extracted text in JSON format

---

## 🛠 Tech Stack

- **FastAPI** – High-performance Python web framework
- **PyMuPDF (fitz)** – Lightweight library for PDF parsing
- **Uvicorn** – ASGI server to run FastAPI apps

---

## 📁 Project Structure

