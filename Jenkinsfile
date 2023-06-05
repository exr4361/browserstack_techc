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
                 sh '/usr/local/bin/wget "https://www.browserstack.com/browserstack-local/BrowserStackLocal-darwin-x64.zip"'
                 sh 'unzip BrowserStackLocal-darwin-x64.zip'
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
   
