// Pipeline 변수 
def SLACK_CHANNEL = "devops"

def DATE = new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSSXXX",TimeZone.getTimeZone('Asia/Seoul'));

// /* Slack 메시지 알람 함수 */
def notifyCommon(slack_channel, message) {
  def DD = new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSSXXX",TimeZone.getTimeZone('Asia/Seoul'));
  slackSend (channel: "${slack_channel}", color: '#FFFF00', message: "${message} ${DD} \n TASK : '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
}

// /* Slack 성공 알람 함수 */
def notifySuccessful(slack_channel) {
  def DD = new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSSXXX",TimeZone.getTimeZone('Asia/Seoul'));
  slackSend (channel: "${slack_channel}", color: '#00FF00', message: "Complete a CI/CD. ${DD} \n TASK : '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
}

// /* Slack 실패 알람 함수 */
def notifyFailed(slack_channel) {
  def DD = new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSSXXX",TimeZone.getTimeZone('Asia/Seoul'));
  slackSend (channel: "${slack_channel}", color: '#FF0000', message: "Failure a CI/CD. ${DD} \n TASK : '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
}

//node('Built-In Node') {
pipeline{
    agent any
    options {
        skipStagesAfterUnstable()
    }
    try {
        // Start alert
        stage('Start alert'){
          notifyCommon(SLACK_CHANNEL,'Clone repository from git')
        }
        // git clone 스테이지
        stage('Clone repository') {
              checkout scm
        }
        // slack alarm
        stage('Git pull done') {
          notifyCommon(SLACK_CHANNEL, 'Complete a Clone')
        }
        // stage('test') {
        //   notifyCommon(SLACK_CHANNEL, 'test alarm for slack')
        // }
        // notifySuccessful(SLACK_CHANNEL)
    } catch(e) {
        /* 배포 실패 시 */
        currentBuild.result = "FAILED"
        // notifyFailed(SLACK_CHANNEL)
    }
}

