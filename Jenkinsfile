pipeline {
    agent any

    stages {
        stage("minikube") {
            steps {
                script {
                    sh '''
                        sh 'sudo yum install -y yum-utils'
                        sh 'sudo yum-config-manager --add-repo https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable/CentOS_7/devel:kubic:libcontainers:stable.repo'
                        sh 'sudo yum install -y cri-tools'
                        sudo yum -y install conntrack
                        echo $USER
                        sudo usermod -aG docker $USER
                        curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
                        sudo install minikube-linux-amd64 /usr/local/bin/minikube
                        sudo chown -R $USER ~/.minikube
                        minikube start --driver=none'''
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
