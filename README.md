# 🧠 Spaced Memory Review System

## 📚 Overview
This project is an intelligent spaced repetition learning system that helps you effectively review and retain information. It implements scientifically-proven memory retention techniques by scheduling reviews at optimal intervals.

## ✨ Features
- 📝 Easy submission of learning materials (text and images)
- 🎯 Smart scheduling of review intervals
- 🌐 Browser-based review interface
- 📊 Organized by subjects and topics
- 🖼️ Support for screenshots and images
- 🔗 Optional link attachments

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.11 or higher
- Jupyter Notebook environment
- Screenshots folder access

### Installation Steps
1. Clone this repository
2. Navigate to the project directory
3. Install required dependencies:
   ```bash
   cd Src
   pip install -r requirements.txt
   ```

## 🚀 Getting Started

1. **Initial Setup**
   - Open `Review_dashboard.ipynb`
   - Run the first cell to initialize the program (one-time setup)

2. **Adding New Material**
   - Run the "Submitting Learned Material" cell
   - Follow the prompts to enter:
     - Subject and topic
     - Text content or screenshots
     - Optional links

3. **Daily Review**
   - Run the "Viewing Daily Review Material" cell
   - Your review content will open automatically in your default browser

## 📂 Project Structure
- `Src/` - Core source code and notebooks
- `Data/` - Storage for learning materials
- `Styles/` - CSS and styling assets

## ⚙️ Configuration
The system can be customized through `config.json`. A template is provided in `config_template.json`.

## 🔄 Reset Instructions
If needed, you can reset the program:
1. Open `Review_dashboard.ipynb`
2. Run the "Reset the Program" cell
3. Confirm when prompted

## ⚠️ Important Notes
- The reset function only clears the review schedule, not your stored materials
- Screenshots must be taken using your system's screenshot tool
- Regular reviews are recommended for optimal learning

## 🤝 Contributing
Feel free to submit issues and enhancement requests!

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
