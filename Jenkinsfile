pipeline {
    agent any

    stages {
        stage('Deploy App') {
            steps {
                script {
                    kubernetesDeploy(configFile: "manifest.yaml", kubeconfigId: "minikube")
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
