// slack 채널 변수
def SLACK_CHANNEL = "jenkins"

// 함수
def notifyCommon(slack_channel, message) {
    slackSend (channel: "${slack_channel}", color: '#FFFF00', message: "${message}")
}

// /* Slack 성공 알람 함수 */
def notifySuccessful(slack_channel) {
  def DD = new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSSXXX",TimeZone.getTimeZone('Asia/Seoul'));
  slackSend (channel: "${slack_channel}", color: '#00FF00', message: "Complete a CI/CD. ${DD} \n TASK : '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
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

        stage('git pull'){
            notifyCommon(SLACK_CHANNEL, 'Build Start')
        }

        stage('Build'){
            echo 'Building...'
            // sh ('ssh ubuntu@ec2 "cd test"')
            sh ('ssh ubuntu@ec2 "source /home/ubuntu/venvs/dogma/bin/activate"')
            // sh ('ssh ubuntu@ec2 "cd ~/projects/Bigdata_busan/ldg/project"')
            sh ('ssh ubuntu@ec2 "pwd"')
            sh ('ssh ubuntu@ec2 "export FLASK_APP=dogma"')
            sh ('ssh ubuntu@ec2 "export FLASK_DEBUG=true"')
            sh ('ssh ubuntu@ec2 "export APP_CONFIG_FILE=/home/ubuntu/projects/Bigdata_busan/ldg/project/config/production.py"')
            sh ('ssh ubuntu@ec2 "cd /home/ubuntu/projects/Bigdata_busan/ldg/project && pwd && git pull"')
        }

        stage('test'){
            
        }

        stage('deploy'){
            // sh 'ssh -v ubuntu@54.180.131.194'
            // sh 'ssh ubuntu@54.180.131.194 mkdir ~/test'
            }


        } catch(e) {
        currentBuild.result = "FAILED"
    }
}

//