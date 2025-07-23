
# 📚 StoryBook Generator

Turn user prompts into illustrated storybooks — complete with structured scenes, voiceovers, and AI-generated images.

---

## 🚀 Getting Started

### 1. Clone the Repository

Open your terminal (Git Bash is recommended) and run:

```bash
git clone https://github.com/FakeandrewA/StoryBookGenerator.git
cd StoryBookGenerator
```

---

### 2. Set Up Your Feature Branch

Always start from the latest `main` branch:

```bash
git checkout main
git pull origin main
```

Create a new feature branch:

```bash
git checkout -b feature/your-feature-name
```

>  **Convention:** Use `feature/your-feature-name` format for branch names.

After making your changes:

```bash
git add --all
git commit -m "Describe your changes"
git push origin feature/your-feature-name
```

You’ll now see your feature branch in the repository.

---

### 3. Opening a Pull Request

* Open a PR targeting the `test-main` branch.
* After integration testing, a maintainer will merge into `main` to version the project safely.

---

## 🔐 Environment Setup

### 1. Get API Keys

* 🧠 Create a Together API key from [api.together.xyz](https://api.together.xyz)
* 🔑 Create a Groq API key from [groq.com](https://groq.com)

Paste both keys into `.env.example` like so:

```env
TOGETHER_API_KEY=your_together_api_key
GROQ_API_KEY=your_groq_api_key
```

Then rename the file:

```bash
mv .env.example .env
```

---

### 2. Create and Activate Virtual Environment

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

✅ Your environment is now ready.

---

## 🧠 Using the `bookGenerator`

```python
from storybookagent.graph import bookGenerator

book = bookGenerator.invoke({
    "userPrompt": "<your prompt here>",
    "userId": request.user.id
})
```

---

## 📦 Output Structure

The `book` returned is a dictionary with the following structure:

```python
book = {
    "userPrompt": str,                 # The original user input
    "grade": str,                      # Prompt grade: "yes" or "no"
    "userId": int,                     # The user ID
    "story": Story(
        title: str,
        titleImagePrompt: str,
        characterDescription: str,
        story: str,
        style: str,
        numOfScenes: int
    ),
    "scenes": Scenes(
        scenes: List[str],             # Detailed prompts for each scene
        voiceovers: List[str]          # Matching narration for each scene
    )
}
```

---

### 📄 For More Info

Explore schema definitions in [`storybookagent/schemas.py`](storybookagent/schemas.py) for complete details on the `Story` and `Scenes` objects.
