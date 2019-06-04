import groovy.json.JsonSlurper
properties properties: [[$class: 'GitLabConnectionProperty', gitLabConnection: 'incubation-railai']]

pipeline {
    agent { label "devpi_client" }
    environment {
        JFROG_CREDS = credentials("railai-jfrog-credential")
    }
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

                    script {
                        try {
                            def materialJson = readFile "material.json"
                            println(materialJson)
                            // Json String to Map
                            def materialMap = new JsonSlurper().parseText(materialJson)
                            println(materialMap.version)
                            env.VERSION = materialMap.version
                            env.PACKAGE_NAME = materialMap.package_name
                        }
                        catch(exc) {
                            println("ignore this error")
                        }
                        sh("python3 setup.py egg_info -b \"\" sdist")
                        sh("curl -u ${JFROG_CREDS_USR}:${JFROG_CREDS_PSW} -T dist/${PACKAGE_NAME}-${VERSION}.tar.gz https://artifactory.isus.emc.com/artifactory/ACE-python-dev-local/dev/${PACKAGE_NAME}/${PACKAGE_NAME}-${VERSION}.tar.gz")
                    }

                    deleteDir()
                }
                failure {
                    deleteDir()
                }
            }
        }
    }
}