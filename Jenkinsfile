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
        // stage('Testing server') {
        //     steps {

        //         echo "Testing.. "
        //         sh 'kubectl get pods --context=minikube'
        //     }
        // }
    }
}
