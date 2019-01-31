properties properties: [[$class: 'GitLabConnectionProperty', gitLabConnection: 'incubation-railai']]
pipeline {
    agent { label "devpi_client" }
    post {
          failure {
            updateGitlabCommitStatus name: 'Upload to Dev index', state: 'failed'
          }
          success {
            updateGitlabCommitStatus name: 'Upload to Dev index', state: 'success'
          }
        }
    stages {
        stage("test") {
            steps {
                sh """
                virtualenv test-venv -p python3
                . test-venv/bin/activate
                pip install -r requirements.txt
                pip install -r test/requirements.txt
                nose2 --verbose --with-coverage --coverage-report html --html-report --start-dir test/unit
                """
            }
            post {
                always {
                    junit testResults: '**/nose2-junit.xml'
                    archiveArtifacts artifacts: "**/test-report.html, **/htmlcov/*"

                }
                success {
                    sh("devpi use http://10.62.65.209:4040")
                    sh("devpi login railai --password=changeme")
                    sh("devpi use railai/dev")
                    sh("devpi upload")
                    deleteDir()
                }
                failure {
                    deleteDir()
                }
            }
        }
    }
}