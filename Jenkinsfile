 pipeline {
   agent any
   stages {
         stage('setup') {
          environment {
                   BS_Credentials = credentials('Trial')
               }
           steps {
             browserstack(credentialsId: 'BS_Creds', localConfig: [localOptions: '', localPath: '']) {
                 echo 'hello bs'
                 // BrowserStack Local configuration
                 sh 'curl -sS https://www.browserstack.com/browserstack-local/BrowserStackLocal-darwin-x64.zip > /var/tmp/BrowserStackLocal.zip'
                 sh "unzip -o /var/tmp/BrowserStackLocal.zip -d /var/tmp"
                 sh "chmod +x /var/tmp/BrowserStackLocal"
                 sh './BrowserStackLocal --key $BROWSERSTACK_ACCESS_KEY --daemon start'
                 // Test Script
                 sh 'python3 browserstechchallenge.py' 
                 sh './BrowserStackLocal --key $BROWSERSTACK_ACCESS_KEY --daemon stop'
                 
             }
             browserStackReportPublisher 'automate'
           }
         }
       }
     }
   
