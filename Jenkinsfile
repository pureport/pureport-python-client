pipeline {
    agent { dockerfile { filename '.jenkins/Dockerfile' } }
    stages {
        stage('Test') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'dev_api_url',
                        variable: 'PUREPORT_API_URL'
                    ),
                    usernamePassword(
                        credentialsId: 'dev_api_credentials',
                        usernameVariable: 'PUREPORT_API_KEY',
                        passwordVariable: 'PUREPORT_API_SECRET'
                    )
                ]) {
                    sh """ 
                        tox
                    """
                }
            }
            post {
                always {
                    publishHTML target: [
                        allowMissing: true,
                        alwaysLinkToLastBuild : true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Summary'
                    ]
                }
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
                    script {
                        version = sh(returnStdout: true, script: "python setup.py --version").trim()
                        sh """
                            git tag $version
                            git push https://$username:$password@github.com/pureport/pureport-python-client $version
                        """
                    }
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
