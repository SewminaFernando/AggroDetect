# AggroDetect

## Overview

AggroDetect is a cutting-edge system designed to transform the call center experience. By using advanced data science techniques, it can analyze both voice and text conversations. This allows it to accurately distinguish between aggressive and non-aggressive customers. With this information, the system can tailor the call center experience to each customer, ensuring exceptional service. Call center agents will be equipped with valuable insights, enabling them to better handle aggressive customers and ultimately enhance overall customer satisfaction.

## Features
- Audio Feature Extraction
- Aggressiveness Classification by Audio
- Voice to Text Transcription
- Aggressiveness Classification by Text
- Department Classification by Text
- Automated Response System
- Entity Extraction (Phone number & Name)
- View past conversation
- Record Customer Complaints
- Display Analytics charts
- Agent Routing

## Demo Video
https://github.com/SewminaFernando/AggroDetect_DSGP/assets/125371767/7df03968-4a3c-4195-a102-d89d8368277e

# How to use

> **Note:**
> This steps are only for Windows users.

### 1. Clone this Repository

To clone this repository, follow these steps:

1. Navigate to the directory where you want to clone the repository.
2. Open the command prompt or terminal from that directory.
3. Copy and paste the following code into the command prompt or terminal:

```bash
git clone https://github.com/SewminaFernando/AggroDetect_DSGP.git
```

### 2. Create Virtual Environment

```bash
pip install virtualenv
```
```bash
virtualenv .venv
```
### 3. Activate Virtual Environment

```bash
.venv\Scripts\activate
```

### 4. Install the required dependencies

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

### 5. Activate rasa action server and run rasa

You should run these commands in two separate command prompts after activating the virtual environment.

> **Note:**
> If your command prompt is not activated with the virtual environment, repeat step 3.

1. Activate rasa action server
```bash
rasa run actions
```

2. Run rasa
```bash
rasa shell
```

### 6. Run the Flask application

Make sure you are in the project folder.

Then navigate to interface folder

```bash
cd interface
```
Then run the `app.py` file in python

```bash
python app.py
```

To access the website, you can either click on the URL provided or navigate to localhost:5000 in your web browser.

<hr>

### Note :

To transcribe audio files using OpenAI API keys, follow these steps:

1. Create a file named `.env`.

2. Paste your OpenAI API key and organization ID into the .env file in the following format:

```bash
OPENAI_API_KEY = <Your-API-Key>
WHISPER_ORG = <Your-Organization-ID>
```
Replace `<Your-API-Key>` with your actual OpenAI API key and `<Your-Organization-ID>` with your organization ID. This information will enable the application to access OpenAI's transcription services securely.

<hr>

# Thank you !!!

