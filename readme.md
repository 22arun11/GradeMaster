# Project Title

GradeMaster

## Description

GradeMaster is a web application for managing student grades and generating marksheets. It allows students to view their grades and teachers to manage student information and generate consolidated marksheets.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/yourusername/GradeMaster.git
    cd GradeMaster
    ```

2. **Create a virtual environment**:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database**:

    ```sh
    python manage.py migrate
    ```

5. **Create a superuser**:

    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server**:

    ```sh
    python manage.py runserver
    ```

## Usage

1. **Access the application**:

    Open your web browser and go to `http://127.0.0.1:8000/`.

2. **Login**:

    Use the superuser credentials to log in to the admin panel at `http://127.0.0.1:8000/admin/`.

3. **Manage Students and Teachers**:

    - Add students and teachers through the admin panel.
    - Teachers can log in and view student marksheets.

4. **Generate Marksheet**:

    - Students can view their marksheets.
    - Teachers can generate consolidated marksheets.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.