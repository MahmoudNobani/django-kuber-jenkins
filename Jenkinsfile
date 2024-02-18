pipeline {
    agent any

    stage('Deploy App') {
      steps {
        script {
          kubernetesDeploy(configs: "manifist.yaml", kubeconfigId: "minikube")
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