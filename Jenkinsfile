pipeline {
agent any

```
stages {

    stage('Clone Repository') {
        steps {
            git branch: 'main',
            url: 'https://github.com/anusharokhade/fido-lost-found-radar.git'
        }
    }

    stage('Build Docker Image') {
        steps {
            sh 'echo Building Docker image...'
        }
    }

    stage('Stop Old Container') {
        steps {
            sh 'echo Stopping old container...'
        }
    }

    stage('Deploy Container') {
        steps {
            sh 'echo Deploying application...'
        }
    }
}
```

}
