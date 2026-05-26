pipeline {
    agent any

    stages {

        stage('Clone Repo') {
            steps {
                git branch: 'main',
                url: 'https://github.com/anusharokhade/fido-lost-found-radar.git'
            }
        }

        stage('Install Requirements') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t fido-project .'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker run -d -p 8501:8501 --name fido-container fido-project'
            }
        }
    }
}