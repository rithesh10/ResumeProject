# Resume Screening Project

## Overview
This project is an AI-powered Resume Screening System that ranks resumes based on a given job description. It utilizes **sentence transformers** for semantic understanding, **cosine similarity search** for ranking, and is built using **Flask**, **React**, and **MongoDB** for full-stack functionality.

## Features
- **Job Description Input**: Allows recruiters to input a job description.
- **Resume Parsing & Storage**: Extracts key details from resumes and stores them in MongoDB.
- **AI-based Resume Ranking**: Uses sentence transformers and cosine similarity to rank resumes based on job relevance.
- **Real-time Results**: Displays ranked resumes dynamically using React.
- **Download & Export Options**: Provides options to export shortlisted resumes.
- **User Authentication**: Secure login system for recruiters.

## Tech Stack
- **Frontend**: React.js, Tailwind CSS
- **Backend**: Flask (Python)
- **AI Models**: Sentence Transformers
- **Database**: MongoDB (NoSQL storage for resumes and job descriptions)
- **Search Algorithm**: Cosine Similarity for relevance ranking

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/rithesh10/ResumeProject.git
   ```
2. Navigate to the project directory:
   ```sh
   cd resume-screening
   ```
3. Install dependencies:
   ```sh
   npm install  # For frontend
   pip install -r requirements.txt  # For backend
   ```
4. Start the backend server:
   ```sh
   python run.py
   ```
5. Start the frontend server:
   ```sh
   npm run dev
   ```

## Usage
- Open `http://localhost:5173` to access the frontend.
- Upload resumes in PDF format.
- Input job descriptions.
- View ranked resumes with scores.



## Future Enhancements
- Add resume keyword extraction.
- Improve UI/UX with better visualizations.
- Integrate multiple job descriptions for comparison.



## Contact
For any queries, reach out via:
- Email: asanthularithesh@gmail.com
- LinkedIn: [rithesh-asanthula](https://linkedin.com/in/rithesh-asanthula)
- GitHub: [rithesh10](https://github.com/rithesh10)

