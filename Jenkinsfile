pipeline {
    agent any

    stages {
        stage("minikube") {
            steps {
                script {
                    sh '''
                        wget https://github.com/kubernetes-sigs/cri-tools/releases/download/v1.26.0/crictl-v1.26.0-linux-amd64.tar.gz
                        sudo tar zxvf crictl-v1.26.0-linux-amd64.tar.gz -C /usr/local/bin
                        crictl --version
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
