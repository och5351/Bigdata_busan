// slack 채널 변수
def SLACK_CHANNEL = "jenkins"

// 함수
def notifyCommon(slack_channel, message) {
    slackSend (channel: "${slack_channel}", color: '#FFFF00', message: "${message}")
}

def remote = [:]
remote.name = 'ubuntu'
remote.host = '54.180.131.194'
remote.allowAnyHosts = true
remote.user = 'ubuntu'

node('master') {
    try {
        //
        // stage('Start alert'){
        //     notifyCommon(SLACK_CHANNEL, 'Clone Repository from git')
        // }

        //
        stage('Clone'){
            checkout scm
        }

        stage('Build'){
            echo 'Building...'
        }
      
        stage('Remote SSH') {
            sshCommand remote : remote, command: 'sudo mkdir /test'
            // writeFile file: 'abc.sh', text: 'ls -lrt'
            // sshScript remote : remote, script: "abc.sh"
        }

        stage('test'){

        }

        stage('deploy'){

        }
    } catch(e) {
        currentBuild.result = "FAILED"
    }
}

//