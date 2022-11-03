// Pipeline 변수 
// def SLACK_CHANNEL = "develop-deployment-alarm"

// def DATE = new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSSXXX",TimeZone.getTimeZone('Asia/Seoul'));

// /* Slack 메시지 알람 함수 */
// def notifyCommon(slack_channel, message) {
//   def DD = new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSSXXX",TimeZone.getTimeZone('Asia/Seoul'));
//   slackSend (channel: "${slack_channel}", color: '#FFFF00', message: "${message} ${DD} \n 작업 : '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
// }

// /* Slack 성공 알람 함수 */
// def notifySuccessful(slack_channel) {
//   def DD = new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSSXXX",TimeZone.getTimeZone('Asia/Seoul'));
//   slackSend (channel: "${slack_channel}", color: '#00FF00', message: "CI/CD를 완료 하였습니다. ${DD} \n 작업 : '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
// }

// /* Slack 실패 알람 함수 */
// def notifyFailed(slack_channel) {
//   def DD = new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSSXXX",TimeZone.getTimeZone('Asia/Seoul'));
//   slackSend (channel: "${slack_channel}", color: '#FF0000', message: "CI/CD를 실패 하였습니다. ${DD} \n 작업 : '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
// }

node('jenkins-slave-pod') {  // 상위에 node 작성 'jenkins-slave-pod' 
    try {
        // Start alert
        // stage('Start alert'){
        //   notifyCommon(SLACK_CHANNEL,'Webhook을 감지하여 CI/CD 를 실행합니다.')
        // }

        // git clone 스테이지
        stage('Clone repository') {
              checkout scm
        }
        // slack alarm
        // stage('Git pull alarm') {
        //   notifyCommon(SLACK_CHANNEL, 'Webhook을 감지하여 Repository 를 복제했습니다.')
        // }
        // gradle build 스테이지
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

