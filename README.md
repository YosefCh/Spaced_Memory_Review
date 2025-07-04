# 🧠 Spaced Memory Review System

## 📚 Overview
This project is an intelligent spaced repetition learning system that helps you effectively review and retain information. It implements scientifically-proven memory retention techniques by scheduling reviews at optimal intervals, enhanced with **AI-powered content generation** for automated learning material creation.

## ✨ Features
- 📝 **Manual Mode**: Easy submission of learning materials (text and screenshots)
- 🤖 **AI Mode**: Automated content generation with three intelligent options
- 🎯 Smart scheduling of review intervals using spaced repetition algorithms
- 🌐 Browser-based review interface with automatic file opening
- 📊 Organized by subjects and topics with metadata tracking
- 📸 Support for system screenshots with base64 encoding
- 🔗 Optional link attachments for additional resources
- 🧠 **AI-Enhanced Learning**: Intelligent topic recommendations based on learning history
- 📈 **Learning Analytics**: Topic frequency analysis and personalized suggestions

## 🤖 AI Features

### Three AI Content Generation Modes:

1. **🎯 User Choice Mode**
   - Enter any subject you want to learn about
   - AI generates educational content tailored to your level
   - Coherence checking to ensure meaningful topics
   - Avoids duplicate content from your learning history

2. **📊 Smart Recommendations Mode**
   - AI analyzes your past learning patterns
   - Weighted algorithm considers overall history, recent third, and past week
   - Suggests new topics based on your interests and gaps
   - Prevents repetition of already learned subjects

3. **🗄️ Database Mode** *(Coming Soon)*
   - Curated database of educational topics
   - Structured learning paths
   - Quality-assured content selection

### AI Content Features:
- **Undergraduate-level content** (4-5 minute read time)
- **Beginner-friendly explanations** with clear concepts
- **Markdown/HTML formatting** support
- **Automatic filename generation** using AI
- **Topic extraction** from generated content

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.x
- Jupyter Notebook environment
- System screenshot capability
- **OpenAI API Key** (for AI features)
- Internet connection (for AI content generation)

### Installation Steps

1. Clone this repository
2. Navigate to the project directory
3. Install required dependencies:

   ```bash
   cd Src
   pip install -r requirements.txt
   ```

4. **Configure AI Settings**:
   - Copy `config_template.json` to `config.json`
   - Add your OpenAI API key to the configuration
   - Customize paths and browser settings as needed

## 🚀 Getting Started

1. **Initial Setup**
   - Open `Review_dashboard.ipynb`
   - Run the first cell to initialize the program (one-time setup)

2. **Adding New Material - Choose Your Mode**

   ### 📝 Manual Mode
   - Run the "Manual Mode: Submit Your Own Learning Material" cell
   - Follow the prompts to enter:
     - Subject and topic
     - Text content or screenshots
     - Optional links

   ### 🤖 AI Mode (Recommended)
   - Run the "AI Mode: Generate and Submit Learning Material" cell
   - Choose from three AI options:
     1. **User Choice**: Enter any subject you want to learn
     2. **Smart Recommendations**: Get AI suggestions based on your learning history
     3. **Database Topics**: *(Coming soon)*
   - AI automatically generates educational content and saves it to your schedule

3. **Daily Review**
   - Run the "Viewing Daily Review Material" cell
   - Your review content will open automatically in your default browser
   - Review materials from today plus spaced intervals (1, 7, 30, 90 days, etc.)

## 🔧 Advanced Features

### AI Content Generation
- **Intelligent Topic Selection**: Avoids repeating previously learned subjects
- **Personalized Recommendations**: Analyzes your learning patterns using weighted algorithms
- **Quality Assurance**: Coherence checking ensures meaningful educational content
- **Automatic Processing**: No manual input required - AI handles everything

### Learning Analytics
- **Topic Frequency Analysis**: Tracks what subjects you study most
- **Learning History Integration**: Builds upon your existing knowledge base
- **Spaced Repetition Optimization**: Reviews scheduled at scientifically optimal intervals

## 📂 Project Structure

- `Src/` - Core source code and notebooks
  - `Spaced_Memory_Review.py` - Main class with AI integration
  - `AI_class.py` - OpenAI client implementations
  - `Review_dashboard.ipynb` - User interface with AI and manual modes
  - `notes.ipynb` - Development and testing notebook
  - `initiate_program.py` - Program initialization
  - `requirements.txt` - Python dependencies
- `Data/` - Storage for learning materials and metadata
  - `learned_material.csv` - Learning history database
  - `Review_Files/` - Generated HTML review files
  - `Single_Day_Files/` - Individual learning material files
- `Styles/` - CSS and styling assets

## 🔧 Technical Implementation

### AI Architecture
- **OpenAI Integration**: Uses GPT-4 models for content generation
- **Reasoning Model**: Advanced model for complex content creation
- **Nano Model**: Fast model for coherence checking and topic extraction
- **Smart Prompting**: Engineered prompts for educational content optimization

### Learning Algorithm
- **Spaced Repetition Intervals**: 1, 7, 30, 90, 365+ days
- **Weighted Recommendation System**: 
  - Overall history: 20%
  - Recent third: 30%
  - Past week: 50%
- **Duplicate Prevention**: Automatic checking against learning history

### Data Management
- **CSV-based storage** for learning metadata
- **HTML generation** for review materials
- **Base64 image encoding** for portability
- **Automatic file management** and naming

## ⚙️ Configuration

The system can be customized through `config.json`. A template is provided in `config_template.json`.

**Key Configuration Options**:
- OpenAI API settings
- File storage paths
- Browser preferences
- Screenshot directories

## 🔄 Reset Instructions
If needed, you can reset the program:
1. Open `Review_dashboard.ipynb`
2. Run the "Reset the Program" cell
3. Confirm when prompted

## ⚠️ Important Notes

- The reset function only clears the review schedule, not your stored materials
- Screenshots must be taken using your system's screenshot tool
- **AI features require OpenAI API key** - configure in `config.json`
- **AI-generated content** is automatically optimized for 4-5 minute reading time
- **Learning history analysis** improves AI recommendations over time
- Regular reviews are recommended for optimal spaced repetition benefits
- AI mode generates content without requiring manual input or screenshots

## 🎯 AI Usage Tips

- **Start with User Choice Mode** to learn specific topics you're interested in
- **Use Recommendations Mode** after building some learning history (10+ entries)
- **Combine AI and Manual modes** for a diverse learning experience


## 🤝 Contributing
Feel free to submit issues and enhancement requests!

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
