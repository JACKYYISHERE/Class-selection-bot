# AI Class Selection Assistant

An intelligent course recommendation system that helps students select classes based on their preferences using natural language processing.

## Features

- Natural language input for class preferences
- AI-powered course recommendations
- Consideration of multiple factors:
  - Time preferences
  - Subject preferences
  - Commute time
  - Class schedule conflicts
  - Credit requirements
- Interactive web interface using Streamlit

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/class_selector_agent.git
cd class_selector_agent
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Enter your preferences in natural language, for example:
   - "I want morning classes on Monday and Wednesday"
   - "I prefer computer science and math classes"
   - "I need classes with at least 30 minutes between them"
   - "I can commute up to 20 minutes"

4. Click "Get Recommendations" to see your personalized course suggestions

## Project Structure

- `app.py` - Main Streamlit application
- `models.py` - Course data model
- `recommender.py` - Course recommendation engine
- `chat_interface.py` - ChatGPT integration
- `requirements.txt` - Python dependencies

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 