# browserstack_techc
Repository for BrowserStack Tech Challenge - 06/05/2023
## Prerequisite
```
An operating system with Jenkins Server installed
```
```
Install and configure Browserstack Plugin in Jenkins
```
To setup Browserstack Plugin in jenkins reference the following link:
```
[https://www.browserstack.com/docs/automate/selenium/jenkins](https://www.browserstack.com/docs/automate/selenium/jenkins#install-and-configure-the-browserstack-jenkins-plugin)
```

## Steps to run test session

- Update jenkinsfile operating system myType variable in environment if needed:

If your operating system of choice differs replace myType with "linux=ia32" for a 32bit Linux, "win-32" for Windows or "darwin-x64" for Mac OS X etc.

a. Linux
```
"linux=ia32"
```
b. Windows
```
"win-32"
```
c. Mac OS C
```
"darwin-x64"
```
- Add your credential as type 'Browserstack' to add your username and access key and set ID to 'BS_Creds'
- Add your browserstack login credentials from your Jenkins server and set the ID 'Trial'
- Create a pipeline with definition as "Pipeline script from SCM"

  a. Select 'git' in the SCM dropdown and add the following Repository URL:
  ```
  https://github.com/exr4361/browserstack_techc.git
  ```
  b. In the Branches to build section change the Branch Specifier:
  ```
  */main
  ```
  c. Click "Save"
- Run the pipepline by clicking "Build Now"


