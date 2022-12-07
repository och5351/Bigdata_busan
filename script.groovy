// slack 채널 변수
def SLACK_CHANNEL = "jenkins"

// /* Slack 메시지 알람 함수 */
def notifyCommon(slack_channel, message) {
    def DD = new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSSXXX",TimeZone.getTimeZone('Asia/Seoul'));
    slackSend (channel: "${slack_channel}", color: '#FFFF00', message: "${message} \n ${DD} \n TASK : '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
}

// /* Slack 성공 알람 함수 */
def notifySuccessful(slack_channel) {
  def DD = new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSSXXX",TimeZone.getTimeZone('Asia/Seoul'));
  slackSend (channel: "${slack_channel}", color: '#00FF00', message: "Complete a CI/CD. \n ${DD} \n TASK : '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
}

// /* Slack 실패 알람 함수 */
def notifyFailed(slack_channel) {
  def DD = new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSSXXX",TimeZone.getTimeZone('Asia/Seoul'));
  slackSend (channel: "${slack_channel}", color: '#FF0000', message: "Failure a CI/CD. \n ${DD} \n TASK : '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
}

env.TARGET_HOST = 'ubuntu@54.180.131.194'

node {
    try {
        
        stage('Start alert'){
            notifyCommon(SLACK_CHANNEL, 'Clone Repository from git')
        }
        
        stage('Clone'){
            checkout scm
        }

        stage('Build alert'){
            notifyCommon(SLACK_CHANNEL, 'Build Start')
        }

        stage('Build'){
            echo 'Building...'
            // sh ('ssh ubuntu@ec2 "cd test"')
            // sh ('ssh ubuntu@ec2 "kill -9 %1"')
            sh ('ssh ubuntu@ec2 "source /home/ubuntu/venvs/dogma/bin/activate"')
            sh ('ssh ubuntu@ec2 "pwd"')
            sh ('ssh ubuntu@ec2 "cd /home/ubuntu/projects/Bigdata_busan/ldg/project && pwd && git pull"')
        }

        stage('Deploy alert'){
            notifyCommon(SLACK_CHANNEL, 'Deploy Start')
        }

        stage('deploy'){
            sh ('ssh ubuntu@ec2 "cd /home/ubuntu/venvs && . flaskRunner.sh"')
            // sh ('ssh ubuntu@ec2 "export FLASK_APP=dogma"')
            // sh ('ssh ubuntu@ec2 "export FLASK_DEBUG=true"')
            // sh ('ssh ubuntu@ec2 "export APP_CONFIG_FILE=/home/ubuntu/projects/Bigdata_busan/ldg/project/config/production.py"')
            // sh 'ssh -v ubuntu@54.180.131.194'
            // sh 'ssh ubuntu@54.180.131.194 mkdir ~/test'
            }

        stage('Complete alert') {
          notifySuccessful(SLACK_CHANNEL)
        }


        } catch(e) {
        currentBuild.result = "FAILED"

        stage('Failed alert') {
          notifyFailed(SLACK_CHANNEL)
        }
    }
}

//