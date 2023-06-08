# browserstack_techc
Repository for BrowserStack Tech Challenge - 06/05/2023
## Prerequisite

1. An operating system with Jenkins Server installed
2. Install and configure Browserstack Plugin in Jenkins
To setup Browserstack Plugin in jenkins reference the following link:
```
(https://www.browserstack.com/docs/automate/selenium/jenkins#install-and-configure-the-browserstack-jenkins-plugin)
```

## Steps to run test session

1. Update jenkinsfile operating system myType variable in environment if needed:

- If your operating system of choice differs replace myType with "linux=ia32" for a 32bit Linux, "win-32" for Windows or "darwin-x64" for Mac OS X etc.

  - Linux
  ```
  "linux=ia32"
  ```
  - Windows
  ```
  "win-32"
  ```
  - Mac OS C
  ```
  "darwin-x64"
  ```
2. Add your credential as type 'Browserstack' to add your username and access key and set ID to:
```
'BS_Login'
```
3. Add your browserstack login credentials from your Jenkins server and set the ID:
```
'Trial'
```
4. Create a pipeline with definition as "Pipeline script from SCM"

  - Select 'git' in the SCM dropdown and add the following Repository URL:
  ```
  https://github.com/exr4361/browserstack_techc.git
  ```
 - In the Branches to build section change the Branch Specifier:
  ```
  */main
  ```
  - Click "Save"
5. Run the pipepline by clicking "Build Now"


