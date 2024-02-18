pipeline {
    agent any

    stages {
        stage("minikube") {
            steps {
                script {
                    sh '''
                        docker ps'''
                }
            }
        }
        stage('Deploy App') {
            steps {
                script {
                    sh 'kubectl apply -f manifist.yaml'
                }
            }
        }
        stage('Testing server') {
            steps {
                echo "Testing.."
                sh './test.sh'
            }
        }
    }
}
