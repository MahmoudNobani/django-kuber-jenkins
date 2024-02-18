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
                    kubernetesDeploy(configs: "manifist.yaml", kubeconfigId: "kube-cred")                    
                }
            }
        }
        stage('Testing server') {
            steps {

                echo "Testing.. "
                sh '''curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl
                sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
                chmod +x kubectl
                mkdir -p ~/.local/bin
                mv ./kubectl ~/.local/bin/kubectl
                kubectl version --client
                '''
            }
        }
    }
}
