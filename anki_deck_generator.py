import genanki
import uuid
import tkinter as tk
from tkinter import messagebox

# Function to generate unique IDs for decks
def generate_unique_id():
    return int(str(uuid.uuid4().int)[:10])

# Function to generate a unique model ID
def generate_model_id():
    return int(str(uuid.uuid4().int)[:10])

# Define the basic note model globally with a unique ID and name
basic_note_model = genanki.Model(
    generate_model_id(),  # Unique model ID
    'Unique Placeholder Model XYZ123',  # Unique model name
    fields=[
        {'name': 'Front'},
        {'name': 'Back'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Front}}',
            'afmt': '{{Back}}',
        },
    ]
)

# Function to create an Anki deck
def create_anki_deck(deck_name):
    deck_id = generate_unique_id()
    print(f"Creating deck: {deck_name}")
    return genanki.Deck(deck_id, deck_name)

# Function to create a placeholder note (flashcard)
def create_placeholder_note(deck_name):
    return genanki.Note(
        model=basic_note_model,
        fields=[deck_name, '']  # Use the deck name as the 'Front' field content
    )

# Function to recursively create decks and add placeholder cards at the final level
def build_anki_decks(deck_name_prefix, deck_data):
    deck = create_anki_deck(deck_name_prefix)
    
    # Add a placeholder note if this is the final level (no children)
    if not deck_data["children"]:
        print(f"Adding note to deck: {deck_name_prefix}")
        note = create_placeholder_note(deck_name_prefix)
        deck.add_note(note)
    
    all_decks = [deck]
    
    # Recursively build sub-decks
    for subdeck_name, subdeck_data in deck_data["children"].items():
        full_subdeck_name = f"{deck_name_prefix}::{subdeck_name}"
        sub_decks = build_anki_decks(full_subdeck_name, subdeck_data)
        all_decks.extend(sub_decks)
    
    return all_decks

# Function to process the input text and create the Anki package
def convert_to_anki_package_from_text(input_text):
    text_lines = input_text.strip().split('\n')
    
    # Parse deck hierarchy from the text
    deck_hierarchy = {}
    for line in text_lines:
        levels = line.strip().split('::')
        
        # Skip empty or invalid lines
        if len(levels) < 2:
            print(f"Skipping line: {line.strip()} (invalid format)")
            continue
        
        # Extract the main deck name
        main_deck_name = levels[0]
        if main_deck_name not in deck_hierarchy:
            deck_hierarchy[main_deck_name] = {"children": {}}
        
        current_level = deck_hierarchy[main_deck_name]["children"]
        for level in levels[1:]:
            if level not in current_level:
                current_level[level] = {"children": {}}
            current_level = current_level[level]["children"]
    
    all_decks = []
    for main_deck_name, main_deck_data in deck_hierarchy.items():
        # Build all decks starting from the main deck
        decks = build_anki_decks(main_deck_name, main_deck_data)
        all_decks.extend(decks)
    
    # Create the Anki package
    package = genanki.Package(all_decks)
    
    # Write the Anki package to a file
    package_file_name = f'{main_deck_name}_nested_deck_structure.apkg'
    package.write_to_file(package_file_name)
    print(f"Anki package created: {package_file_name}")
    
    # Inform the user that the process is complete
    messagebox.showinfo("Completed", f"Anki package created: {package_file_name}")

# Function to handle the "Generate Prompt" button click
def generate_prompt():
    exam_name = exam_name_entry.get().strip()
    if not exam_name:
        messagebox.showwarning("Warning", "Please enter the exam name.")
        return
    
    # Generate the prompt based on the exam name
    prompt_text = f"""
Objective: Develop a comprehensive and detailed structure of topics, subtopics, and lessons for the {exam_name} exam. The focus is on creating a granular and extensive content map tailored for educational content creation, specifically for Anki decks or similar educational tools.

Requirements:

1. **Exhaustive Content Breakdown:**

   - **Topics:** Each main topic should be segmented into multiple subtopics, covering all major and minor areas relevant to the {exam_name} exam.

   - **Subtopics:** Each subtopic should encapsulate at least three detailed lessons, ensuring a thorough examination of the material.

   - **Lessons:** Lessons must articulate specific, actionable concepts, presenting clear educational objectives.

2. **Granular and Specific Lessons:**

   - **Lesson titles** must precisely define the concept, theory, rule, process, or application they cover, each aiming to deliver a singular learning objective.

3. **Formatting and Structure:**

   - Adhere to a strict formatting protocol for readability and consistency, with each entry presented on a new line, structured as shown in the example.

   - Use the following format:

     ```
     {exam_name}::Topic::Subtopic::Lesson
     ```

4. **Research and Accuracy:**

   - Perform in-depth research using the most current textbooks, official exam content outlines, recognized study guides, and reputable educational platforms.

   - Utilize reliable sources to access the latest and most relevant materials.

5. **Length and Detail:**

   - Ensure that the structure is comprehensive, aiming for a minimum of 10 lines per topic.

   - For an exam with 10 topics, the total number of lines should be approximately 120-150 lines.

Example Format:

This is a sample structure for the "{exam_name}" exam, designed to illustrate the desired output format. The full output should be similarly comprehensive, covering all necessary topics and lessons thoroughly and meticulously.
Exam::Ethical and Professional Standards::Code of Ethics::Lesson 1: Introduction to Ethics
Exam::Ethical and Professional Standards::Code of Ethics::Lesson 2: Ethical Responsibilities
Exam::Ethical and Professional Standards::Standards I-VII::Lesson 1: Overview
Exam::Ethical and Professional Standards::Standards I-VII::Lesson 2: Applications
(+ 140 lines after this)

Execution:

The generation of this structure can be computationally intensive, focusing on quality and granularity over speed. The system should methodically cover all aspects of the exam's content, ensuring no area is overlooked. This task should be approached with diligence, ensuring a slow and thorough process.

Note: The aim is to produce a well-organized, detailed content structure that can be transformed into educational formats like Anki decks, covering all key areas comprehensively.

---

Please generate the complete content in a UNIQUE code block, not just a few lines. Ensure a minimum of 10 lines per topic, aiming for an average of 120-150 lines for the entire exam. Take your time to produce a thorough and detailed structure.
"""
    # Display the prompt in the prompt_text widget
    prompt_text_widget.config(state=tk.NORMAL)
    prompt_text_widget.delete("1.0", tk.END)
    prompt_text_widget.insert(tk.END, prompt_text.strip())
    prompt_text_widget.config(state=tk.DISABLED)

# Function to copy the prompt to the clipboard
def copy_prompt():
    prompt = prompt_text_widget.get("1.0", tk.END).strip()
    if not prompt:
        messagebox.showwarning("Warning", "No prompt to copy. Please generate the prompt first.")
        return
    root.clipboard_clear()
    root.clipboard_append(prompt)
    messagebox.showinfo("Copied", "Prompt copied to clipboard.")

# Function to handle the "Generate Anki Package" button click
def generate_anki_package():
    input_text = text_input.get("1.0", tk.END)
    if not input_text.strip():
        messagebox.showwarning("Warning", "Please paste the text generated by ChatGPT.")
        return
    try:
        convert_to_anki_package_from_text(input_text)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

# Create the main window
root = tk.Tk()
root.title("Anki Deck Generator")

# Exam Name Input
exam_name_label = tk.Label(root, text="Enter the exam you are preparing for:")
exam_name_label.pack(pady=5)
exam_name_entry = tk.Entry(root, width=50)
exam_name_entry.pack(pady=5)

# Generate Prompt Button
generate_prompt_button = tk.Button(root, text="Generate Prompt", command=generate_prompt)
generate_prompt_button.pack(pady=5)

# Prompt Display
prompt_label = tk.Label(root, text="Generated Prompt:")
prompt_label.pack(pady=5)
prompt_text_widget = tk.Text(root, height=15, width=80, state=tk.DISABLED)
prompt_text_widget.pack(padx=10, pady=5)

# Copy Prompt Button
copy_prompt_button = tk.Button(root, text="Copy Prompt to Clipboard", command=copy_prompt)
copy_prompt_button.pack(pady=5)

# Instructions
instructions_label = tk.Label(root, text="After generating the prompt, copy it, paste it into ChatGPT, and obtain the structured content. Then, paste the result below:")
instructions_label.pack(pady=10)

# Text Input for ChatGPT Response
text_input = tk.Text(root, height=15, width=80)
text_input.pack(padx=10, pady=5)

# Generate Anki Package Button
generate_button = tk.Button(root, text="Generate Anki Package", command=generate_anki_package)
generate_button.pack(pady=10)

# Start the GUI loop
root.mainloop()
