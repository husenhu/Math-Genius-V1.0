import sys
import json
import os
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QStackedWidget, QListWidget, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt, QTimer # Import QTimer

class MathQuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.scores_file = os.path.join('save', 'data.json')
        self.current_language = 'id'  # Default language is Indonesian
        self.translations = {
            'id': {
                'app_title': 'Math Genius v1.0',
                'welcome': 'Selamat Datang di Kuis Matematika!',
                'enter_name': 'Masukkan Nama Anda:',
                'start_quiz': 'Mulai Kuis',
                'history': 'Riwayat Skor',
                'language_select': 'Pilih Bahasa:',
                'question': 'Pertanyaan:',
                'your_answer': 'Jawaban Anda:',
                'submit': 'Kirim',
                'score': 'Skor Anda:',
                'time': 'Waktu:', # New translation for time
                'correct_answer': 'Jawaban Benar!',
                'wrong_answer': 'Jawaban Salah. Jawaban yang benar adalah:',
                'quiz_finished': 'Kuis Selesai!',
                'back_to_menu': 'Kembali ke Menu Utama',
                'name_placeholder': 'Nama Anda',
                'answer_placeholder': 'Masukkan jawaban',
                'no_history': 'Belum ada riwayat skor.',
                'question_type_add': 'Berapakah hasil dari {} + {}?',
                'question_type_sub': 'Berapakah hasil dari {} - {}?',
                'question_type_mul': 'Berapakah hasil dari {} x {}?',
                'question_type_div': 'Berapakah hasil dari {} : {}? (Bulatkan ke bawah jika ada sisa)',
                'total_questions': 'Total Pertanyaan:',
                'correct_questions': 'Jawaban Benar:',
                'final_score': 'Skor Akhir:',
                'time_taken': 'Waktu Pengerjaan:', # New translation for time taken on result page
                'rating': 'Rating:', # New translation for rating
                'rating_excellent': 'Sangat Baik',
                'rating_great': 'Bagus',
                'rating_good': 'Cukup Baik',
                'rating_needs_practice': 'Perlu Latihan Lagi',
                'not_available': 'N/A' # New translation for 'Not Available'
            },
            'en': {
                'app_title': 'Math Genius v1.0',
                'welcome': 'Welcome to the Math Quiz!',
                'enter_name': 'Enter Your Name:',
                'start_quiz': 'Start Quiz',
                'history': 'Score History',
                'language_select': 'Select Language:',
                'question': 'Question:',
                'your_answer': 'Your Answer:',
                'submit': 'Submit',
                'score': 'Your Score:',
                'time': 'Time:', # New translation for time
                'correct_answer': 'Correct Answer!',
                'wrong_answer': 'Wrong Answer. The correct answer was:',
                'quiz_finished': 'Quiz Finished!',
                'back_to_menu': 'Back to Main Menu',
                'name_placeholder': 'Your Name',
                'answer_placeholder': 'Enter answer',
                'no_history': 'No score history yet.',
                'question_type_add': 'What is {} + {}?',
                'question_type_sub': 'What is {} - {}?',
                'question_type_mul': 'What is {} x {}?',
                'question_type_div': 'What is {} : {}? (Round down if there\'s a remainder)',
                'total_questions': 'Total Questions:',
                'correct_questions': 'Correct Answers:',
                'final_score': 'Final Score:',
                'time_taken': 'Time Taken:', # New translation for time taken on result page
                'rating': 'Rating:', # New translation for rating
                'rating_excellent': 'Excellent',
                'rating_great': 'Great',
                'rating_good': 'Good',
                'rating_needs_practice': 'Needs More Practice',
                'not_available': 'N/A' # New translation for 'Not Available'
            }
        }
        self.quiz_timer = QTimer(self)
        self.quiz_timer.timeout.connect(self.update_timer)
        self.elapsed_time = 0 # Initialize elapsed time in seconds
        self.current_score = 0 # Initialize current_score here

        self.init_ui()
        self.load_scores()
        self.update_history_display()
        self.update_ui_language()

    def get_text(self, key):
        return self.translations[self.current_language].get(key, key)

    def init_ui(self):
        self.setWindowTitle(self.get_text('app_title'))
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QStackedWidget(self)
        # self.setCentralWidget(self.stacked_widget) # This line is not needed for QWidget, only QMainWindow

        # Main Menu Page
        self.main_menu_page = QWidget()
        self.main_menu_layout = QVBoxLayout()
        self.main_menu_page.setLayout(self.main_menu_layout)

        self.welcome_label = QLabel(self.get_text('welcome'))
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.main_menu_layout.addWidget(self.welcome_label)

        self.language_label = QLabel(self.get_text('language_select'))
        self.language_label.setAlignment(Qt.AlignCenter)
        self.main_menu_layout.addWidget(self.language_label)

        self.language_combo = QComboBox()
        self.language_combo.addItem("Bahasa Indonesia", "id")
        self.language_combo.addItem("English", "en")
        self.language_combo.currentIndexChanged.connect(self.change_language)
        self.main_menu_layout.addWidget(self.language_combo, alignment=Qt.AlignCenter)

        self.start_button = QPushButton(self.get_text('start_quiz'))
        self.start_button.clicked.connect(self.show_name_input)
        self.main_menu_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        self.history_label = QLabel(self.get_text('history'))
        self.history_label.setAlignment(Qt.AlignCenter)
        self.history_label.setStyleSheet("font-size: 18px; margin-top: 20px;")
        self.main_menu_layout.addWidget(self.history_label)

        self.history_list = QListWidget()
        self.history_list.setMinimumHeight(150)
        self.main_menu_layout.addWidget(self.history_list)

        self.stacked_widget.addWidget(self.main_menu_page)

        # Name Input Page
        self.name_input_page = QWidget()
        self.name_input_layout = QVBoxLayout()
        self.name_input_page.setLayout(self.name_input_layout)

        self.name_label = QLabel(self.get_text('enter_name'))
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet("font-size: 18px;")
        self.name_input_layout.addWidget(self.name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(self.get_text('name_placeholder'))
        self.name_input.setAlignment(Qt.AlignCenter)
        self.name_input_layout.addWidget(self.name_input, alignment=Qt.AlignCenter)

        self.start_quiz_button = QPushButton(self.get_text('start_quiz'))
        self.start_quiz_button.clicked.connect(self.start_quiz)
        self.name_input_layout.addWidget(self.start_quiz_button, alignment=Qt.AlignCenter)

        self.stacked_widget.addWidget(self.name_input_page)

        # Quiz Page
        self.quiz_page = QWidget()
        self.quiz_layout = QVBoxLayout()
        self.quiz_page.setLayout(self.quiz_layout)

        # Top bar for Score and Time
        top_bar_layout = QHBoxLayout()
        self.score_display = QLabel(self.get_text('score') + " 0")
        self.score_display.setAlignment(Qt.AlignLeft)
        top_bar_layout.addWidget(self.score_display)

        self.timer_display = QLabel(self.get_text('time') + " 00:00")
        self.timer_display.setAlignment(Qt.AlignRight)
        top_bar_layout.addWidget(self.timer_display)
        self.quiz_layout.addLayout(top_bar_layout)

        self.question_label = QLabel(self.get_text('question') + " ")
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setStyleSheet("font-size: 22px; font-weight: bold; margin-top: 20px;")
        self.quiz_layout.addWidget(self.question_label)

        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText(self.get_text('answer_placeholder'))
        self.answer_input.setAlignment(Qt.AlignCenter)
        self.answer_input.returnPressed.connect(self.check_answer) # Allow Enter key to submit
        self.quiz_layout.addWidget(self.answer_input, alignment=Qt.AlignCenter)

        self.submit_button = QPushButton(self.get_text('submit'))
        self.submit_button.clicked.connect(self.check_answer)
        self.quiz_layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)

        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet("font-size: 16px; margin-top: 10px;")
        self.quiz_layout.addWidget(self.feedback_label)

        self.stacked_widget.addWidget(self.quiz_page)

        # Result Page
        self.result_page = QWidget()
        self.result_layout = QVBoxLayout()
        self.result_page.setLayout(self.result_layout)

        self.result_message_label = QLabel(self.get_text('quiz_finished'))
        self.result_message_label.setAlignment(Qt.AlignCenter)
        self.result_message_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.result_layout.addWidget(self.result_message_label)

        self.final_score_label = QLabel("")
        self.final_score_label.setAlignment(Qt.AlignCenter)
        self.final_score_label.setStyleSheet("font-size: 20px; margin-top: 10px;")
        self.result_layout.addWidget(self.final_score_label)

        self.final_time_label = QLabel("") # New label for final time
        self.final_time_label.setAlignment(Qt.AlignCenter)
        self.final_time_label.setStyleSheet("font-size: 18px; margin-top: 5px;")
        self.result_layout.addWidget(self.final_time_label)

        self.final_rating_label = QLabel("") # New label for final rating
        self.final_rating_label.setAlignment(Qt.AlignCenter)
        self.final_rating_label.setStyleSheet("font-size: 18px; margin-top: 5px; font-weight: bold;")
        self.result_layout.addWidget(self.final_rating_label)

        self.back_to_menu_button = QPushButton(self.get_text('back_to_menu'))
        self.back_to_menu_button.clicked.connect(self.show_main_menu)
        self.result_layout.addWidget(self.back_to_menu_button, alignment=Qt.AlignCenter)

        self.stacked_widget.addWidget(self.result_page)

        # Set initial page
        self.stacked_widget.setCurrentWidget(self.main_menu_page)

        # Main layout for the QWidget
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.stacked_widget)
        self.setLayout(self.main_layout)

    def change_language(self, index):
        self.current_language = self.language_combo.itemData(index)
        self.update_ui_language()

    def update_ui_language(self):
        self.setWindowTitle(self.get_text('app_title'))
        self.welcome_label.setText(self.get_text('welcome'))
        self.language_label.setText(self.get_text('language_select'))
        self.start_button.setText(self.get_text('start_quiz'))
        self.history_label.setText(self.get_text('history'))
        self.name_label.setText(self.get_text('enter_name'))
        self.name_input.setPlaceholderText(self.get_text('name_placeholder'))
        self.start_quiz_button.setText(self.get_text('start_quiz'))
        # Ensure current_score is initialized before using it here
        if hasattr(self, 'current_score'):
            self.score_display.setText(self.get_text('score') + " " + str(self.current_score))
        else:
            self.score_display.setText(self.get_text('score') + " 0")
        self.timer_display.setText(self.get_text('time') + " 00:00") # Reset timer display on language change
        self.question_label.setText(self.get_text('question') + " ") # Reset question label for new language
        self.answer_input.setPlaceholderText(self.get_text('answer_placeholder'))
        self.submit_button.setText(self.get_text('submit'))
        self.result_message_label.setText(self.get_text('quiz_finished'))
        self.back_to_menu_button.setText(self.get_text('back_to_menu'))
        self.update_history_display() # Update history display for new language

    def show_name_input(self):
        self.stacked_widget.setCurrentWidget(self.name_input_page)
        self.name_input.clear() # Clear name input when showing page

    def start_quiz(self):
        self.player_name = self.name_input.text().strip()
        if not self.player_name:
            QMessageBox.warning(self, "Input Error", "Mohon masukkan nama Anda untuk memulai kuis.")
            return

        self.current_score = 0
        self.current_question_index = 0
        self.correct_answers_count = 0
        self.elapsed_time = 0 # Reset elapsed time for new quiz
        self.update_timer_display() # Update timer display immediately
        self.quiz_timer.start(1000) # Start the timer (fires every 1000 ms = 1 second)

        self.generate_questions()
        self.update_score_display()
        self.display_next_question()
        self.stacked_widget.setCurrentWidget(self.quiz_page)
        self.feedback_label.clear() # Clear feedback from previous quiz

    def update_timer(self):
        self.elapsed_time += 1
        self.update_timer_display()

    def update_timer_display(self):
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.timer_display.setText(self.get_text('time') + f" {time_str}")


    def generate_questions(self):
        self.questions = []
        num_questions = 10 # Number of questions for the quiz

        for _ in range(num_questions):
            op_type = random.choice(['add', 'sub', 'mul', 'div']) # Include multiplication and division
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)

            question_text = ""
            correct_answer = 0

            if op_type == 'add':
                question_text = self.get_text('question_type_add').format(num1, num2)
                correct_answer = num1 + num2
            elif op_type == 'sub':
                # Ensure num1 is greater than or equal to num2 for subtraction
                if num1 < num2:
                    num1, num2 = num2, num1
                question_text = self.get_text('question_type_sub').format(num1, num2)
                correct_answer = num1 - num2
            elif op_type == 'mul':
                # Keep numbers small for 1st grade multiplication
                num1 = random.randint(1, 5)
                num2 = random.randint(1, 5)
                question_text = self.get_text('question_type_mul').format(num1, num2)
                correct_answer = num1 * num2
            elif op_type == 'div':
                # Ensure num1 is a multiple of num2 for division, and num2 is not zero
                num2 = random.randint(1, 5) # Divisor
                correct_answer = random.randint(1, 5) # Result
                num1 = num2 * correct_answer
                question_text = self.get_text('question_type_div').format(num1, num2)

            self.questions.append({'question': question_text, 'answer': correct_answer})
        random.shuffle(self.questions) # Shuffle the generated questions

    def display_next_question(self):
        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]
            self.question_label.setText(self.get_text('question') + " " + question_data['question'])
            self.answer_input.clear()
            self.feedback_label.clear()
            self.answer_input.setFocus() # Set focus to answer input
        else:
            self.end_quiz()

    def check_answer(self):
        if self.current_question_index >= len(self.questions):
            return # Prevent checking answer if quiz is already finished

        user_answer_text = self.answer_input.text().strip()
        if not user_answer_text:
            self.feedback_label.setText("Mohon masukkan jawaban Anda.")
            return

        try:
            user_answer = int(user_answer_text)
            correct_answer = self.questions[self.current_question_index]['answer']

            if user_answer == correct_answer:
                self.current_score += 10 # Award 10 points for correct answer
                self.correct_answers_count += 1
                self.feedback_label.setText(self.get_text('correct_answer'))
                self.feedback_label.setStyleSheet("color: green; font-weight: bold;")
            else:
                self.feedback_label.setText(
                    self.get_text('wrong_answer') + f" {correct_answer}"
                )
                self.feedback_label.setStyleSheet("color: red; font-weight: bold;")

            self.update_score_display()
            self.current_question_index += 1
            # Use QTimer.singleShot to delay showing the next question slightly
            # This allows the user to see the feedback before the question changes
            QTimer.singleShot(1000, self.display_next_question) # 1 second delay
        except ValueError:
            self.feedback_label.setText("Jawaban tidak valid. Mohon masukkan angka.")
            self.feedback_label.setStyleSheet("color: orange; font-weight: bold;")

    def update_score_display(self):
        self.score_display.setText(self.get_text('score') + f" {self.current_score}")

    def calculate_rating(self, correct_count, total_questions):
        if total_questions == 0:
            return self.get_text('rating_needs_practice') # Avoid division by zero

        percentage = (correct_count / total_questions) * 100
        if percentage >= 90:
            return self.get_text('rating_excellent')
        elif percentage >= 70:
            return self.get_text('rating_great')
        elif percentage >= 50:
            return self.get_text('rating_good')
        else:
            return self.get_text('rating_needs_practice')

    def end_quiz(self):
        self.quiz_timer.stop() # Stop the timer when quiz ends

        total_questions = len(self.questions)
        calculated_rating = self.calculate_rating(self.correct_answers_count, total_questions)
        self.save_score(self.player_name, self.current_score, self.elapsed_time, calculated_rating)
        self.update_history_display()

        final_message = (
            f"{self.get_text('total_questions')} {total_questions}\n"
            f"{self.get_text('correct_questions')} {self.correct_answers_count}\n"
            f"{self.get_text('final_score')} {self.current_score}"
        )
        self.final_score_label.setText(final_message)

        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.final_time_label.setText(self.get_text('time_taken') + f" {time_str}")
        self.final_rating_label.setText(self.get_text('rating') + f" {calculated_rating}")

        self.stacked_widget.setCurrentWidget(self.result_page)

    def load_scores(self):
        if not os.path.exists('save'):
            os.makedirs('save')
        if os.path.exists(self.scores_file):
            with open(self.scores_file, 'r') as f:
                try:
                    self.scores = json.load(f)
                    # Ensure all loaded scores have 'time_taken' and 'rating' keys
                    # This handles compatibility with older data.json files
                    for score_entry in self.scores:
                        if 'time_taken' not in score_entry:
                            score_entry['time_taken'] = 0 # Default value for old entries
                        if 'rating' not in score_entry:
                            score_entry['rating'] = self.get_text('not_available') # Default value for old entries
                except json.JSONDecodeError:
                    self.scores = []
        else:
            self.scores = []

    def save_score(self, name, score, time_taken, rating):
        self.scores.append({'name': name, 'score': score, 'time_taken': time_taken, 'rating': rating})
        # Sort scores in descending order by score, then ascending by time_taken for ties
        self.scores.sort(key=lambda x: (x['score'], -x['time_taken']), reverse=True)
        # Keep only the top 10 scores, for example
        self.scores = self.scores[:10]
        with open(self.scores_file, 'w') as f:
            json.dump(self.scores, f, indent=4)

    def update_history_display(self):
        self.history_list.clear()
        if not self.scores:
            self.history_list.addItem(self.get_text('no_history'))
            return

        for entry in self.scores:
            # Safely get time_taken and rating, providing defaults for old entries
            time_taken = entry.get('time_taken', 0)
            rating = entry.get('rating', self.get_text('not_available'))

            minutes = time_taken // 60
            seconds = time_taken % 60
            time_str = f"{minutes:02d}:{seconds:02d}"
            self.history_list.addItem(
                f"{entry['name']}: {entry['score']} {self.get_text('score')} | "
                f"{self.get_text('time')}: {time_str} | "
                f"{self.get_text('rating')}: {rating}"
            )

    def show_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu_page)
        self.update_history_display() # Ensure history is updated when returning to menu

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MathQuizApp()
    window.show()
    sys.exit(app.exec_())
