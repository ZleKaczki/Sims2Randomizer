import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QTextEdit, \
    QLabel, QCheckBox, QInputDialog
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from PyQt5.QtCore import Qt
import random
import json


class SimulationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.include_pets_enabled = False  # Initialize to False

        self.include_pets_checkbox = QCheckBox("Include Cats and Dogs")
        self.include_pets_checkbox.setChecked(False)  # Default to not include pets
        self.include_pets_checkbox.stateChanged.connect(self.on_include_pets_changed)

        self.add_event_button = QPushButton("Add Event")
        self.add_event_button.clicked.connect(self.add_event)

        self.remove_event_button = QPushButton("Remove Event")
        self.remove_event_button.clicked.connect(self.remove_event)
        self.initUI()

    def on_include_pets_changed(self, state):
        if state == Qt.Checked:
            self.include_pets_enabled = True
        else:
            self.include_pets_enabled = False

    def initUI(self):
        self.setWindowTitle('Sims 2 Randomizer')
        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(149, 164, 219))
        self.setPalette(palette)

        # Load categories from JSON file
        with open('characters.json') as f:
            character_data = json.load(f)
            self.chemistry_traits = character_data['chemistry']
            self.aspirations = character_data['aspiration']
            self.color = character_data['fav_color']

        # Load events from JSON file
        self.load_events()

        with open('family.json') as f:
            self.family_data = json.load(f)

        self.setWindowIcon(QIcon('graphics/icon.png'))
        # Set font
        font = QFont("ITC Benguiat Gothic", 14)
        self.setFont(font)

        # Create buttons
        self.sim_button = QPushButton('Randomize Sim')
        self.event_button = QPushButton('Random Event')
        self.family_button = QPushButton('Randomize Family')

        # Set button style
        button_style = """
                    QPushButton {
                        color: rgb(10, 18, 101);
                        background-color: rgb(174,189,255); /* Blue color similar to Sims 2 */
                        border: 3px solid rgb(10, 18, 101); /* Border color */
                        border-radius: 10px;
                        padding: 10px 20px;
                    }
                    QPushButton:hover {
                        background-color: #4D90FE; /* Darker shade when hovered */
                    }
                """
        self.setStyleSheet(button_style)

        # Connect button signals to slots
        self.sim_button.clicked.connect(self.randomize_sim)
        self.event_button.clicked.connect(self.random_event)
        self.family_button.clicked.connect(self.randomize_family)

        # Create text edit widget
        self.info_display = QTextEdit()
        self.info_display.setReadOnly(True)
        self.info_display.setFont(font)
        self.info_display.setStyleSheet("background-color: rgb(174,189,255); color: rgb(10, 18, 101); border: 3px solid rgb(10, 18, 101); padding: 10px 20px; border-radius: 10px;")
        self.info_display.setLineWrapMode(QTextEdit.NoWrap)

        # Create layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.sim_button)
        button_layout.addWidget(self.event_button)
        button_layout.addWidget(self.family_button)

        button_layout.setAlignment(Qt.AlignCenter)

        # Create layout for the main window
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.include_pets_checkbox)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.info_display)
        main_layout.setContentsMargins(50, 20, 50, 20)
        main_layout.addWidget(self.add_event_button)
        main_layout.addWidget(self.remove_event_button)

        self.setLayout(main_layout)
        self.setWindowState(Qt.WindowMaximized)

    def randomize_sim(self):
        # Initialize trait points
        traits = {"lazy/active": 0, "sloppy/neat": 0, "serious/playful": 0, "grouchy/nice": 0, "shy/outgoing": 0}

        # Allocate 50 points among traits
        points_remaining = 25
        for _ in range(points_remaining):
            # Randomly select a trait
            trait = random.choice(list(traits.keys()))

            # Increment trait value by one, ensuring it doesn't exceed 10
            if traits[trait] < 10:
                traits[trait] += 1
            else:
                # Choose a different trait
                remaining_traits = [t for t in traits if traits[t] < 10]
                if remaining_traits:
                    new_trait = random.choice(remaining_traits)
                    traits[new_trait] += 1
        # Display result
        result_text = "Traits:\n"
        for trait, value in traits.items():
            result_text += f"{trait.capitalize()}: {value}\n"

        # Randomly select chemistry traits
        chemistry_traits = random.sample(self.chemistry_traits, 3)
        result_text += "\nChemistry Traits:\n"
        result_text += "Turn Ons: "
        for i in range(2):
            result_text += f"{chemistry_traits[i]}, "
        result_text += "\nTurn Off: "
        result_text += f"{chemistry_traits[2]}\n"

        # Randomly select an aspiration
        aspiration = random.choice(self.aspirations)
        result_text += f"\nAspiration: {aspiration}\n"

        color = random.choice(self.color)
        result_text += f"\nFavorite color: {color}\n"
        result_text += "________"

        # Append new text to existing text
        self.append_to_info_display(result_text)

    def random_event(self):
        if not self.events['events']:
            QMessageBox.warning(self, "Error", "No events available to randomize.")
            return

        # Random selection
        random_event = random.choice(self.events['events'])
        text_event = f"{random_event}\n_______"

        # Display text
        self.append_to_info_display(text_event)

    def load_events(self):
        # Load events from the JSON file
        try:
            with open("events.json", "r") as file:
                self.events = json.load(file)
        except FileNotFoundError:
            self.events = {"events": []}

    def save_events(self):
        # Save events to the JSON file
        with open("events.json", "w") as file:
            json.dump(self.events, file, indent=4)

    def add_event(self):
        # Open a dialog to get the new event from the user
        new_event, ok_pressed = QInputDialog.getText(self, "Add Event", "Enter the new event:")

        # If the user pressed OK and entered a new event
        if ok_pressed and new_event.strip():
            # Add the new event to the list of events
            self.events['events'].append(new_event)
            self.save_events()  # Save events to the JSON file
            QMessageBox.information(self, "Success", "Event added successfully.")
        elif ok_pressed and not new_event.strip():
            QMessageBox.warning(self, "Error", "Event name cannot be empty.")

    def remove_event(self):
        if not self.events['events']:
            QMessageBox.warning(self, "Error", "No events available.")
            return

        # Create a list of event names for the user to select from
        event_names = self.events['events']

        # Open a dialog for the user to select an event to remove
        selected_event, ok_pressed = QInputDialog.getItem(self, "Remove Event", "Select an event to remove:",
                                                          event_names, editable=False)

        # If the user pressed OK and selected an event
        if ok_pressed and selected_event:
            # Remove the selected event from the list of events
            self.events['events'].remove(selected_event)
            self.save_events()  # Save events to the JSON file
            QMessageBox.information(self, "Success", "Event removed successfully.")
        elif ok_pressed and not selected_event:
            QMessageBox.warning(self, "Error", "Please select an event to remove.")

    def randomize_family(self):
        # Randomize number of sims
        first_gender = random.choice(self.family_data['gender'])
        num_sims = random.randint(*self.family_data['nr_of_sims'])
        family_text = f"Number of Family Members: {num_sims}\n\n"
        family_text += f"Sim 1: Adult, {first_gender}\n"

        for i in range(1, num_sims):  # Start the loop from the second sim
            if self.include_pets_enabled:
                age = random.choice(self.family_data['animal'])
            else:
                age = random.choice(self.family_data['age'])
            gender = random.choice(self.family_data['gender'])
            family_text += f"Sim {i + 1}: {age}, "
            family_text += f"{gender}\n"
        family_text += "\n_______"

        # Display text
        self.append_to_info_display(family_text)

    def append_to_info_display(self, text):
        # Append new text to existing text
        current_text = self.info_display.toPlainText()
        self.info_display.setPlainText(current_text + '\n\n' + text)

        # Scroll to the end of the text window
        scroll_bar = self.info_display.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

        # Hide the scroll bar
        self.info_display.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimulationApp()
    window.show()
    sys.exit(app.exec_())
