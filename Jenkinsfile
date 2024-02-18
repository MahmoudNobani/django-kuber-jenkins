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
                withKubeConfig([credentialsId: 'user1', serverUrl: 'http://192.168.49.2:32171/']) {
                sh 'kubectl exec -it deploy/django-app -- pytest meal/tests.py employee/tests.py'
                }
        }
    }
}
