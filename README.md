# Django Wordle Web App

This is a web-based implementation of the classic Wordle game, built with Django.

## Features
- Classic Wordle rules: 5-letter words, 6 guesses
- Built-in word list
- Interactive game board with color feedback (green/yellow/gray)
- Game state persists per user session

## Setup Instructions

1. **Clone the repository** (if not already):
   ```sh
   git clone <repo-url>
   cd Wordle
   ```

2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```sh
   python manage.py migrate
   ```

4. **Start the development server**:
   ```sh
   python manage.py runserver
   ```

5. **Open your browser** and go to `http://127.0.0.1:8000/` to play Wordle!

## Project Structure
- `wordle_project/` - Django project settings
- `game/` - Main app containing game logic and views
- `manage.py` - Django management script

---

Enjoy playing Wordle! 