# Chat with your PDF

This Streamlit application allows you to upload a PDF document, and then ask questions to retrieve relevant information from the document.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- [Streamlit](https://streamlit.io/)
- Required Python libraries listed in `requirements.txt`

### Installation

1. Clone this repository to your local machine.
```bash
git clone https://github.com/franpandol/streamlit_openai_ask_pdf.git
```
2. Navigate to the project directory.
```bash
cd your-repo
```
3. Install the required Python libraries.
```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root directory to store your OpenAI API key. The contents of the file should be as follows:

```plaintext
OPENAI_API_KEY=your-api-key-here
```

Replace `your-api-key-here` with your actual OpenAI API key.

## Usage

To run the application, use the following command in the project root directory:

```bash
streamlit run app.py
```

This will launch the Streamlit server and open the application in your web browser. You can then upload a PDF document using the file uploader, and ask questions related to the document content in the provided text input field.

## Features

- Upload a PDF document to process its content.
- Ask questions to retrieve relevant information from the document.
- Lazy loading of resources for better performance.
- Error handling to ensure a smooth user experience.

## Troubleshooting

If you encounter any issues while running the application, check the console for error messages. Ensure that your OpenAI API key is correct and that you have internet connectivity.

## Contributing

Feel free to fork this repository, make changes, and open a pull request if you think your changes are worth sharing.

## License

[MIT License](LICENSE)
