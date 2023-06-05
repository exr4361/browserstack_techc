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
                 sh 'pip3 install -r requirements.txt --user'
                 sh 'pip3 install urllib3==1.26.6 --user'
                 // BrowserStack Local configuration
                 sh 'wget "https://www.browserstack.com/browserstack-local/BrowserStackLocal-darwin-x64.zip"'
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
   
