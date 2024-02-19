pipeline {
    agent any

    stages {
        stage("Minikube") {
            steps {
                script {
                    sh '''
                        docker ps
                    '''
                }
            }
        }
        stage('Deploy App') {
            steps {
                script {
                    withKubeConfig([credentialsId: 'myKubeConfig']) {
                        sh 'kubectl apply -f manifist.yaml'
                        sh 'kubectl rollout status deployment django-app postgresql -w --timeout 5m'
                    }
                    //kubernetesDeploy(configs: "manifist.yaml", kubeconfigId: "kube-cred")                    
                }
            }
        }
        stage('Testing server') {
            steps {
                withKubeConfig([credentialsId: 'myKubeConfig']) {
                    sh 'kubectl exec -it deploy/django-app -- pytest meal/tests.py employee/tests.py'
                }
            }
        }
    }
}
