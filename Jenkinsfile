pipeline {
    agent any

    stages {
        stage("minikube") {
            steps {
                script {
                    sh '''echo $USER
                        sudo usermod -aG docker $USER
                        curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
                        sudo install minikube-linux-amd64 /usr/local/bin/minikube
                        minikube start'''
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
