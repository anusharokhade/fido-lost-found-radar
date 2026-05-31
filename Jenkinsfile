pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git 'https://github.com/anusharokhade/fido-lost-found-radar.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t fido-app .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker stop fido-container || true'
                sh 'docker rm fido-container || true'
            }
        }

        stage('Deploy Container') {
            steps {
                sh 'docker run -d -p 8501:8501 --name fido-container fido-app'
            }
        }
    }
}