pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker-credentials')
        }
    stages {
        stage("building images") {
            steps {
                script {
                    sh '''
                        docker build -t mahmoudnobani/my_django_image .
                    '''
                    // docker.withRegistry('https://index.docker.io/v1/', 'docker-credentials') {
                    //     docker.build('mahmoudnobani/my_django_image')
                    // }
                }
            }
        }
        stage("push image") {
            steps {
                script {
                    sh '''
                        docker login -u $DOCKERHUB_CREDENTIALS_USR -p $DOCKERHUB_CREDENTIALS_PSW 
		                docker push mahmoudnobani/my_django_image
                    '''
                }
                // script {
                //     docker.withRegistry('https://index.docker.io/v1/', 'docker-credentials') {
                //         docker.build('mahmoudnobani/my_django_image').push('latest')
                //     }
                // }
            }
        }
        stage('Deploy App') {
            steps {
                script {
                    withKubeConfig([credentialsId: 'myKubeConfig']) {
                        sh 'kubectl apply -f manifist.yaml'
                        sh 'kubectl rollout status deployment django-app postgresql -w --timeout 5m'
                    }
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
