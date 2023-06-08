pipeline {
   agent any
   stages {
         stage('setup') {
          environment {
                   BS_Login = credentials('Trial')
                   // Type of operating system
                   myType = 'darwin-x64'
               }
           steps {
             browserstack(credentialsId: 'BS_Creds', localConfig: [localOptions: '', localPath: '']) {
                 // BrowserStack Local configuration
                 sh 'curl -sS https://www.browserstack.com/browserstack-local/BrowserStackLocal-$myType.zip > /var/tmp/BrowserStackLocal.zip'
                 sh "unzip -o /var/tmp/BrowserStackLocal.zip -d /var/tmp"
                 sh "chmod +x /var/tmp/BrowserStackLocal"
                 sh '/var/tmp/BrowserStackLocal --key $BROWSERSTACK_ACCESS_KEY --daemon start'
                 // Test Script
                 sh 'pip3 install -r requirements.txt --user'
                 sh 'pip3 install urllib3==1.26.6 --user'
                 sh 'python3 browserstack_techchallenge2.py'
                 sh '/var/tmp/BrowserStackLocal --key $BROWSERSTACK_ACCESS_KEY --daemon stop'
             }
             browserStackReportPublisher 'automate'
           }
         }
       }
     }
   
