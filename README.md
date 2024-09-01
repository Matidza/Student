

# Student Card Project

## Project Overview

The **Student Card Project** is a web application designed for students at North West University. It provides a streamlined platform for students to access their exam timetables quickly, without the hassle of navigating through the entire university website. The project aims to improve the student experience by offering easy access to crucial academic information.

## Features

- **Quick Access:** Students can view their exam timetables with just a few clicks.
- **User-Friendly Interface:** A clean and responsive design, making it easy for students to use on any device.
- **Secure Authentication:** Ensures that only authorized users can access their personal information.

## Technologies Used

### Back-End
- **Python:** Core programming language used for logic and functionality.
- **Flask:** Lightweight web framework used to develop the back-end of the application.
- **MySQL:** Relational database used for storing user data securely.

### Front-End
- **HTML:** Structure and content of the web pages.
- **CSS:** Styling to make the web pages visually appealing.
- **Bootstrap:** Responsive design framework to ensure the application works well on different screen sizes.

## Installation and Setup

### Clone the Repository

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/student-card-project.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd student-card-project
   ```

### Set Up in Visual Studio Code

1. **Open the Project in VS Code:**
   - Open Visual Studio Code.
   - Click on `File > Open Folder...` and select the `student-card-project` directory.

2. **Set Up a Virtual Environment:**
   - Open the integrated terminal in VS Code (`Ctrl + `` or `Terminal > New Terminal`).
   - Run the following command to create a virtual environment:
     ```bash
     python -m venv venv
     ```

3. **Activate the Virtual Environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the Required Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up the MySQL Database:**
   - Create a new database in MySQL.
   - Update the database configuration in the `config.py` file with your database credentials.
   - Run the migrations to set up the database tables:
     ```bash
     flask db upgrade
     ```

6. **Run the Application:**
   - In the integrated terminal, run:
     ```bash
     flask run
     ```
   - The application will be accessible at `http://127.0.0.1:5000/`.

### Contributing to the Project

We welcome contributions from the community! If you'd like to contribute to the **Student Card Project**, please follow these steps:

1. **Fork the Repository:**
   - Click the "Fork" button on the top right of the project repository page.

2. **Clone Your Fork:**
   - Clone your forked repository to your local machine:
     ```bash
     git clone https://github.com/yourusername/student-card-project.git
     ```

3. **Create a New Branch:**
   - Create a new branch for your feature or bug fix:
     ```bash
     git checkout -b feature-name
     ```

4. **Make Your Changes:**
   - Develop your feature or fix the bug in your new branch.
   - Ensure your code adheres to the project's coding standards.

5. **Commit Your Changes:**
   - Commit your changes with a descriptive commit message:
     ```bash
     git commit -m "Add feature XYZ"
     ```

6. **Push to Your Fork:**
   - Push your branch to your forked repository:
     ```bash
     git push origin feature-name
     ```

7. **Submit a Pull Request:**
   - Go to the original repository on GitHub and submit a pull request with a clear description of your changes.

8. **Review Process:**
   - Your pull request will be reviewed, and feedback may be provided. Once approved, it will be merged into the main branch.

## License




## Contact

If you have any questions or suggestions, feel free to reach out:

- **Email:** [matidza.mukwevho.z@gmail.com](matidza.mukwevho.z@gmail.com)
- **Portfolio:** [https://matidza.w3spaces.com/index.html](https://matidza.w3spaces.com/index.html)


