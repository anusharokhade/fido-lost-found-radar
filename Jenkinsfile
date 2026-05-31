pipeline {
agent any

stages {

    stage('Clone Repository') {
        steps {
            git branch: 'main',
                url: 'https://github.com/anusharokhade/fido-lost-found-radar.git'
        }
    }

    stage('Deploy to EC2') {
        steps {
            sshagent(['ec2-key']) {
                sh '''
                ssh -o StrictHostKeyChecking=no ubuntu@3.108.228.207 "
                cd ~/fido-lost-found-radar &&
                git pull origin main &&
                sudo docker stop fido-container || true &&
                sudo docker rm fido-container || true &&
                sudo docker build -t fido-app . &&
                sudo docker run -d -p 8501:8501 --name fido-container fido-app
                "
                '''
            }
        }
    }
}

}
