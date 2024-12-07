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

## ScreenShots For the App 
#Login Page

![WhatsApp Image 2024-12-07 at 20 54 49_5845f370](https://github.com/user-attachments/assets/6f5e7c9b-6340-4d04-9996-2b0129667e4b)


#Register Page 
#Students could register with the student role and teacher with the teacher role 

![WhatsApp Image 2024-12-07 at 20 59 12_6acd5479](https://github.com/user-attachments/assets/1079ae01-f1fb-4723-b6aa-6db9c6f0d311)


#Student login Page 
#Upon logging in each student could log in to their own account and only their details will be visible

![WhatsApp Image 2024-12-07 at 18 31 27_dacb3b11](https://github.com/user-attachments/assets/26df51a7-d966-421b-b3b0-26fb06865420)


#When a student selects a particular semester to view Marsheet

![WhatsApp Image 2024-12-07 at 18 31 48_01d4c398](https://github.com/user-attachments/assets/135f11ca-02fc-4ed6-a647-9e709988a192)
![WhatsApp Image 2024-12-07 at 18 32 30_cb3756af](https://github.com/user-attachments/assets/9e734c27-b498-4d5f-b896-d46dd9596c1b)


#When a student wishes to see the consolidated Marksheet then on selecting Consolidated Marksheet

![WhatsApp Image 2024-12-07 at 18 32 56_25d87853](https://github.com/user-attachments/assets/86a2a519-54a6-4074-8e29-89bfc67af4a5)
![WhatsApp Image 2024-12-07 at 18 33 17_7ae02ca2](https://github.com/user-attachments/assets/648df63e-78ed-4eee-9ecf-1a41ed021155)


#Now when the student wish to Generate the Marksheet and Download them
![image](https://github.com/user-attachments/assets/d49b0d45-8317-496b-9d36-f16977e49639)


Now when the student wishes to get some recommendation based on his Strengths and Weakness he could select the strengths and weakness
(This is Done with respect to the gemini API please visit : https://aistudio.google.com/  for further information)
![WhatsApp Image 2024-12-07 at 18 31 06_2eb4ca87](https://github.com/user-attachments/assets/a616a5f7-c80b-43f2-a8cf-0d23c7449b73)

Now When the teacher logs in They could see the details of any registered student
![WhatsApp Image 2024-12-07 at 20 53 52_79e96719](https://github.com/user-attachments/assets/aa96cf10-08c0-44fa-bb44-fa7997df9747)
![WhatsApp Image 2024-12-07 at 20 54 09_30692eab](https://github.com/user-attachments/assets/7bdf209e-5b4c-41f5-a8ab-784a4ffbf7d8)
![image](https://github.com/user-attachments/assets/5fca7d53-306b-4123-b65f-8ede4cb9eaa1)
![image](https://github.com/user-attachments/assets/1dbcefc7-d8c1-432e-8215-dfaf4d0b2b18)









