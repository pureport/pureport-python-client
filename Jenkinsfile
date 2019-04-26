pipeline {
    agent { dockerfile { filename '.jenkins/Dockerfile' } }
    stages {
        stage('Lint') {
            steps {
                sh """
                    flake8
                """
            }
        }
        stage('Build') {
            steps {
                sh """
                    python setup.py sdist bdist_wheel
                """
            }
        }
        stage('Archive') {
            steps {
                archiveArtifacts 'dist/*'
            }
        }
        stage('Release') {
            when {
                branch 'master'
            }
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'pypi_credentials',
                        usernameVariable: 'TWINE_USERNAME',
                        passwordVariable: 'TWINE_PASSWORD'
                    )
                ]) {
                    sh """
                        twine upload dist/*
                    """
                }
                withCredentials([
                    usernamePassword(
                        credentialsId: 'git_credentials',
                        usernameVariable: 'username',
                        passwordVariable: 'password'
                    )
                ]) {
                    sh """
                        version=\$(python setup.py --version)
                        git tag $version
                        git push https://$username:$password@github.com/pureport/pureport-python-client $version
                    """
                }
            }
        }
    }
    post {
        success {
            slackSend(color: '#30A452', message: "SUCCESS: <${env.BUILD_URL}|${env.JOB_NAME}#${env.BUILD_NUMBER}>")
        }
        unstable {
            slackSend(color: '#DD9F3D', message: "UNSTABLE: <${env.BUILD_URL}|${env.JOB_NAME}#${env.BUILD_NUMBER}>")
        }
        failure {
            slackSend(color: '#D41519', message: "FAILED: <${env.BUILD_URL}|${env.JOB_NAME}#${env.BUILD_NUMBER}>")
        }
    }
}
