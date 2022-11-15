// slack 채널 변수
def SLACK_CHANNEL = "jenkins"

// 함수
def notifyCommon(slack_channel, message) {
    slackSend (channel: "${slack_channel}", color: '#FFFF00', message: "${message}")
}

// def remote = [:]
// remote.name = 'ubuntu'
// remote.host = '54.180.131.194'
// // remote.password = 'password'
// remote.allowAnyHosts = true
// remote.user = 'ubuntu'

env.TARGET_HOST = 'ubuntu@54.180.131.194'

node {
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
      
        // stage('Remote SSH') {
        //     sshCommand remote: remote, command: 'sh "mkdir ~/test"'
        //     // writeFile file: 'abc.sh', text: 'ls -lrt'
        //     // sshScript remote : remote, script: "abc.sh"
        // }

        stage('test'){
            sh ('ssh ubuntu@ec2 "cd test"')
            sh ('ssh ubuntu@ec2 "source /home/ubuntu/venvs/dogma/bin/activate"')
            // sh ('ssh ubuntu@ec2 "cd ~/projects/Bigdata_busan/ldg/project"')
            sh ('ssh ubuntu@ec2 "pwd"')
            sh ('ssh ubuntu@ec2 "export FLASK_APP=dogma"')
            sh ('ssh ubuntu@ec2 "export FLASK_DEBUG=true"')
            sh ('ssh ubuntu@ec2 "export APP_CONFIG_FILE=/home/ubuntu/projects/Bigdata_busan/ldg/project/config/production.py"')
            sh ('ssh ubuntu@ec2 "cd /home/ubuntu/projects/Bigdata_busan/ldg/project && pwd && git pull"')
        }

        stage('deploy'){
            // sshagent (credentials: ['ssh key']) {
            //     sh 'ssh -v ubuntu@54.180.131.194'
            //     sh 'ssh ubuntu@54.180.131.194 mkdir ~/test'
            }


        } catch(e) {
        currentBuild.result = "FAILED"
    }
}

//