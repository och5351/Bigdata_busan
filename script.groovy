// slack 채널 변수
def SLACK_CHANNEL = "devops"

// 함수
def notifyCommon(slack_channel, message) {
    slackSend (channel: "${slack_channel}", color: '#FFFF00', message: "${message}")
}


node('master') {
    try {
        //
        stage('Start alert'){
            notifyCommon(SLACK_CHANNEL, 'Clone Repository from git')
        }

        //
        stage('Build'){

        }
        
        stage('test'){

        }

        stage('deploy'){

        }
    }
}

//