pipeline {
   agent any

   stages {

    stage('Checkout') {
         steps {
        git 'https://github.com/sridharkidambi/beelineProcessor'

        }
       }
      stage('download files from s3') {


         steps {

            sh 'aws s3 sync s3://beelineprocess  files'
            sh 'aws s3 sync s3://beelineprocess  files'
            sh 'ls -latr'

         }

      }


  }

}