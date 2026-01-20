# pdf-rag-chatbot

Activate the Python virtual environment
```
python -m venv venv
source venv/bin/activate
```

Install Python packages
```
pip install -r requirements.txt
```

Download [Ollama](https://ollama.com/download) & run ollama.dmg

Download llama3 open-source large language model
```
ollama pull llama3
```

Run the Streamlit app
```
streamlit run app.py
```

Upload [pdf-sample.pdf](data/uploads/pdf-sample.pdf)

Ask questions like "What is the full form of PDF?"

Delete LLM
```
ollama rm llama3
```

Clear pip cache
```
pip cache purge
```